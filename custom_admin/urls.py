from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.admin_users, name='admin_users'),
    path('users/toggle/<int:user_id>/', views.admin_user_toggle_status, name='admin_user_toggle_status'),
    path('users/edit/<int:user_id>/', views.admin_user_update, name='admin_user_update'),
    path('users/delete/<int:user_id>/', views.admin_user_delete, name='admin_user_delete'),
]
