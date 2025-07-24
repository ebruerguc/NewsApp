from django.urls import path
from . import views
from .views import SignUpView, CustomPasswordChangeView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),

    path('login/', auth_views.LoginView.as_view(), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'), name='logout'),

    #password_change path

    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/',
     auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
     name='password_change_done'),
    
    #password_reset path

    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), 
         name='password_reset'),

    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
     auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
     name='password_reset_confirm'),

    path('reset/done/', 
     auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
     name='password_reset_complete'),
]

