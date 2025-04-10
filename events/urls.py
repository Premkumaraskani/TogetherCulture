from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.events_view, name='events'),
    path("add-event/", views.add_event, name="add_event"),
    path('register-event/', views.register_event, name='register_event'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
]
