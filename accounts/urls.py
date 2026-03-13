from django.urls import path
from . import views
from django.contrib.auth import views as auth_views





urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('userupdateinfo/', views.userupdateinfo, name='userupdateinfo'),
    path('changepassword/', views.userchangepassword, name='changepassword'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/verify/', views.password_reset_verify, name='password_reset_verify'),
    path('password-reset/confirm/', views.password_reset_confirm_otp, name='password_reset_confirm_otp'),
    path('verify-otp/', views.verify_email_otp, name='verify_email_otp'),
    path('verify-done/', views.verify_email_done, name='verify_email_done'),
    path('settings/', views.account_settings, name='account_settings'),
    path('delete-account/', views.delete_account, name='delete_account'),
]