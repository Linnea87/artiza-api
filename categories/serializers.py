from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
 
    def get_posts_count(self, obj):
        return obj.post_set.count()

    class Meta:
        model = Category
        fields = [
            'id', 
            'name', 
            'created_at', 
            'posts_count'
        ]


# class CategorySerializer(serializers.ModelSerializer):
#     """Serializes Category model (id, name, created_at) for API.
#     """
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'created_at']


# class CategoryDetailSerializer(CategorySerializer):
#     """
#     Serializer for the Comment model used in Detail view
#     Post is a read only field so that we dont have
#     to set it on each update
#     """
#     category_id = serializers.ReadOnlyField(source='id')

#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'created_at', 'category_id']