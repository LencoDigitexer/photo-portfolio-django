from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Photo, Like
from .serializers import PhotoSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db import IntegrityError


# это класс вьюсета, он принимает на вход класс сериализатора и класс модели, и на выходе дает нам все объекты модели и возможность их изменять через api
# т.е. мы можем посмотреть все картинки и их свойства, добавить новую картинку, удалить картинку, изменить картинку
class PhotoViewSet(viewsets.ModelViewSet):
    # queryset это все объекты модели сортированные по дате создания по убыванию 
    queryset = Photo.objects.all().order_by('-created_at')
    # класс сериализатора для работы с данными модели 
    serializer_class = PhotoSerializer

    # Добавляем поддержку фильтрации
    filter_backends = [DjangoFilterBackend]  
    # Разрешаем фильтрацию по полю id
    filterset_fields = ['id', 'category_id', 'user_id']  


    # Метод для добавления лайка к фотографии
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        photo = self.get_object()
        ip = request.META.get('REMOTE_ADDR')  # Получаем IP-адрес пользователя

        try:
            Like.objects.create(photo=photo, ip_address=ip)
        except IntegrityError:  # Если такой IP уже лайкнул это фото
            return Response(
                {"error": "Вы уже поставили лайк"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(photo)
        return Response(serializer.data, status=status.HTTP_200_OK)