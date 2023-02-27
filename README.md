Installing Django, DRF, and initializing the project/apps

pip install django
pip install djangorestframework
django-admin startproject drf
django-admin startapp base
django-admin startapp api

The base app is where models will be defined

The api app is where the serializers and API endpoints will be defined

Go to settings.py and under INSTALLED_APPS add

    'base.apps.BaseConfig',
    'api.apps.ApiConfig',
    'rest_framework',

Go to base/models.py and add

    from django.db import models

    class Item(models.Model):
        name = models.CharField(max_length=200)
        created = models.DateTimeField(auto_now_add=True)

Go to base/admin.py and add

    from .models import Item
    admin.site.register(Item)

Create a super user using the console

    python3 manage.py createsuperuser
    username:       admin
    email address:  admin@something.com
    password:       pass

The last two code snippets are what allows for the use of the admin console to create, update, and delete records in the  Item table. Sign into the admin console and create a few records for testing purposes.

The api/view.py file is where the API will be defined. Each API endpoint will return a Response object which comes from rest_framework.response. The Response object cannot natively handle Django model instances. Therefore, Django model instance data must first be serialized before it can be rendered by Response. Below we create a serializer for the Item model which will convert instances of our Items from objects to into a data type the response object can understand.

Create api/serializers.py and add

    from rest_framework import serializers
    from base.models import Item

    class ItemSerializer(serializers.ModelSerializer):
        class Meta:
            model = Item
            fields = '__all__'

Above, the class name is arbitrary but a good convention is “modelSerializer”

Go to api/views.py and add

    from rest_framework.response import Response
    from rest_framework.decorators import api_view
    from base.models import Item
    from .serializers import ItemSerializer

    @api_view(['GET'])
    def getData(request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

many=True tells the serializer that more than one item will be serialized; many=False would limit to 1 item

The Response object returned above is what takes Python dictionaries (or already serialized data) and renders it as JSON.

Create api/urls.py and add

    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.getData),
    ]

Go to the project’s urls.py and add a path to  api/urls.py

    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('api.urls')),
    ]

Using the console, migrate the changes and run the server

    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py runserver

Going to http://127.0.0.1:8000/ will execute getData(request). This function-based API view retrieves and displays all the records and their fields from the Item table.

Next, create an endpoint to facilitate POST requests. Go back to api/views.py and add

    @api_view(['POST'])
    def addItem(request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    Update api/urls.py to include path('add/', views.addItem)

Going to http://127.0.0.1:8000/add/ will display the UI to submit a POST request. Try it (remember that “name” was defined as a character field in the Item model)