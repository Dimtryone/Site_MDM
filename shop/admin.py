from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, ProductImage


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    '''Вспомогательный класс для отображения полей в таблице админ панели'''

    list_display = ('id', 'title', 'color', 'material', 'description',
                    'photo', 'category', 'brend', 'amount', 'price',
                    'product_id')
    list_display_links = ('title', 'category', 'amount', 'price', 'product_id')
    search_fields = ('title', 'category', 'size', 'amount')
    list_filter = ('title', 'category', 'size', 'amount', 'brend')

admin.site.register(Product, ProductAdmin)

class ProductImageAdmin(admin.ModelAdmin):
    '''Вспомогательный класс для отображения полей в таблице админ панели'''

    list_display = ('product', 'image', 'created_at', 'updated_at')
    list_display_links = ('product', 'image')
    search_fields = ('product', 'id')
    list_filter = ('product', 'created_at')



admin.site.register(ProductImage, ProductImageAdmin)


class BrendAdmin(admin.ModelAdmin):

    list_display = ('id', 'name_brend')
    list_display_links = ('id', 'name_brend')
    search_fields = ('name_brend',)
    list_filter = ('name_brend',)

admin.site.register(Brend, BrendAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_category', 'link_icons', 'slug')

admin.site.register(Category, CategoryAdmin)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    ordering = ("email",) #error  (admin.E033)
    list_filter = ('is_admin',)  #error (admin.E116) T
    list_display = ['email', 'name', 'last_name', 'phone']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'last_name', 'phone', 'password1',
            'password2'),
        }),
    )
    search_fields = ('email',)
    filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)

