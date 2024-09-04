from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryList, CategoryDetail

router = DefaultRouter()

urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('categories/<int:pk>/', CategoryDetail.as_view()),
    path('api/', include(router.urls)),
]
