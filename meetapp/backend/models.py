from django.db import models
from django.contrib.auth.models import AbstractUser


class Language(models.Model):
    name = models.CharField(max_length=30, verbose_name='Язык')

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'


class Tag(models.Model):
    name = models.CharField(max_length=40, verbose_name='Тег')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Image(models.Model):
    url = models.TextField(verbose_name='URL изображения')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
    

class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index = True, verbose_name = 'Прощёл активацию?')
    send_messages = models.BooleanField(default = True, verbose_name = 'Уведомлять о сообщениях?')

    def delete(self, *args, **kwargs):
        for item in self.item_set.all():
            item.delete()
        super().delete(*args, **kwargs)
    

class Profile(models.Model):
    name = models.CharField(max_length=20, blank=False, verbose_name='Твое имя')
    age = models.IntegerField(db_index = True, blank=False, verbose_name = 'Возраст')
    city = models.CharField(max_length=168, db_index = True, blank=False, verbose_name='Город')
    description = models.TextField(blank=True, null=True, verbose_name='Расскажи о себе')
    gender = models.CharField(max_length=10, db_index=True, blank=False, verbose_name='Пол')
    children = models.CharField(max_length=4, blank=True, null=True, verbose_name='У тебя есть дети?')
    education = models.CharField(max_length=150, blank=True, null=True, verbose_name='Образование')
    profession = models.CharField(max_length=50, blank=True, null=True, verbose_name='Должность на работе')
    languages = models.ManyToManyField(Language, through='LanguageProfile', verbose_name='Языки')
    tags = models.ManyToManyField(Tag, through='TagProfile', verbose_name='Теги')
    images = models.ManyToManyField(Image, through='ImageProfile', verbose_name='Фото')
    alcohol = models.CharField(max_length=30, verbose_name='Алкоголь', blank=True, null=True,)
    smoke = models.CharField(verbose_name='Курение', blank=True, null=True,)
    horoscope = models.CharField(max_length=25, blank=True, null=True, verbose_name='Знак зодиака')
    target = models.CharField(max_length=35, blank=True, null=True, verbose_name='Цель')
    #isOnline
    #last_online

    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'


class LanguageProfile(models.Model):
    language = models.ForeignKey(Language, on_delete=models.RESTRICT, verbose_name='Язык')
    profile = models.ForeignKey(Profile, on_delete=models.RESTRICT, verbose_name='Анкета пользователя')

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'


class TagProfile(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.RESTRICT, verbose_name='Тег')
    profile = models.ForeignKey(Profile, on_delete=models.RESTRICT, verbose_name='Анкета пользователя')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class ImageProfile(models.Model):
    image = models.ForeignKey(Image, on_delete=models.RESTRICT, verbose_name='Фото')
    profile = models.ForeignKey(Profile, on_delete=models.RESTRICT, verbose_name='Анкета пользователя')
    
