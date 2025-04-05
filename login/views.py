from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db.utils import IntegrityError
import json
from .models import Users
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Return a response that tells the client to redirect
            return JsonResponse({
                'success': True,
                'redirect_url': reverse('homepage')
            })
        else:
            # Return error message for invalid credentials
            return JsonResponse({
                'success': False,
                'error': 'Invalid credentials. Please try again.'
            })
    return render(request, 'login/loginpage.html')


def userregister_view(request):
    if request.method == 'POST':
        first_name    = request.POST.get('first_name', '').strip()
        last_name     = request.POST.get('last_name', '').strip()
        username      = request.POST.get('username', '').strip()
        password      = request.POST.get('password', '').strip()
        email         = request.POST.get('email', '').strip()
        phone         = request.POST.get('phone', '').strip()
        interests_str = request.POST.get('interests', '[]').strip()
        try:
            interests = json.loads(interests_str)
        except json.JSONDecodeError:
            interests = []
            
        # Check for duplicate username
        if Users.objects.filter(username=username).exists():
            error_msg = "User already exists!"
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({'success': False, 'error': error_msg})
            else:
                messages.error(request, error_msg)
                return render(request, 'login/userregister.html')
            
        if Users.objects.filter(email=email).exists():
            error_msg = "Email already exists!"
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({'success': False, 'error': error_msg})
            else:
                messages.error(request, error_msg)
                return render(request, 'login/userregister.html')
        
        try:
            user = Users.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                interests=interests,
                type="user"
            )
        except Exception as e:
            err_msg = f"Error creating account: {str(e)}"
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({'success': False, 'error': err_msg})
            else:
                messages.error(request, err_msg)
                return render(request, 'login/userregister.html')
                
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect_url = reverse('homepage')
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({'success': True, 'redirect_url': redirect_url})
            else:
                return redirect(redirect_url)
        else:
            err_msg = "Authentication failed after registration!"
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({'success': False, 'error': err_msg})
            else:
                messages.error(request, err_msg)
                return render(request, 'login/userregister.html')
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
            user.profile_image = request.FILES["profile_image"]

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, "login/profile.html", {"user": user})




def dashboard_view(request):
    return render(request, 'dashboard/homepage.html')

def check_username(request):
    username = request.GET.get("username", "").strip()
    exists = Users.objects.filter(username=username).exists()
    return JsonResponse({"exists": exists})

# login(request, user)
# return redirect('homepage')