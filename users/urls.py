from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_view, name='user'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('reject/<int:user_id>/', views.reject_user, name='reject_user'),
]
