from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import JsonResponse
from .forms import UserRegisterForm
# Create your views here.
def dashboard_view(request):
    return render(request, 'dashboard/homepage.html')

def login_view(request):
    if request.method == 'POST':
        loginid = request.POST.get('loginid')
        password = request.POST.get('password')
        print(f"Login ID: {loginid}, Password: {password}")
        return JsonResponse({'message': 'Login successful'})
    return render(request, 'login/loginpage.html')

def userregister_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = user.username
            return redirect(reverse('homepage') + f'?username={username}')
    else:
        form = UserRegisterForm()
    return render(request, 'login/userregister.html', {'form': form})