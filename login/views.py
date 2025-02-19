from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User 
from django.shortcuts import redirect
from django.http import JsonResponse
import json
from .models import Users

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        loginid = request.POST.get('loginid')
        password = request.POST.get('password')
        print("Login ID and Password: "+loginid+" : "+password)
        user = authenticate(request, username=loginid, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login/loginpage.html', {'error': 'Invalid credentials'})
    
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
        print(f"User Details: {first_name} : {last_name} : {username} : {password} : {email} : {phoneno} : {status} : {interests}")
        user = Users(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
            phone=phoneno,
            status=status,
            interests=interests
        )
        user.save()
        return JsonResponse({'message': 'Registered Successfully'})
    return render(request, 'login/userregister.html')