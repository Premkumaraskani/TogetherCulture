from django.shortcuts import render

from django.http import JsonResponse


def dashboard_view(request):
    return render(request, 'dashboard/homepage.html')



def homepage_view(request):
    return render(request, 'dashboard/homepage.html')

