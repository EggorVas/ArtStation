from django.conf import settings
from django.db import models
from django.utils import timezone


class Art(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=150)
    author = models.CharField('Автор', max_length=150)
    image = models.ImageField('Картина', upload_to='images/')
    description = models.TextField('Описание')

    sortingChoices = (
        ('-published_date', 'дате публикации (сначала поздние)'),
        ('published_date', 'дате публикации (сначала ранние)'),
        ('name', 'названию (а-я)'),
        ('-name', 'названию (я-а)'),
        ('author', 'автору (а-я)'),
        ('-author', 'автору (я-а)'),
    )

    styleChoices = (
        ('REN', 'Ренессанс'),
        ('MAN', 'Маньеризм'),
        ('BAR', 'Барокко'),
        ('CLA', 'Классицизм'),
        ('ROM', 'Романтизм'),
        ('IMP', 'Импрессионизм'),
        ('EXP', 'Экспрессионизм'),
        ('AVA', 'Авангард'),
        ('OTH', 'Другой'),
    )
    style = models.CharField('Стиль', max_length=3, choices=styleChoices, default='OTH')

    genreChoices = (
        ('POR', 'Портрет'),
        ('PEI', 'Пейзаж'),
        ('MAR', 'Марина'),
        ('IST', 'Исторический'),
        ('BAT', 'Батальный'),
        ('ANI', 'Анималистика'),
        ('BIT', 'Бытовой'),
        ('NAT', 'Натюрморт'),
        ('ARH', 'Архитектурный'),
        ('NU', 'Жанр Ню'),
        ('OTH', 'Другой'),
    )
    genre = models.CharField('Жанр', max_length=3, choices=genreChoices, default='OTH')

    techniqueChoices = (
        ('MAS', 'Масляная'),
        ('AKR', 'Акриловая'),
        ('AKV', 'Акварель'),
        ('TEM', 'Темпера'),
        ('GUA', 'Гуашь'),
        ('TUS', 'Тушь'),
        ('PAS', 'Пастель'),
        ('ANC', 'Энкаустика'),
        ('AER', 'Аэрография'),
        ('SME', 'Смешанная'),
        ('OTH', 'Другая'),
    )
    technique = models.CharField('Техника', max_length=3, choices=techniqueChoices, default='OTH')

    published_date = models.DateField('Дата публикации', default=timezone.now)

    def __str__(self):
        return '{0} - {1}'.format(self.name, self.author)


class Liked_art(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    art_id = models.ForeignKey(Art, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} - {1}'.format(self.user_id, self.art_id.name)
