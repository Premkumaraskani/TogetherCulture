from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='loginpage'),
    path('register/', views.userregister_view, name='userregister'),
]
