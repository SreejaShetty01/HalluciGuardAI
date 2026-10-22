import json
import io
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Avg, Count, Min, Max
from .models import PromptHistory, Response, HallucinationReport, ModelComparison
from .prompt_generator import PromptGenerator
from llm_api.gemini_client import GeminiClient
from hallucination_detector.analyzer import HallucinationAnalyzer
from authentication.models import ActivityLog


def _safe_pct(val):
    """Convert 0-1 float to rounded percentage."""
    return round((val or 0) * 100, 1)


@login_required
def user_dashboard(request):
    user = request.user
    histories = PromptHistory.objects.filter(user=user)
    responses = Response.objects.filter(prompt_history__user=user)

    total_queries = histories.count()
    total_responses = responses.count()
    hallucinated_count = responses.filter(is_hallucinated=True).count()
    clean_count = responses.filter(is_hallucinated=False).count()

    agg = responses.aggregate(
        avg_hall=Avg('hallucination_score'),
        avg_acc=Avg('accuracy_score'),
        avg_lat=Avg('response_time'),
    )

    prompt_stats = list(
        responses.values('prompt_type').annotate(
            avg_hall=Avg('hallucination_score'),
            avg_acc=Avg('accuracy_score'),
            avg_conf=Avg('confidence_score'),
            avg_flu=Avg('fluency_score'),
            avg_lat=Avg('response_time'),
            count=Count('id'),
        ).order_by('prompt_type')
    )
    for s in prompt_stats:
        s['avg_hall'] = _safe_pct(s['avg_hall'])
        s['avg_acc'] = _safe_pct(s['avg_acc'])
        s['avg_conf'] = _safe_pct(s['avg_conf'])
        s['avg_flu'] = _safe_pct(s['avg_flu'])
        s['avg_lat'] = round(s['avg_lat'] or 0, 3)

    best_prompt = min(prompt_stats, key=lambda x: x['avg_hall']) if prompt_stats else None
    recent_history = histories.prefetch_related('responses')[:8]

    context = {
        'total_queries': total_queries,
        'total_responses': total_responses,
        'hallucinated_count': hallucinated_count,
        'clean_count': clean_count,
        'avg_hallucination': _safe_pct(agg['avg_hall']),
        'avg_accuracy': _safe_pct(agg['avg_acc']),
        'avg_latency': round(agg['avg_lat'] or 0, 3),
        'best_prompt': best_prompt,
        'prompt_stats': prompt_stats,
        'prompt_stats_json': json.dumps(prompt_stats),
        'recent_history': recent_history,
        'hall_yes': hallucinated_count,
        'hall_no': clean_count,
    }
    return render(request, 'dashboard/user_dashboard.html', context)


@login_required
def prompt_test(request):
    if request.method == 'POST':
        query = request.POST.get('query', '').strip()
        if not query:
            messages.error(request, 'Please enter a question or query.')
            return redirect('prompt_test')
        if len(query) < 5:
            messages.error(request, 'Query is too short. Please provide a meaningful question.')
            return redirect('prompt_test')

        # Create history record
        history = PromptHistory.objects.create(user=request.user, query=query)

        # Generate prompts
        generator = PromptGenerator(query)
        all_prompts = generator.generate_all()

        # Initialize Gemini client
        client = GeminiClient()
        results = []

        for ptype, pdata in all_prompts.items():
            api_result = client.generate_response(pdata['prompt'])
            analyzer = HallucinationAnalyzer(query, api_result['response'])
            analysis = analyzer.analyze()

            resp = Response.objects.create(
                prompt_history=history,
                prompt_type=ptype,
                prompt_text=pdata['prompt'],
                response_text=api_result['response'],
                response_time=api_result['response_time'],
                token_count=api_result['token_count'],
                hallucination_score=analysis['hallucination_score'],
                confidence_score=analysis['confidence_score'],
                accuracy_score=analysis['accuracy_score'],
                consistency_score=analysis['consistency_score'],
                fluency_score=analysis['fluency_score'],
                similarity_score=analysis['similarity_score'],
                is_hallucinated=analysis['is_hallucinated'],
                api_success=api_result['success'],
            )

            HallucinationReport.objects.create(
                response=resp,
                factual_consistency=analysis['factual_consistency'],
                keyword_mismatch_count=analysis['keyword_mismatch_count'],
                suspicious_phrases=analysis['suspicious_phrases'],
                rule_based_flags=analysis['rule_based_flags'],
                semantic_similarity=analysis['semantic_similarity'],
                overall_hallucination_pct=analysis['hallucination_percentage'],
                analysis_notes=analysis['analysis_notes'],
            )

            results.append({
                'type': ptype,
                'hall_pct': analysis['hallucination_percentage'],
                'acc': analysis['accuracy_score'],
            })

        # Save comparison summary
        best = min(results, key=lambda x: x['hall_pct'])
        ModelComparison.objects.create(
            prompt_history=history,
            best_prompt_type=best['type'],
            lowest_hallucination_score=best['hall_pct'] / 100,
            highest_accuracy_score=best['acc'],
            summary=f"Best: {best['type']} with {round(best['hall_pct'], 1)}% hallucination",
        )

        # Update user profile
        try:
            profile = request.user.profile
            profile.total_queries += 1
            profile.save()
        except Exception:
            pass

        ActivityLog.objects.create(
            user=request.user, action='prompt_test',
            details=f"Query: {query[:120]}",
            ip_address=request.META.get('REMOTE_ADDR'),
        )

        messages.success(request, f'Analysis complete! 4 prompt types tested for: "{query[:60]}..."')
        return redirect('compare_responses', session_id=history.session_id)

    recent = PromptHistory.objects.filter(user=request.user).prefetch_related('responses')[:6]
    return render(request, 'prompts/test.html', {'recent': recent})


@login_required
def compare_responses(request, session_id):
    history = get_object_or_404(PromptHistory, session_id=session_id, user=request.user)
    responses = history.responses.select_related('hallucination_report').order_by('prompt_type')

    data = []
    for r in responses:
        report = getattr(r, 'hallucination_report', None)
        data.append({
            'id': r.id,
            'type': r.prompt_type,
            'label': r.get_prompt_type_display(),
            'prompt': r.prompt_text,
            'response': r.response_text,
            'response_time': r.response_time,
            'token_count': r.token_count,
            'hallucination_score': _safe_pct(r.hallucination_score),
            'confidence_score': _safe_pct(r.confidence_score),
            'accuracy_score': _safe_pct(r.accuracy_score),
            'consistency_score': _safe_pct(r.consistency_score),
            'fluency_score': _safe_pct(r.fluency_score),
            'similarity_score': _safe_pct(r.similarity_score),
            'is_hallucinated': r.is_hallucinated,
            'api_success': r.api_success,
            'report': {
                'hallucination_pct': round(report.overall_hallucination_pct, 1) if report else 0,
                'factual': round(report.factual_consistency * 100, 1) if report else 0,
                'suspicious': report.suspicious_phrases if report else '',
                'flags': report.rule_based_flags if report else '',
                'notes': report.analysis_notes if report else '',
                'risk': report.risk_level() if report else 'unknown',
            } if report else {},
        })

    best = min(data, key=lambda x: x['hallucination_score']) if data else None
    worst = max(data, key=lambda x: x['hallucination_score']) if data else None

    comparison = getattr(history, 'comparison', None)

    context = {
        'history': history,
        'responses': data,
        'responses_json': json.dumps(data),
        'best': best,
        'worst': worst,
        'comparison': comparison,
    }
    return render(request, 'prompts/compare.html', context)


@login_required
def prompt_history_list(request):
    histories = PromptHistory.objects.filter(user=request.user).prefetch_related('responses')
    search = request.GET.get('search', '').strip()
    if search:
        histories = histories.filter(query__icontains=search)
    context = {'histories': histories, 'search': search}
    return render(request, 'prompts/history.html', context)


@login_required
def export_excel(request, session_id):
    import pandas as pd

    history = get_object_or_404(PromptHistory, session_id=session_id, user=request.user)
    responses = history.responses.select_related('hallucination_report').all()

    rows = []
    for r in responses:
        report = getattr(r, 'hallucination_report', None)
        rows.append({
            'Prompt Type': r.get_prompt_type_display(),
            'Response Time (s)': r.response_time,
            'Hallucination Score (%)': _safe_pct(r.hallucination_score),
            'Accuracy Score (%)': _safe_pct(r.accuracy_score),
            'Confidence Score (%)': _safe_pct(r.confidence_score),
            'Consistency Score (%)': _safe_pct(r.consistency_score),
            'Fluency Score (%)': _safe_pct(r.fluency_score),
            'Is Hallucinated': 'Yes' if r.is_hallucinated else 'No',
            'Factual Consistency': round(report.factual_consistency * 100, 1) if report else '',
            'Suspicious Phrases': report.suspicious_phrases if report else '',
            'Analysis Notes': report.analysis_notes if report else '',
            'Response Preview': r.response_text[:300],
        })

    df = pd.DataFrame(rows)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Hallucination Analysis')
        # Style the worksheet
        ws = writer.sheets['Hallucination Analysis']
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 50)

    output.seek(0)
    fname = f"halluci_report_{history.session_id[:8]}.xlsx"
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{fname}"'

    ActivityLog.objects.create(
        user=request.user, action='export',
        details=f"Exported Excel for session {session_id[:8]}"
    )
    return response


@login_required
def delete_history(request, session_id):
    history = get_object_or_404(PromptHistory, session_id=session_id, user=request.user)
    if request.method == 'POST':
        history.delete()
        messages.success(request, 'Query history deleted.')
    return redirect('prompt_history')
