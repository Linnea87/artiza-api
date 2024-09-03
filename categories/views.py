from django.db.models import Count
from rest_framework import generics, filters
from .models import Category
from .serializers import CategorySerializer


class CategoryList(generics.ListCreateAPIView):
    """
    API view to list all categories.

    Allows filtering by name.
    """
    queryset = Category.objects.annotate(
        posts_count=Count('post', distinct=True)
    ).order_by('-posts_count')
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = [
        'posts_count',
    ]
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.annotate(
        posts_count=Count('post', distinct=True)
    ).order_by('-posts_count')
