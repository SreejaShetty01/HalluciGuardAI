import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from prompt_engine.models import PromptHistory, Response, HallucinationReport


def _p(v):
    return round((v or 0) * 100, 1)


@login_required
def analytics_dashboard(request):
    user = request.user
    responses = Response.objects.filter(prompt_history__user=user)

    prompt_hall = list(
        responses.values('prompt_type').annotate(
            avg_hall=Avg('hallucination_score'),
            avg_acc=Avg('accuracy_score'),
            avg_lat=Avg('response_time'),
            avg_conf=Avg('confidence_score'),
            avg_cons=Avg('consistency_score'),
            avg_flu=Avg('fluency_score'),
            count=Count('id'),
        ).order_by('prompt_type')
    )
    for item in prompt_hall:
        item['avg_hall'] = _p(item['avg_hall'])
        item['avg_acc'] = _p(item['avg_acc'])
        item['avg_conf'] = _p(item['avg_conf'])
        item['avg_cons'] = _p(item['avg_cons'])
        item['avg_flu'] = _p(item['avg_flu'])
        item['avg_lat'] = round(item['avg_lat'] or 0, 3)

    hall_yes = responses.filter(is_hallucinated=True).count()
    hall_no = responses.filter(is_hallucinated=False).count()

    # Time series data using SQLite date function
    from django.db import connection
    time_series = []
    try:
        time_series = list(
            responses.extra(select={'day': "strftime('%%Y-%%m-%%d', created_at)"})
            .values('day', 'prompt_type')
            .annotate(avg_hall=Avg('hallucination_score'))
            .order_by('day')[:40]
        )
        for item in time_series:
            item['avg_hall'] = _p(item['avg_hall'])
    except Exception:
        pass

    total_queries = PromptHistory.objects.filter(user=user).count()
    total_hall = responses.filter(is_hallucinated=True).count()
    best_prompt = min(prompt_hall, key=lambda x: x['avg_hall']) if prompt_hall else None
    agg = responses.aggregate(avg_lat=Avg('response_time'), avg_acc=Avg('accuracy_score'))

    context = {
        'prompt_hall': prompt_hall,
        'prompt_hall_json': json.dumps(prompt_hall),
        'hall_yes': hall_yes,
        'hall_no': hall_no,
        'time_series_json': json.dumps(time_series),
        'total_queries': total_queries,
        'total_hallucinations': total_hall,
        'best_prompt': best_prompt,
        'avg_latency': round(agg['avg_lat'] or 0, 3),
        'avg_accuracy': _p(agg['avg_acc']),
    }
    return render(request, 'analytics/dashboard.html', context)


@login_required
def hallucination_reports(request):
    reports = (
        HallucinationReport.objects
        .filter(response__prompt_history__user=request.user)
        .select_related('response', 'response__prompt_history')
        .order_by('-created_at')
    )
    search = request.GET.get('search', '').strip()
    if search:
        reports = reports.filter(response__prompt_history__query__icontains=search)

    context = {'reports': reports, 'search': search}
    return render(request, 'analytics/reports.html', context)
