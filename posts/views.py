from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from artiza_api.permissions import IsOwnerOrReadOnly
from .models import Post
from categories.models import Category
from bookmarks.models import Bookmark
from .serializers import PostSerializer



class PostList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in
    The perform_create method associates the post with the logged in user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True),
        bookmarks_count=Count('bookmarks', distinct=True)
    )

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__profile',
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'bookmarks__owner__profile',
        'category_id',  
        'category',      
    ]
    search_fields = [
        'owner__username',
        'title',
        'content',
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at',
    ]

    def perform_create(self, serializer):
        # Post creation, associates owner with current user
        serializer.save(owner=self.request.user)
 

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True),
        bookmarks_count=Count('bookmarks', distinct=True),
    )
