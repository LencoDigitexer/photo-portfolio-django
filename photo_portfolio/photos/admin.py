from django.contrib import admin

# Импортируем модель, которую вы хотите управлять через админку
from .models import Photo

# Зарегистрируйте модель в админке, чтобы можно было управлять фотографиями через админку Django
# Теперь вы можете управлять фотографиями через админку Django
# https://docs.djangoproject.com/en/4.1/ref/contrib/admin/

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'created_at')