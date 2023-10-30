from django import forms

from .models import Profile

class CreateProfileForm(forms.ModelForm):
    GENDERS = (('male', 'Мужчина'), ('female', 'Женщина'))
    CHILDREN = (('true', 'Есть'), ('false', 'Нет'))
    ALCHOHOL = (('withCompany', 'За компанию'), ('never', 'Никогда'), ('often', 'Часто'), ('abstain', 'Воздерживаюсь'), ('noAnswer', 'Предпочитаю не отвечать'))
    SMOKE = (('yes', 'Да'), ('no', 'Нет'), ('sometimes', 'Иногда'), ('noAnswer', 'Предпочитаю не отвечать'))
    HOROSCOPE = (('aries', 'Овен'), ('taurus', 'Телец'), ('gemini', 'Близнецы'), ('cancer', 'Рак'), \
                 ('leo', 'Лев'), ('virgo', 'Дева'), ('libra', 'Весы'), ('scorpio', 'Скорпион'), \
                 ('sagittarius', 'Стрелец'), ('capricorn', 'Козерог'), ('aquarius', 'Водолей'), \
                 ('pisces', 'Рыбы'), ('noAnswer', 'Предпочитаю не отвечать'))
    TARGET = (('dating', 'Ходить на свидания'), ('communication', 'Просто общаться'), ('findLove', 'Найти любовь'))
    name = forms.CharField(label='Имя')
    age = forms.IntegerField(label='Возраст', min_value=18)
    city = forms.CharField(label='Город')
    description = forms.Textarea()
    gender = forms.ChoiceField(label='Пол',choices=GENDERS)
    children = forms.ChoiceField(label='Есть дети?',choices=CHILDREN)
    education = forms.CharField(label='Образование')
    profession = forms.CharField(label='Работа')
    languages = forms.CharField(label='Языки')
    tags = forms.CharField(label='Мои интересы')
    image = forms.CharField(label='Мое фото url') #Передалть на ImageField
    alcohol = forms.ChoiceField(choices=ALCHOHOL)
    smoke = forms.ChoiceField(choices=SMOKE)
    horoscope = forms.ChoiceField(choices=HOROSCOPE)
    target = forms.ChoiceField(choices=TARGET)

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile


    class Meta:
        model = Profile
        # fields = ('name', 'age', 'city', 'description', 'gender',\
        #            'children', 'education', 'profession', 'languages', 'tags', 'image', 'alchohol', 'smoke', 'horoscope', 'target')
        fields = '__all__'