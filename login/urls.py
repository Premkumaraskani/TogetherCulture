from django.urls import path
from . import views
# from dashboard import views as login_views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.dashboard_view, name='homepage'),
    path('login/', views.login_view, name='loginpage'),
    # path(
    #     'login/',
    #     LoginView.as_view(
    #         template_name='login/loginpage.html',
    #         redirect_authenticated_user=True
    #     ),
    #     name='loginpage'
    # ),
    path('userregister/', views.userregister_view, name='userregister'),
    path('check_username/', views.check_username, name='check_username'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # path('', views.login_view, name='loginpage'),
    # path('register/', views.userregister_view, name='userregister'),
    # path('logout/', views.logout_view, name='logout'),
    # path('profile/', views.profile_view, name='profile'),
    # path('check_username/', views.check_username, name='check_username'),
]

