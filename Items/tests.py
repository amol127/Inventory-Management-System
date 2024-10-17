from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Item 
from django.contrib.auth import get_user_model

User = get_user_model()

class ItemViewTests(APITestCase):

    def setUp(self):

        # Create a test user and obtain tokens
        self.user = User.objects.create_user(username='testuser',email='test@gmail.com', password='testpassword')
        self.refresh = RefreshToken.for_user(self.user)
        self.access = str(self.refresh.access_token)

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)

    # TEST THE CREATE ITEM :
    def test_create_item(self):
        self.authenticate()
        url = reverse('create-item') 

        data = {'name': 'Test Item', 'description':'test description'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, 'Test Item')

    # TEST THE CHECK ALREADY EXITS ITEM :
    def test_create_existing_item(self):
        self.authenticate()
        Item.objects.create(name='Test Item')
        url = reverse('create-item')

        data = {'name': 'Test Item', 'description':'test description'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Item already exists')

    # TEST GET ITEM 
    def test_get_item(self):
        self.authenticate()
        item = Item.objects.create(name='Test Item')
        url = reverse('item-detail', kwargs={'pk': item.id})  # Adjust based on your urls.py

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response']['name'], 'Test Item')

    def test_get_non_existing_item(self):
        self.authenticate()
        url = reverse('item-detail', kwargs={'pk': 999})  # Non-existing ID

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Item not found')

    def test_update_item(self):
        self.authenticate()
        item = Item.objects.create(name='Test Item')
        url = reverse('item-detail', kwargs={'pk': item.id})

        data = {'name': 'Updated Item'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.name, 'Updated Item')

    def test_update_non_existing_item(self):
        self.authenticate()
        url = reverse('item-detail', kwargs={'pk': 999})  # Non-existing ID

        data = {'name': 'Updated Item'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Item not found')

    def test_delete_item(self):
        self.authenticate()
        item = Item.objects.create(name='Test Item')
        url = reverse('item-detail', kwargs={'pk': item.id})

        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

    def test_delete_non_existing_item(self):
        self.authenticate()
        url = reverse('item-detail', kwargs={'pk': 999})  

        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Item not found')

