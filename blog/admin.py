from django.contrib import admin
from .models import *


# Register your models here.
class MainPostsAdmin(admin.ModelAdmin):
    '''Вспомогательный класс для отображения полей в таблице админ панели'''

    list_display = ('id', 'title', 'body', 'slug', 'image')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'slug')
    list_filter = ('id', 'slug')

admin.site.register(MainPosts, MainPostsAdmin)