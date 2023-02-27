from rest_framework import serializers
from base.models import Item

# Class naming convention: modelSerializer
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'