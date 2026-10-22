from django.contrib import admin
from .models import PromptHistory, Response, HallucinationReport, ModelComparison


@admin.register(PromptHistory)
class PromptHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'query_short', 'response_count', 'created_at']
    search_fields = ['query', 'user__username']
    list_filter = ['created_at']

    def query_short(self, obj):
        return obj.query[:60]
    query_short.short_description = 'Query'

    def response_count(self, obj):
        return obj.responses.count()
    response_count.short_description = 'Responses'


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['prompt_type', 'hall_pct_display', 'accuracy_pct', 'is_hallucinated', 'response_time', 'created_at']
    list_filter = ['prompt_type', 'is_hallucinated', 'created_at']
    search_fields = ['prompt_history__query', 'response_text']

    def hall_pct_display(self, obj):
        return f"{round(obj.hallucination_score * 100, 1)}%"
    hall_pct_display.short_description = 'Hallucination %'


@admin.register(HallucinationReport)
class HallucinationReportAdmin(admin.ModelAdmin):
    list_display = ['response', 'overall_hallucination_pct', 'factual_consistency', 'created_at']
    list_filter = ['created_at']


@admin.register(ModelComparison)
class ModelComparisonAdmin(admin.ModelAdmin):
    list_display = ['prompt_history', 'best_prompt_type', 'lowest_hallucination_score', 'created_at']
