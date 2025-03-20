from django.urls import path
from . import views

urlpatterns = [
    path('membership/', views.membership_view, name='membership'),
    path('save-membership-application/', views.save_membership_application, name='save_membership_application'),
]