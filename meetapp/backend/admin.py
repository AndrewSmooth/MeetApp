from django.contrib import admin

from .models import Profile, Image, Tag, Language, AdvUser



# class AdvUserAdmin(admin.ModelAdmin):
#     list_display = ('__str__', 'is_activated', 'date_joined')
#     search_fields = ('username', 'email', 'first_name', 'last_name')
#     # fields = (('username', 'email'), 
#     #           ('first_name', 'last_name'), 
#     #           ('send_messages', 'is_active', 'is_activated'), 
#     #           ('is_staff', 'is_superuser'), 
#     #           'groups', 'user_permissions', 
#     #           ('last_login', 'date_joined'),          
#     #           )
#     readonly_fields = ('last_login', 'date_joined')


class ImageInline(admin.TabularInline):
    model = Profile.images.through


class TagInline(admin.TabularInline):
    model = Profile.tags.through


class LanguageInline(admin.TabularInline):
    model = Profile.languages.through


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'city', 'description', 'gender', 'children',\
                    'education', 'profession', 'alcohol', 'smoke', 'horoscope', 'target')
    fields = ('name', 'age', 'city', 'description', 'gender', 'children',\
                    'education', 'profession', 'alcohol', 'smoke', 'horoscope', 'target')
    inlines = (ImageInline, TagInline, LanguageInline)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('url', )


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', )

    
admin.site.register(Profile, ProfileAdmin)
# admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Language, LanguageAdmin)