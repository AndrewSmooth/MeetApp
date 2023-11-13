from django.contrib import admin

from .models import Profile,  Tag, Language, TagProfile

class TagInline(admin.TabularInline):
    model = Profile.tags.through


class LanguageInline(admin.TabularInline):
    model = Profile.languages.through


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'city', 'description', 'gender', 'children',\
                    'education', 'profession', 'alcohol', 'smoke', 'horoscope', 'target')
    fields = ('name', 'age', 'city', 'description', 'gender', 'children', 'images',\
                    'education', 'profession', 'alcohol', 'smoke', 'horoscope', 'target')
    inlines = (TagInline, LanguageInline)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', )

class TagProfileAdmin(admin.ModelAdmin):
    list_display = ('tag', 'profile')

    
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(TagProfile, TagProfileAdmin)