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
    # количество лайков
    likes_count = models.IntegerField(default=0)


    # имя фото будет равно имени, которое задано при создании объекта
    def __str__(self):
        return f"Photo {self.id}"
    

# При изменении этого файла нужно выполнить команду:
# python manage.py makemigrations 
# python manage.py migrate