from django.urls import path
from .views import BookmarkList, BookmarkDetail


urlpatterns = [
    path('bookmarks/', BookmarkList.as_view()),
    path('bookmarks/<int:pk>/', BookmarkDetail.as_view()),
]