from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class LoginUserTests(APITestCase):

    def setUp(self):

        # CREATE TEST USER :
        self.user = User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='testpassword'
        )
        self.url = reverse('login-user')


    # TEST THE USER LOGIN SUCCESS :
    def test_login_user_success(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    # TEST THE USER LOGIN WITH INVALIDE PASSWORD :
    def test_login_user_invalid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'   # WRONG PASSWORD
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Invalid credentials')

    # TEST THE MISSING FIELD USERNAME OR PASSWORD ;
    def test_login_user_missing_fields(self):
        # missing username :
        data = {
                'username': '', 
                'password': 'testpassword'
                }
        
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

        #  missing password
        data = {'username': 'testuser', 'password': ''}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    # TEST THE USER NOT EXISTS :
    def test_login_user_non_existent_user(self):
        data = {
            'username': 'nonexistentuser',  # User that does not exist
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Invalid credentials')
