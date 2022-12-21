
from unicodedata import name
from django.urls import path

from .import views

urlpatterns = [
    path('signup',views.SignUp.as_view(),name='signup'),
    path('signin',views.Signin.as_view(),name='signin'),
    path('forgetpassword',views.ForgotPassword.as_view(),name='forgetpassword'),
    path('otp',views.OTP.as_view(),name='otp'),
    path('profile',views.Profile.as_view(),name='profile'),
    path('editProfile',views.EditProfile.as_view(),name='editprofile'),
    path('profileupload',views.ProfileUpload.as_view(),name='profileupload'),
    

    path('logout',views.Logout.as_view(),name='logout'),


    # path('ForgotPassword',views.ForgotPassword.as_view(),name='ForgotPassword'),


]
