from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logged_out.html'), name='logout'),
path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='account/profile.html',
            success_url=reverse_lazy('password_change_done')
        ),
        name='password_change'
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='account/password_change_done.html'  # <--- YOUR CUSTOM TEMPLATE
        ),
        name='password_change_done'
    ),
    # reset password urls
   path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='account/password_reset_form.html'),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password_reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),
    path('register/', views.UserRegistration.as_view(), name='register'),
    path('verify/', views.VerifyOTP.as_view(), name='verify'),
    
    path('register-page/', views.register_page, name='register-page'),
    path('verify-page/', views.verify_page, name='verify-page'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('properties/', views.properties, name='properties'),
    
    
]
