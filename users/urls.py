from django.urls import path
from . import views
from .views import SignUpView, CustomPasswordChangeView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),

    path('login/', auth_views.LoginView.as_view(), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'), name='logout'),
    
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
]
