# auth/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
import logging

logger = logging.getLogger('Auth')


# USER REGISTER 
# RESQUEST  :   username , email, password
class RegisterUser(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"User {request.data['username']} registered successfully.")
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        logger.error(f"Registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# USER LOGIN ()
# username : username,
# password : password
# response is refresh tokon and access token :
class LoginUser(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                logger.info(f"User {username} logged in successfully.")
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                logger.warning(f"Login failed for user {username}.")
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        logger.error(f"Login validation error: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET NEW ACCESS TOKEN :
# request the refreshtoken then respobse access token :
class RetrieveToken(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            logger.info("Access token refreshed successfully.")
            return Response({'access': access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Token refresh error: {str(e)}")
            return Response({'error': 'Token is invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)
