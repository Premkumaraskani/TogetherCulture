from django.shortcuts import render

# Create your views here.
def membership_view(request):
    return render(request,'membership.html')