from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PhotoViewSet

router = DefaultRouter()

# это нужно для создания CRUD операций над фото
# CRUD = Create, Read, Update, Delete
router.register(r'photos', PhotoViewSet)

# подключаем эти маршруты к нашим урлам
urlpatterns = [
    path('', include(router.urls)),
]