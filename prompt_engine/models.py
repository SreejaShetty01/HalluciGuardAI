from django.db import models
from django.contrib.auth.models import User
import uuid


class PromptHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prompt_histories')
    query = models.TextField()
    session_id = models.CharField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Prompt Histories'

    def save(self, *args, **kwargs):
        if not self.session_id:
            self.session_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}: {self.query[:60]}"

    def get_best_response(self):
        return self.responses.order_by('hallucination_score').first()


class Response(models.Model):
    PROMPT_TYPE_CHOICES = [
        ('zero_shot', 'Zero-Shot'),
        ('few_shot', 'Few-Shot'),
        ('chain_of_thought', 'Chain-of-Thought'),
        ('role_based', 'Role-Based'),
    ]

    prompt_history = models.ForeignKey(PromptHistory, on_delete=models.CASCADE, related_name='responses')
    prompt_type = models.CharField(max_length=50, choices=PROMPT_TYPE_CHOICES)
    prompt_text = models.TextField()
    response_text = models.TextField()
    response_time = models.FloatField(default=0.0, help_text="Response time in seconds")
    token_count = models.IntegerField(default=0)

    # Scores (0.0 - 1.0)
    hallucination_score = models.FloatField(default=0.0)
    confidence_score = models.FloatField(default=0.0)
    accuracy_score = models.FloatField(default=0.0)
    consistency_score = models.FloatField(default=0.0)
    fluency_score = models.FloatField(default=0.0)
    similarity_score = models.FloatField(default=0.0)

    is_hallucinated = models.BooleanField(default=False)
    api_success = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['prompt_type']

    def __str__(self):
        return f"[{self.prompt_type}] {self.prompt_history.query[:40]}"

    def hallucination_pct(self):
        return round(self.hallucination_score * 100, 1)

    def accuracy_pct(self):
        return round(self.accuracy_score * 100, 1)

    def confidence_pct(self):
        return round(self.confidence_score * 100, 1)

    def consistency_pct(self):
        return round(self.consistency_score * 100, 1)

    def fluency_pct(self):
        return round(self.fluency_score * 100, 1)


class HallucinationReport(models.Model):
    response = models.OneToOneField(Response, on_delete=models.CASCADE, related_name='hallucination_report')
    factual_consistency = models.FloatField(default=0.0)
    keyword_mismatch_count = models.IntegerField(default=0)
    suspicious_phrases = models.TextField(blank=True)
    rule_based_flags = models.TextField(blank=True)
    semantic_similarity = models.FloatField(default=0.0)
    overall_hallucination_pct = models.FloatField(default=0.0)
    analysis_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report: {self.response}"

    def risk_level(self):
        if self.overall_hallucination_pct < 25:
            return 'low'
        elif self.overall_hallucination_pct < 55:
            return 'medium'
        return 'high'


class ModelComparison(models.Model):
    prompt_history = models.OneToOneField(PromptHistory, on_delete=models.CASCADE, related_name='comparison')
    best_prompt_type = models.CharField(max_length=50)
    lowest_hallucination_score = models.FloatField()
    highest_accuracy_score = models.FloatField()
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comparison for: {self.prompt_history.query[:40]}"
