from django.shortcuts import render
from .models import MainPosts
from django.views.generic import ListView, DetailView
from django.db.models import Q


# Create your views here.

header_menu = [{'title': 'о себе', 'url_name': 'my_site'},
               {'title': 'портфолио', 'url_name': 'shop'},
               {'title': "достижения", 'url_name': 'achievement'},
               {'title': 'развитие', 'url_name': 'development'}
            ]
git = 'https://github.com/Dimtryone'
resume = 'https://kazan.hh.ru/resume/c6af9d19ff0ade59ca0039ed1f69754768764d?hhtmFrom=resume_list'


class BlogHome(ListView):
    ''' Класс для представления главной страницы сайта
    template_name - для указания своего шаблона по умолчанию путь имя приложения/имя модели
    context_object_name - для того чтобы в шаблоне не менять название переменной
    extra_context - можно передавать только неизменяемые значения, поэтому
    создают функцию, которая будт формировать котекст.
    succes_url = reverse_lazy('URL_name') - для переотправки на URL,
    при добавлении статью в классе CreateView
    '''


    model = MainPosts
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        ''' super().get_context_data(**kwargs) для получения других данных
        контекста, например, posts '''

        context = super().get_context_data(**kwargs)
        context['header_menu'] = header_menu
        context['git'] = git
        context['resume'] = resume
        context['title'] = 'Вдовин Дмитрий'
        context['post_sidebar'] = self.get_queryset_for_sidebar()
        #c_def = self.get_context(title='Вдовин Дмитрий')
        return context

    def get_queryset(self):
        '''функция для того чтобы указывать параметры для запроса модели'''

        return MainPosts.objects.all().order_by('pk')

    def get_queryset_for_sidebar(self):
        '''функция для того чтобы указывать параметры для запроса модели'''

        return MainPosts.objects.filter(Q(pk__lt=7) & Q(pk__gt=3)).order_by(
            'pk')

class BlogDetail(DetailView):
    '''класс для отображения деталей поста
    slug_url_kwarg - для передачи в url.py параметра slug
    pk_url_kwarg - для передачи в url.py параметра id  '''

    model = MainPosts
    template_name = 'blog/index_post.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        ''' super().get_context_data(**kwargs) для получения других данных
        контекста, например, posts '''

        context = super().get_context_data(**kwargs)
        context['header_menu'] = header_menu
        context['post_sidebar'] = self.get_queryset_for_sidebar()
        #c_def = self.get_context(title=context['post'])
        return context
        #dict(list(context.items()) + list(c_def.items()))

    def get_queryset_for_sidebar(self):
        '''функция для того чтобы указывать параметры для запроса модели'''

        return MainPosts.objects.filter(Q(pk__lt=7) & Q(pk__gt=0)).order_by('pk')

def achievement(request):
    context = {'title': 'Достижения',
               'header_menu': header_menu,
               'git': git,
               'resume': resume}
    return render(request, 'blog/index_ach.html', context=context)

def development(request):
    context = {'title': 'Планы развития',
               'header_menu': header_menu,
               'git': git,
               'resume': resume}
    return render(request, 'blog/index_dev.html', context=context)


# def show_post_detail(request, slug):
#     post = MainPosts.objects.get(slug__iexact=slug)
#     context = {'post': post,
#                'title': f'Вдовин Дмитрий {slug}',
#                'header_menu': header_menu}
#     return render(request, 'blog/index_post.html', context=context)


#старая функция представления
# def mysite(request):
#     posts = MainPosts.objects.all()
#     context = {'posts': posts,
#                'title': 'Вдовин Дмитрий',
#                'header_menu': header_menu,
#                'git': git,
#                'resume': resume}
#     return render(request, 'blog/index.html', context=context)