from django.conf import settings
from django.db import models
from django.utils import timezone


class Art(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=150)
    author = models.CharField('Автор', max_length=150)
    image = models.ImageField('Картина', upload_to='images/')
    description = models.TextField('Описание')
    kind = models.CharField('Разновидность', max_length=50)
    published_date = models.DateField('Дата публикации', default=timezone.now)

    def __str__(self):
        return self.name


class Liked_art(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    art_id = models.ForeignKey(Art, on_delete=models.CASCADE)

    def __str__(self):
        return self.art_id
