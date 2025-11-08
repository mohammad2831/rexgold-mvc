from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.SignupGenerateOTPView.as_view(), name='signup'),
    path('login', views.LoginGenerateOTPView.as_view(), name='login'),
    path('verify/lgoin/', views.VerifyOTPView.as_view(), name='verify-login-otp'),
    path('verify/signup/', views.SignupVerifyOtpView.as_view(), name='verify-signup-otp'),
    path('refreshToken', views.RefreshAccessTokenView.as_view(), name='refresh-token'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

]