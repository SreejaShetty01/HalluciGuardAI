from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import UserProfile, ActivityLog


def home_view(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    return render(request, 'dashboard/home.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate user on registration
            user.save()
            UserProfile.objects.get_or_create(user=user)
            ActivityLog.objects.create(
                user=user, action='register',
                details='New account registration (pending admin activation)',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.warning(request, 'wait until activated by admin')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'auth/auth_combined.html', {'form': form, 'active_tab': 'register'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            ActivityLog.objects.create(
                user=user, action='login',
                details='User logged in',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            next_url = request.GET.get('next', 'user_dashboard')
            return redirect(next_url)
        else:
            # Check if user exists but is deactivated
            username = request.POST.get('username')
            try:
                from django.contrib.auth.models import User
                user = User.objects.filter(username=username).first()
                if user and not user.is_active:
                    messages.error(request, 'Your account is deactivated. An administrator must activate it before you can log in.')
                else:
                    messages.error(request, 'Invalid username or password.')
            except Exception:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'auth/auth_combined.html', {'form': form, 'active_tab': 'login'})


def logout_view(request):
    if request.user.is_authenticated:
        ActivityLog.objects.create(
            user=request.user, action='logout',
            details='User logged out'
        )
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')
