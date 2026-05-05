"""
Authentication views for user management.

Handles:
user registration (self-registration)
login and logout
password reset (forgot password)
profile viewing and updating
password changing

"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from .forms import RegistrationForm
from .models import User

def register(request):
    """Handles user self-registration

    GET: Display empty registration form
    POST: Validate form, create user and log them in automatically

    After successful registration, user is redirected to dashboard.
    
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome!')
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    """Handles user login page

    GET: Display login form
    POST: Authenticate user credentials and create session
    
    Uses Django's built-in authenticate() function.
    Redirects to dashboard on success, shows error on failure.
    
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

def user_logout(request):
    """
    Handle user logout.
    
    Destroys user session and redirects to login page.
    Shows confirmation message to user.

    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

def forgot_password(request):
    """
    Handle password reset requests.
    
    For production: This should send an email with reset link.
    For coursework: Shows success message as demonstration.
    
    In a real implementation, would use Django's PasswordResetView.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # In production, send actual email
            messages.success(request, f'Password reset link sent to {email}')
        except User.DoesNotExist:
            messages.error(request, 'No account found with that email.')
        return redirect('login')
    return render(request, 'accounts/forgot_password.html')

@login_required
def profile(request):
    """
    Display user profile page.
    
    Shows all user information including:
    - Username, email, full name
    - Role, phone, department
    - Last login time
    
    Requires user to be logged in (@login_required decorator).
    """
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def update_profile(request):
    """
    Handle profile update form submission.
    
    Updates editable fields:
    - First name, last name
    - Email address
    - Phone number
    - Department
    
    Requires user to be logged in.
    """
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.phone = request.POST.get('phone', '')
        user.department = request.POST.get('department', '')
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'accounts/update_profile.html')

@login_required
def change_password(request):
    """
    Handle password change form.
    
    Validates:
    1. Old password is correct
    2. New password and confirmation match
    3. New password meets minimum length (8 characters)
    
    After successful change, user must login again with new password.
    """
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not request.user.check_password(old_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        elif len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Password changed successfully! Please login again.')
            return redirect('login')
    return render(request, 'accounts/change_password.html')

