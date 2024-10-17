
from django.urls import path, include

from .views import ItemView
urlpatterns = [   

    path('items/',      ItemView.as_view(), name = 'create-item'),    # for Create items 
    path('items/<pk>/', ItemView.as_view(), name = 'item-detail'),    # SEARCH , UPDATE , DELETE ITEMS  
]
