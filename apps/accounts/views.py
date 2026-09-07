from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import SignupForm, LoginForm, ProfileForm

# Create your views here.

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('projects:list')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome your account has been created')
            return redirect('projects:list')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('projects:list')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('projects:list')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('accounts:login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})





