# URL & Redirecting
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

# Authentication
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Forms & Models 
from .models import User, Profile
from .forms import SignUpForm, ProfileForm

# Messages
from django.contrib import messages

# Create your views here.

def sign_up(req):
    form = SignUpForm()
    if (req.method == 'POST'):
        form = SignUpForm(req.POST)
        if (form.is_valid()):
            # Save the user
            form.save()
            messages.success(req, "Account Created Successfully")
            return HttpResponseRedirect(reverse('AppLogin:login'))
    return render(req, 'AppLogin/sign_up.html', context={'form':form})

def login_user(req):
    form = AuthenticationForm()
    if(req.method == 'POST'):
        form = AuthenticationForm(data=req.POST)
        if(form.is_valid()):
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if(user is not None):
                login(req, user)
                return HttpResponseRedirect(reverse('AppShop:home'))
    return render(req, 'AppLogin/login.html', context={'form':form })
@login_required
def logout_user(req):
    logout(req)
    messages.warning(req, "You have been logged out!")
    return HttpResponseRedirect(reverse('AppShop:home'))

@login_required
def profile_user(req):
    profile = Profile.objects.get(user=req.user)
    form = ProfileForm(instance=profile)
    if(req.method == 'POST'):
        form = ProfileForm(req.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(req, "Profile updated successfully!")
            form = ProfileForm(instance=profile)
    return render(req, 'AppLogin/change_profile.html', context={'form':form})