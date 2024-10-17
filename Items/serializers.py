from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'description']

    # CREATE METHODS AUTOMATICALLY HADLLE OTHERWISE OVERRIDES
    def create(self, validated_data):
        return Item.objects.create(**validated_data)