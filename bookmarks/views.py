from rest_framework import generics, permissions
from artiza_api.permissions import IsOwnerOrReadOnly
from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer


# based off of Likes views provided by DRF-API walkthrough.
class BookmarkList(generics.ListCreateAPIView):
    """
    View all bookmarked posts.
    bookmark a post if logged in.
    Permission already set globally in settings.py
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookmarkDetail(generics.RetrieveDestroyAPIView):
    # Retrieve/delete a bookmarked post if it is your bookmark.
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()