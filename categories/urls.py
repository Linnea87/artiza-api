from django.urls import path, include
from rest_framework.routers import DefaultRouter
from categories import views


router = DefaultRouter()


urlpatterns = [
    path('categories/', views.CategoryList.as_view()),
    path('categories/<int:pk>/', views.CategoryDetail.as_view()),
    path('api/', include(router.urls)),
]
