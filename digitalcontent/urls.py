from django.urls import path
from . import views

urlpatterns = [
    path('digital/', views.digital_view, name='digital'),
    path('add/', views.add_digital_content, name='add_digital_content'),
    path('details/<int:content_id>/', views.digital_content_details, name='digital_content_details'),
    path('registered-users/<int:content_id>/', views.registered_users, name='registered_users'),
    path('monitor/<int:content_id>/', views.digital_content_monitor, name='digital_content_monitor'),
    path('update/', views.update_digital_content, name='update_digital_content'),
]