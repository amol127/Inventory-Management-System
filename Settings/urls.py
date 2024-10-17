
from django.urls import path, include

urlpatterns = [

    path('v1/auth/',  include('Auth.urls')) ,  # Base path of Auth (user login all api )  
    path('v1/store/', include('Items.urls'))   # Base path of Items (ALL CURD OPERATION)
]
