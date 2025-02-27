from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='loginpage'),
    path('userregister/', views.userregister_view, name='userregister'),
]

