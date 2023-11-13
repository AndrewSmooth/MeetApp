from django import forms

from .models import Profile, Language, LanguageProfile, Tag, TagProfile

from django.core.exceptions import ValidationError

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
    name = forms.CharField(max_length=20, label='Имя', required = True)
    age = forms.IntegerField( label='Возраст', min_value=18, required = True)
    city = forms.CharField(max_length=168, label='Город', required = True)
    profession = forms.CharField(max_length=50, required=False, label= 'Работа')
    description = forms.Textarea()
    gender = forms.TypedChoiceField(label='Пол', choices=GENDERS, required = True)
    children = forms.ChoiceField(label='Дети', required=False, choices=CHILDREN)
    education = forms.CharField(max_length=150, required=False, label='Образование')
    languages = forms.ModelMultipleChoiceField(Language.objects.get_queryset(), widget=forms.CheckboxSelectMultiple, label='Языки', required = True)
    tags = forms.ModelMultipleChoiceField(Tag.objects.get_queryset(), widget=forms.CheckboxSelectMultiple, label='Мои интересы', required = True)
    images = forms.Textarea()
    alcohol = forms.ChoiceField(choices=ALCHOHOL, required=False, label='Алкоголь')
    smoke = forms.ChoiceField(choices=SMOKE, required=False, label='Курение')
    horoscope = forms.ChoiceField(choices=HOROSCOPE, required=False, label='Знак зодиака')
    target = forms.ChoiceField(choices=TARGET, required=False, label='Цель')

    def clean(self):
        super().clean()
        if self.cleaned_data['languages'] == False or self.cleaned_data['tags'] == False:
            raise ValidationError()


    def save(self, commit=True):
        profile = super().save(commit=False)
        tags = self.cleaned_data['tags']
        languages = self.cleaned_data['languages']
        
        if commit:
            profile.save()
            if tags:
                for tag in tags:
                    TagProfile.objects.create(tag = tag, profile = profile)
            if languages:
                for language in languages:
                    LanguageProfile.objects.create(language = language, profile = profile)
        return profile


    class Meta:
        model = Profile
        # fields = ('name', 'age', 'city', 'description', 'gender',\
        #            'children', 'education', 'profession', 'languages', 'tags', 'image', 'alchohol', 'smoke', 'horoscope', 'target')
        fields = '__all__'