from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PhotoViewSet
from .views import  UserProfileView  # добавляем маршрут для получения профиля пользователя


router = DefaultRouter()

# это нужно для создания CRUD операций над фото
# CRUD = Create, Read, Update, Delete
router.register(r'photos', PhotoViewSet)

# подключаем эти маршруты к нашим урлам
urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]

urlpatterns += [
    path('user/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
]