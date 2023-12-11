from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils import timezone
from django.core.cache import cache


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index = True, verbose_name = 'Прощёл активацию?')
    send_messages = models.BooleanField(default = True, verbose_name = 'Уведомлять о сообщениях?')
    CHOICES = (
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
    )
    gender = models.CharField(max_length=7, choices=CHOICES, default='Женщина')

    last_online = models.DateTimeField(blank=True, null=True, verbose_name='Последний онлайн')

    def is_online(self):
        if self.last_online:
            return (timezone.now() - self.last_online) < timezone.timedelta(minutes=15)
        return False

    def get_online_info(self):
        if self.is_online():
    
            return ('Online')
        if self.last_online:
        
            return ('Last visit {}').format(naturaltime(self.last_online))
            
        return ('Unknown')

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=30, verbose_name='Язык')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'


class Tag(models.Model):
    name = models.CharField(max_length=40, verbose_name='Тег')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Profile(models.Model):
    CHOICES = (
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
    )
    name = models.CharField(max_length=20, blank=False, verbose_name='Имя')
    age = models.IntegerField(db_index = True, blank=False, verbose_name = 'Возраст')
    city = models.CharField(max_length=168, db_index = True, blank=False, verbose_name='Город')
    description = models.TextField(blank=True, null=True, verbose_name='Расскажи о себе')
    gender = models.CharField(max_length=7, db_index=True, blank=False, verbose_name='Пол', choices=CHOICES)
    children = models.CharField(max_length=4, blank=True, null=True, verbose_name='Дети')
    education = models.CharField(max_length=150, blank=True, null=True, verbose_name='Образование')
    profession = models.CharField(max_length=50, blank=True, null=True, verbose_name='Работа')
    languages = models.ManyToManyField(Language, blank=False, through='LanguageProfile', verbose_name='Языки')
    tags = models.ManyToManyField(Tag, through='TagProfile', verbose_name='Интересы')
    images = models.TextField(verbose_name= 'url фото', blank=False, null=False, default=' ')
    alcohol = models.CharField(max_length=30, verbose_name='Алкоголь', blank=True, null=True,)
    smoke = models.CharField(verbose_name='Курение', blank=True, null=True,)
    horoscope = models.CharField(max_length=25, blank=True, null=True, verbose_name='Знак зодиака')
    target = models.CharField(max_length=35, blank=True, null=True, verbose_name='Цель')
    advuser = models.OneToOneField(AdvUser, blank=True, on_delete= models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.name


    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'

class LanguageProfile(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='Язык')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Анкета пользователя')

    class Meta:
        verbose_name = 'ЯзыкАнкета'
        verbose_name_plural = 'ЯзыкиАнкеты'


class TagProfile(models.Model):
    tag = models.ForeignKey(Tag, on_delete= models.CASCADE, verbose_name='Тег')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Анкета пользователя')

    class Meta:
        verbose_name = 'ТегАнкета'
        verbose_name_plural = 'ТегиАнкеты'


class Match(models.Model):
    giveLikeUser = models.ForeignKey(AdvUser, on_delete=models.CASCADE, related_name='likedProfilesGive', verbose_name='Поставивший лайк')
    getLikeUser = models.ForeignKey(AdvUser, on_delete=models.CASCADE, related_name='likedProfilesGet',  verbose_name='Получивший лайк')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class userProfile(models.Model):
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Анкета пользователя')

    class Meta:
        verbose_name = 'ПользовательАнкета'
        verbose_name_plural = 'ПользователиАнкеты'
