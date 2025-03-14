from django.urls import path
from . import views

urlpatterns = [
    path('digital/', views.digital_view, name='digital'),
]