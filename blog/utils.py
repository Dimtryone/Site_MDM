# from .models import MainPosts

header_menu = [{'title': 'о себе', 'url_name': 'my_site'},
               {'title': 'портфолио', 'url_name': 'shop'},
               {'title': "достижения", 'url_name': 'achievement'},
               {'title': 'развитие', 'url_name': 'development'}
            ]
git = 'https://github.com/Dimtryone'
resume = 'https://kazan.hh.ru/resume/c6af9d19ff0ade59ca0039ed1f69754768764d?hhtmFrom=resume_list'


# class DataBlogMixin:
#     '''Вспомогательный класс (Mixin) для приложения blog'''
#
#     def get_context(self, **kwargs):
#         ''' super().get_context_data(**kwargs) для получения других данных
#         контекста, например, posts '''
#
#         context = kwargs
#         #post = MainPosts.objects.all().order_by('pk')
#         context['header_menu'] = header_menu
#         context['git'] = git
#         context['resume'] = resume
#         #context['post'] = post
#         return context