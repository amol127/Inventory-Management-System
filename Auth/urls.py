from django.urls import path
from .views import RegisterUser, LoginUser, RetrieveToken

urlpatterns = [
    path('register/', RegisterUser.as_view(),  name = 'register-user'),  # User Register 
    path('login/',    LoginUser.as_view(),     name = 'login-user'),     # User Login 
    path('token/',    RetrieveToken.as_view(), name = 'retrieve-token'), # User Token retrive
]
