from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']


class CategoryDetailSerializer(CategorySerializer):
    category_id = serializers.ReadOnlyField(source='id')

    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at', 'category_id']
