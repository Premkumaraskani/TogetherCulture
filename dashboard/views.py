from django.shortcuts import render
from django.http import JsonResponse

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
    return render(request,'login/userregister.html')
