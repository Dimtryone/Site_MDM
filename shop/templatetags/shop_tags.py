from django import template
#Модуль template для работы с шаблонами
from ..models import *


register = template.Library()
#с помощью Library создают экземпляр класса и регистрируют собственные теги
# далее описывают функцию (теги бывают простыми - возвращает данные и
# включающими может являться фрагментом html страницы) в зависимости
# от декоратора. В декораторе можно указать атрибут name чтобы обращаться не
# по названию функции, а по имени
#простой тег:


@register.simple_tag()
def get_categories():
    '''Сортировку категории и выводит согласно списку ranging_categories'''

    ranging_categories = ['Платья', 'Костюмы', 'Рубашки', 'Пиджаки', 'Джинсы',
                          'Водолазки', 'Другое', 'Распродажа']
    list_category = []
    for category in ranging_categories:
         category = Category.objects.get(name_category=category)
         list_category.append(category)
    return list_category


@register.inclusion_tag('shop/categories_for_list.html')
def show_all_categories():
    ranging_categories = ['Платья', 'Костюмы', 'Рубашки', 'Пиджаки', 'Джинсы',
                          'Водолазки', 'Другое', 'Распродажа']
    list_category = []
    for category in ranging_categories:
        category = Category.objects.get(name_category=category)
        list_category.append(category)
    return {'list_category': list_category}

