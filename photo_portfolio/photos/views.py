from django.shortcuts import render                                 # импортируем функцию для отображения страницы
from rest_framework.decorators import action                        # импортируем функцию для работы с действиями вьюсета
from rest_framework.response import Response                        # импортируем класс для работы с ответами в формате json
from rest_framework import viewsets, status                         # импортируем класс для работы с вьюсетами и статусами ответов
from rest_framework.views import APIView                            # импортируем класс для работы с вью в формате json     
from rest_framework.parsers import MultiPartParser, FormParser      # импортируем классы для работы с файлами и формами
from .models import Photo, Like                                     # импортируем модели из приложения
from .models import UserProfile                                     # импортируем класс модели пользователя  
from .serializers import UserProfileSerializer                      # импортируем класс сериализатора для работы с данными модели
from .serializers import PhotoSerializer                            # импортируем класс сериализатора для работы с данными модели
from .permissions import ReadOnlyOrIsAuthenticatedAndInGroup        # импортируем класс разрешений для работы с вьюсетом
from django_filters.rest_framework import DjangoFilterBackend       # импортируем класс для работы с фильтрацией
from django.db import IntegrityError                                # импортируем класс для работы с исключениями
from rest_framework.permissions import BasePermission               # импортируем класс базового разрешения для работы с вьюсетом
from rest_framework.permissions import IsAuthenticated              # импортируем класс разрешений для работы с вьюсетом


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class IsPhotographerOrArtist(BasePermission):
    """
    Разрешение: только пользователи из групп Photographer или Artist могут создавать фото.
    """
    def has_permission(self, request, view):
        return (
            request.user.groups.filter(name='Photographer').exists() or
            request.user.groups.filter(name='Artist').exists()
        )


# это класс вьюсета, он принимает на вход класс сериализатора и класс модели, и на выходе дает нам все объекты модели и возможность их изменять через api
# т.е. мы можем посмотреть все картинки и их свойства, добавить новую картинку, удалить картинку, изменить картинку
class PhotoViewSet(viewsets.ModelViewSet):
    # queryset это все объекты модели сортированные по дате создания по убыванию 
    queryset = Photo.objects.all().order_by('-created_at')
    # класс сериализатора для работы с данными модели 
    serializer_class = PhotoSerializer

    # Делаем так, чтобы только пользователи с правами фотографа или художника могли создавать фотографии
    permission_classes = [ReadOnlyOrIsAuthenticatedAndInGroup]

    def perform_create(self, serializer):
        """
        Автоматически привязываем фото к текущему пользователю.
        """
        serializer.save(user=self.request.user)

    # Добавляем поддержку фильтрации
    filter_backends = [DjangoFilterBackend]  
    # Разрешаем фильтрацию по полю id
    filterset_fields = ['id', 'category_id', 'user_id']  


    # Метод для добавления лайка к фотографии
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        photo = self.get_object()
        ip = request.META.get('REMOTE_ADDR')

        # Проверяем, существует ли лайк
        try:
            like = Like.objects.get(photo=photo, ip_address=ip)
            like.delete()  # Удаляем лайк, если он уже есть
            message = "Лайк удален"
        except Like.DoesNotExist:
            Like.objects.create(photo=photo, ip_address=ip)  # Создаем новый лайк
            message = "Лайк добавлен"

        # Возвращаем обновленные данные
        serializer = self.get_serializer(photo)
        return Response({
            "status": message,
            "photo": serializer.data
        }, status=status.HTTP_200_OK)