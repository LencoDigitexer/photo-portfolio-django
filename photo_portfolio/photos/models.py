from django.db import models



class Photo(models.Model):
    # куда будет сохраняться фото
    image = models.ImageField(upload_to='photos/')
    # комментарий к фото
    description = models.TextField(blank=True)
    # время создания фото
    created_at = models.DateTimeField(auto_now_add=True)
    # кто создал фото
    user_id = models.IntegerField(default=0)
    # категория фото
    category_id = models.IntegerField(default=0)
    



    # имя фото будет равно имени, которое задано при создании объекта
    def __str__(self):
        return f"Photo {self.id}"
    

    # количество лайков
    @property
    def likes_count(self):
        return self.likes.count()
    
# Модель лайка для фотографии 
class Like(models.Model):
    # фото к которому будет привязан лайк
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes')
    # IP адрес пользователя, который поставил лайк
    ip_address = models.GenericIPAddressField()
    # время создания лайка
    created_at = models.DateTimeField(auto_now_add=True)

    # Мета-класс для модели Like который определяет, что каждый пользователь может поставить лайк только один раз для каждой фотографии. 
    # Это предотвращает дублирование лайков от одного и того же пользователя.
    class Meta:
        unique_together = ('photo', 'ip_address')  # Один IP = один лайк на фото
    

# При изменении этого файла нужно выполнить команду:
# python manage.py makemigrations 
# python manage.py migrate