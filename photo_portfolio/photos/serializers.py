from rest_framework import serializers
from .models import Photo


# это нужно для сериализации данных из бд и их отображения в виде json
# (для того, чтобы в браузере можно было увидеть данные, которые мы получаем из бд)

# тут можно создать любые дополнительные поля, которые будут отображаться в браузере
class PhotoSerializer(serializers.ModelSerializer):

    # поле для подсчета лайков 
    likes_count = serializers.SerializerMethodField()
    class Meta:
        model = Photo
        fields = ['id', 'image', 'description', 'created_at', 'user_id', 'category_id', 'likes_count']
        read_only_fields = ['user']

    # мы должны создать функцию для подсчета лайков, потому что мы не можем использовать поле в модели (не так просто) 
    def get_likes_count(self, obj):
        return obj.likes.count()