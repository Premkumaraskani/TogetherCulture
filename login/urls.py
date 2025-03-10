from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='loginpage'),
    path('userregister/', views.userregister_view, name='userregister'),
    # new code added
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('homepage/', views.dashboard_view, name='homepage'),
    path('check_username/', views.check_username, name='check_username'),
]

