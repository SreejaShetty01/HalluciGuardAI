from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_dashboard, name='user_dashboard'),
    path('test/', views.prompt_test, name='prompt_test'),
    path('compare/<str:session_id>/', views.compare_responses, name='compare_responses'),
    path('history/', views.prompt_history_list, name='prompt_history'),
    path('export/<str:session_id>/', views.export_excel, name='export_excel'),
    path('delete/<str:session_id>/', views.delete_history, name='delete_history'),
]
