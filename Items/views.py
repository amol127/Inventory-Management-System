
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import Item
from .serializers import ItemSerializer

from rest_framework.permissions import IsAuthenticated

# Get the logger for your app
logger = logging.getLogger('items')




class ItemView(APIView):
    permission_classes = [IsAuthenticated]
    
    # CREATE ITEM
    def post(self, request):
        try:
            data = request.data
            item_name = data.get('name')

            # Check if item already exists
            if Item.objects.filter(name=item_name).exists():
                logger.warning(f"Item '{item_name}' already exists.")
                return Response({'error': 'Item already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate serializer and save
            serializer = ItemSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Created item: {serializer.data}")
                
                # Clear cache after creating item
                cache.delete('items_list')
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            logger.error(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error occurred while creating item: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # SEARCH (READ) ITEM
    def get(self, request, pk=None):
        try:
            if pk:  # If item ID is provided, fetch a specific item
                cache_key = f'item_{pk}'
                cached_item = cache.get(cache_key)
                
                # Check if item is in cache
                if cached_item:
                    logger.debug(f"Cache hit for item {pk}")
                    return Response({"cache": cached_item}, status=status.HTTP_200_OK)
                
                # Fetch from database if not in cache
                item = Item.objects.get(id=pk)
                serializer = ItemSerializer(item)
                
                # Cache the item after fetching from the database
                cache.set(cache_key, serializer.data, timeout=60 * 15)  # Cache for 15 minutes
                logger.info(f"Fetched item from database: {serializer.data}")
                return Response({"response": serializer.data}, status=status.HTTP_200_OK)
            else:
                logger.warning("Item ID not provided.")
                return Response({"error": "Item ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Item.DoesNotExist:
            logger.warning(f"Item with id {pk} not found.")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error occurred while retrieving item: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # UPDATE ITEM
    def put(self, request, pk=None):
        try:
            if pk:  # Ensure item ID is provided
                item = Item.objects.get(id=pk)
                serializer = ItemSerializer(item, data=request.data, partial=True)
                
                if serializer.is_valid():
                    serializer.save()
                    logger.info(f"Updated item {pk}: {serializer.data}")
                    
                    # Update cache for the updated item
                    cache.set(f'item_{pk}', serializer.data, timeout=60 * 15)
                    return Response(serializer.data, status=status.HTTP_200_OK)

                logger.error(f"Serializer errors while updating item {pk}: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            logger.warning("Item ID not provided for update.")
            return Response({"error": "Item ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Item.DoesNotExist:
            logger.warning(f"Item with id {pk} not found for update.")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error occurred while updating item {pk}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DELETE ITEM
    def delete(self, request, pk=None):
        try:
            if pk:  # Ensure item ID is provided
                item = Item.objects.get(id=pk)
                item.delete()
                logger.info(f"Deleted item {pk}")

                # Clear cache for the deleted item
                cache.delete(f'item_{pk}')
                return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

            logger.warning("Item ID not provided for deletion.")
            return Response({"error": "Item ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Item.DoesNotExist:
            logger.warning(f"Item with id {pk} not found for deletion.")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error occurred while deleting item {pk}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
