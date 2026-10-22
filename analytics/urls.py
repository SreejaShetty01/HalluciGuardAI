from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_dashboard, name='analytics_dashboard'),
    path('reports/', views.hallucination_reports, name='hallucination_reports'),
]
