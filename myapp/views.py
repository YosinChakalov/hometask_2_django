from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate
from .forms import *
from .models import *


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            request.session['id'] = user.id
            return redirect('profile')
        else:
            context = "Invalid username or password"
            return render(request, 'login.html', {'context': context})
    return render(request, 'login.html')


def profile(request):
    user_id = request.session.get('id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)

    return render(request, 'profile.html', {'user': user,'profile': profile})


def profile_edit(request):
    user_id = request.session.get('id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile_edit.html', {'form': form,'user': user,'profile': profile})

def logout(request):
    request.session.flush()
    return redirect('login')