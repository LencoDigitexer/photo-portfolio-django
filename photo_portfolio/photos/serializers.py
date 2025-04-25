from rest_framework import serializers
from .models import Photo
from .models import UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Кастомный сериализатор для добавления имени и фамилии в JWT-ответ.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Безопасное получение профиля
        profile = getattr(user, 'profile', None)
        avatar_url = profile.avatar.url if profile and profile.avatar else None

        # Добавляем дополнительные поля в токен
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['avatar'] = avatar_url

        return token

    def validate(self, attrs):
        # Получаем стандартные данные токена
        data = super().validate(attrs)

        profile = getattr(self.user, 'profile', None)
        avatar_url = profile.avatar.url if profile and profile.avatar else None

        # Добавляем имя и фамилию в ответ
        data['username'] = self.user.username
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['avatar'] = avatar_url

        return data


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