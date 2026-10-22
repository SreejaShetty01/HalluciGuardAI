from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import models as django_models
from django.db.models import Sum
from functools import wraps
from .models import AdminAccount
from .forms import AdminLoginForm, UserUpdateForm
from authentication.models import UserProfile, ActivityLog

def admin_required(view_func):
    """Decorator to ensure custom admin session authentication is present."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'custom_admin_id' not in request.session:
            messages.error(request, 'Please log in as an administrator first.')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_login(request):
    """Custom login view for the admin module, auto-populating admin/admin if empty."""
    # Ensure default admin account exists
    if not AdminAccount.objects.filter(username='admin').exists():
        AdminAccount.objects.create(username='admin', password='admin')

    if 'custom_admin_id' in request.session:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                admin_user = AdminAccount.objects.get(username=username)
                if admin_user.check_password(password):
                    request.session['custom_admin_id'] = admin_user.id
                    request.session['custom_admin_username'] = admin_user.username
                    messages.success(request, f'Welcome back, administrator {admin_user.username}!')
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, 'Invalid admin username or password.')
            except AdminAccount.DoesNotExist:
                messages.error(request, 'Invalid admin username or password.')
    else:
        form = AdminLoginForm()
    return render(request, 'custom_admin/login.html', {'form': form})

def admin_logout(request):
    """Custom logout view for clearing admin sessions."""
    if 'custom_admin_id' in request.session:
        del request.session['custom_admin_id']
    if 'custom_admin_username' in request.session:
        del request.session['custom_admin_username']
    messages.info(request, 'Admin logged out successfully.')
    return redirect('admin_login')

@admin_required
def admin_dashboard(request):
    """Admin dashboard homepage displaying overall metrics and stats."""
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    inactive_users = User.objects.filter(is_active=False).count()
    total_queries = UserProfile.objects.aggregate(total=Sum('total_queries'))['total'] or 0
    recent_users = User.objects.order_by('-date_joined')[:5]

    context = {
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
        'total_queries': total_queries,
        'recent_users': recent_users,
    }
    return render(request, 'custom_admin/dashboard.html', context)

@admin_required
def admin_users(request):
    """Admin view showing a searchable datatable of all registered users."""
    users = User.objects.all().select_related('profile').order_by('-date_joined')
    search_query = request.GET.get('search', '').strip()
    if search_query:
        users = users.filter(
            django_models.Q(username__icontains=search_query) |
            django_models.Q(first_name__icontains=search_query) |
            django_models.Q(last_name__icontains=search_query) |
            django_models.Q(email__icontains=search_query)
        )
    
    context = {
        'users': users,
        'search_query': search_query,
    }
    return render(request, 'custom_admin/users.html', context)

@admin_required
def admin_user_toggle_status(request, user_id):
    """Endpoint to activate or deactivate a user."""
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        status_str = "activated" if user.is_active else "deactivated"
        messages.success(request, f"User {user.username} has been {status_str} successfully.")
    return redirect('admin_users')

@admin_required
def admin_user_update(request, user_id):
    """Endpoint to update details and bio for a specific user."""
    user = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user, profile=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f"User details for {user.username} updated successfully.")
            return redirect('admin_users')
        else:
            messages.error(request, "Failed to update user details. Please check the errors.")
    else:
        form = UserUpdateForm(instance=user, profile=profile)
    
    context = {
        'form': form,
        'user_to_edit': user,
    }
    return render(request, 'custom_admin/edit_user.html', context)

@admin_required
def admin_user_delete(request, user_id):
    """Endpoint to permanently delete a user from the system."""
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"User {username} has been deleted successfully.")
    return redirect('admin_users')
