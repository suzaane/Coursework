from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request):
    """Temporary stub until auth lead provides the real view."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    """Temporary stub."""
    return render(request, 'accounts/register.html')

@login_required
def profile_view(request):
    """Temporary stub."""
    return render(request, 'accounts/profile.html')

def logout_view(request):
    """Temporary stub."""
    logout(request)
    return redirect('accounts:login')