from rest_framework import serializers
from .models import Photo


# это нужно для сериализации данных из бд и их отображения в виде json
# (для того, чтобы в браузере можно было увидеть данные, которые мы получаем из бд)

# тут можно создать любые дополнительные поля, которые будут отображаться в браузере
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'description', 'created_at', 'user_id', 'category_id', 'likes_count']