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
