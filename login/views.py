from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from django.http import JsonResponse
from django.db.utils import IntegrityError
import json
from .models import Users
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        loginid = request.POST.get('loginid')
        password = request.POST.get('password')
        print(f"Login ID: {loginid}, Password: {password}")
        user = authenticate(request, username=loginid, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': reverse('dashboard')})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})
    return render(request, 'login/loginpage.html')

def userregister_view(request):
    if request.method == 'POST':
        first_name    = request.POST.get('first_name')
        last_name     = request.POST.get('last_name')
        username      = request.POST.get('username')
        password      = request.POST.get('password')
        email         = request.POST.get('email')
        phoneno       = request.POST.get('phoneno')
        status        = request.POST.get('status')
        interests_str = request.POST.get('interests')
        type_field    = request.POST.get('type', 'Guest')
        
        try:
            interests = json.loads(interests_str)
        except (TypeError, json.JSONDecodeError):
            interests = []
        
        # Debug print
        print(f"User Details: {first_name} | {last_name} | {username} | {password} | {email} | {phoneno} | {status} | {interests} | {type_field}")
        
        try:
            user = Users.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phoneno,
                status=status,
                interests=interests,
                type=type_field
            )
        except IntegrityError:
            return render(request, 'login/userregister.html', {'error': 'Username already exists'})
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect(f'{reverse("homepage")}?username={username}')
    
    return render(request, 'login/userregister.html')

def logout_view(request):
    logout(request)
    return redirect('homepage')


@login_required(login_url='loginpage')
def profile_view(request):
    user = request.user
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        interests_data = request.POST.get("interests_data", "[]")
        try:
            interests = json.loads(interests_data)
        except json.JSONDecodeError:
            interests = []

        # Update user fields
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.interests = interests

        if request.FILES.get("profile_image"):
            user.profile_image = request.FILES.get("profile_image")

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, "login/profile.html", {"user": user})

def dashboard_view(request):
    return render(request, 'dashboard/homepage.html')

def check_username(request):
    if request.method == "POST":
        username = request.POST.get("username")
        exists = Users.objects.filter(username=username).exists()
        return JsonResponse({"exists": exists})
    return JsonResponse({"exists": False})