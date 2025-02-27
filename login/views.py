from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User 
from django.http import JsonResponse
import json
from .models import Users

# Create your views here.
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
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phoneno = request.POST.get('phoneno')
        status = request.POST.get('status')
        interests = request.POST.get('interests')
        
        interests = json.loads(interests)
        type = request.POST.get('type', 'guest')
        print(f"User Details are here: {first_name} : {last_name} : {username} : {password} : {email} : {phoneno} : {status} : {interests} : {type}")
        user = Users(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
            phone=phoneno,
            status=status,
            interests=interests,
            type=type
        )
        user.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect(f'{reverse("homepage")}?username={username}')
    return render(request, 'login/userregister.html')

# def homepage_view(request):
#     user_authenticated = request.user.is_authenticated
#     return render(request, 'dashboard/homepage.html', {'user_authenticated': user_authenticated})

# def logout_view(request):
#     logout(request)
#     return redirect('homepage')

# def profile_view(request):
#     if request.user.is_authenticated:
#         user = request.user
#         return render(request, 'login/profile.html', {'user': user})
#     return redirect('login')