from django.shortcuts import render

# Create your views here.
def digital_view(request):
    return render(request, 'digital.html')
