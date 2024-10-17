# Inventory-Management-System



# Table of Contents
    # Introduction
    # Features
    # Requirements
    # Installation
    # Setup Instructions
    # API Documentation
    # Usage Examples
    # Testing
    # Contributing
    # License


# Introduction
    The Inventory Management System is a web application designed to help businesses manage their inventory efficiently. It provides features for adding, updating, and deleting inventory items, as well as tracking stock levels and generating reports. This application is suitable for small to medium-sized businesses looking to streamline their inventory processes.



# Features
    # User registration and authentication
    # CRUD (Create, Read, Update, Delete) operations for inventory items
    # Token-based authentication using JWT (JSON Web Tokens)
    # API endpoints for interacting with the inventory
    # Detailed logging for user activities


# Requirements
    Python 3.x
    Django 3.x or above
    Django REST Framework
    Django Simple JWT
    Other necessary libraries as listed in requirements.txt


# Installation
   # Clone the repository:
        git clone https://github.com/username/inventory-management-system.git
        cd inventory-management-system
    
   # Create a virtual environment (if needed) :
        python -m venv env
        env\Scripts\activate

   # Install the requirements:
        pip install -r requirements.txt

   # Apply migrations:
        python manage.py migrate

   # Run the development server
        python manage.py runserver

# Setup Instructions ;

   # Database Configuration:
        Configure your database settings in settings.py. For MY-SQL, ensure you have the necessary credentials.

   # Environment Variables: 
        Set the following environment variables in your .env file or directly in your environment:
        SECRET_KEY    : Your Django secret key
        DEBUG         : Set to True for development, False for production
        ALLOWED_HOSTS : List of hosts/domain names that your Django site can serve

##  
## API Documentation

# Authentication :

   # Register User :
        # Endpoint : /v1/auth/register/
        # Method : POST
        # Request Body:
                {
                    "username": "testuser",
                    "email": "test@gmail.com",
                    "password": "testpassword"
                }

        # Response :
                Status: 201 Created
                {
                    "message": "User registered successfully"
                }

   # Login User :
        # Endpoint : /v1/auth/login/
        # Method : POST
        # Request Body:
                {
                    "username": "testuser",
                    "password": "testpassword"
                }

        # Response :
                Status: 200 OK

                {
                    "refresh": "refresh_token_here",
                    "access": "access_token_here"
                }


   # Inventory Add items :

        # Endpoint : /v1/store/items/
        # Method : POST
        # Request Body :
                {
                    "name": "New Item",
                    "description": "Item description"
                }

        # Response:
                Status: 201 Created
                {
                    "id": 1,
                    "name": "New Item",
                    "description": "Item description"
                }


   # Inventory Get items :
   
        # Endpoint: /v1/items/{id}/
        # Method: GET
        # URL Parameters:
        # id: The ID of the item to be deleted (e.g., 1 for the item with ID 1).
        
        # Response:
            Status: 204 No Content
            Body: (No content returned)

        Error Response:
        If the item does not exist:
        Status: 404 Not Found
        Body:

        {
            "error": "Item not found"
        }


    
   # Delete Item
        # Endpoint: /v1/items/{id}/
        # Method: DELETE
        # URL Parameters:
        # id: The ID of the item to be deleted (e.g., 1 for the item with ID 1).
        
        # Response:
            Status: 204 No Content
            Body: (No content returned)

        Error Response:
        If the item does not exist:
        Status: 404 Not Found
        Body:

        {
            "error": "Item not found"
        }

# Testing

    python manage.py test






