from django.db.models import Count
from rest_framework import generics, permissions, filters
from artiza_api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category
from .serializers import CategorySerializer


class CategoryList(generics.ListCreateAPIView):
    """
    API view to list all categories.

    Allows filtering by name.
    """
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Category.objects.annotate(
        post_count = Count('post', distinct=True),
    )
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_fields = [
        'name',
    ]
   
    search_fields = [
        'post__title'
        
    ]

    ordering_fields = [
        'post_count',
    ]


class CategoryDetail(generics.RetrieveDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Category.objects.annotate(
        post_count=Count('post', distinct=True)

    )
