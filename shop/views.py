from django.contrib.auth import logout, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.db.models import Q, Count, F
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView
from rest_framework.permissions import IsAuthenticated
from .forms import CustomUserCreationForm, LoginUserForm, ResetPasswordUserForm, \
    MySetPasswordForm
from .models import Category, Product, CustomUser, Size, OrderProduct, \
    OrderStatus, Status, Order
from blog.views import *
from rest_framework import generics, status, views
from .serializers import ProductSerializer, SizeSerializer, OrderSerializer, \
    OrderProductSerializer, MyAuthTokenSerializer, OrderStatusSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from datetime import datetime
from django.db import connection, OperationalError  # для прямого SQL запроса
from .tasks import increase_product_quantity_task


class CustomAuthToken(ObtainAuthToken):
    '''Класс для получения токена'''

    serializer_class = MyAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

class OrderAPICreate(generics.CreateAPIView):
    '''Класс для создания информации о заказе в таблице Order'''
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderProductCreateView(generics.CreateAPIView):
    '''Класс для создания промежуточной таблицы OrderProduct и обновления
    информации в таблице Product'''
    serializer_class = OrderProductSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        order_id = int(request.data.get('order'))
        product_id = int(request.data.get('product'))
        count_ord = request.data.get('count')

        if OrderProduct.objects.filter(order=order_id, product=product_id).exists():
            return Response({'message': 'Запись уже существует'}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Выполняем UPDATE запрос на объект Product
        try:
            product = Product.objects.get(pk=product_id)
            if product.amount - int(count_ord) == 0:
                print("***********")
                print()
                print("отдаем задачу в CELERY")
                print()
                print("*******")
                increase_product_quantity_task.delay(product_id)
                print("отдали задачу в CELERY")
            product.amount -= int(count_ord)
            print("***********")
            print()
            print("Перед сохранением product")
            print()
            print("*******")
            product.save()
            print("***********")
            print()
            print("cохранили product")
            print()
            print("*******")


            # INSERT OrderStatus на присвоение статуса
            if OrderStatus.objects.filter(order_id=order_id, status_id=3).exists():
                print("***********")
                print()
                print("Пара OrderStatus дублируется")
                print()
                print("*******")
            else:
                date_today = datetime.now()
                status_order = Status.objects.get(id=3)
                order_order = Order.objects.get(id=order_id)
                OrderStatus.objects.create(
                    date_strat=date_today,
                    date_finish=date_today,
                    flag_finish=False,
                    status_id=status_order,
                    order_id=order_order
                )
                print("***********")
                print()
                print("OrderStatus создан")
                print()
                print("*******")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({'message': 'Продукт не найден'}, status=status.HTTP_404_NOT_FOUND)


class GetStatus(APIView):
    '''Класс для получения статуса своего заказа'''

    serializer_class = OrderStatusSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_id = request.user.id
            print(user_id)
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT name_status, so2.id, sc.name, sc.last_name "
                    "FROM shop_status ss "
                    "INNER JOIN shop_orderstatus so ON so.status_id_id = ss.id "
                    "INNER JOIN shop_order so2 ON so2.id = so.order_id_id "
                    "INNER JOIN shop_customuser sc ON so2.user_id = sc.id "
                    "WHERE sc.id = %s;",
                    [user_id])
                result_query = cursor.fetchall()
                print("*******")
                print()
                print(result_query)
                print()
                print("*******")
                keys = ['status', 'id', 'first_name', 'last_name']
                result = []
                for row in result_query:
                    result.append(dict(zip(keys, row)))

                return Response(result)
        except OperationalError:
            return Response({'error': 'Orders not found'},status=status.HTTP_404_NOT_FOUND)

# logger = logging.getLogger(__name__) - НУЖНО ЛИ ЗАПИСЫВАТЬ ЛОГИ?
class ProductAPIList(generics.ListAPIView):
    '''Класс для получения из таблицы Product информации о доступных размерах товара'''

    serializer_class = SizeSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')
        color = request.GET.get('color')

        # logger.debug(f"ProductAPIList: product_id={product_id}, color={
        # color}") НУЖНО ЛИ ВООБЩЕ ЗАПИСЫВАТЬ ЛОГИ?
        try:
            queryset = Size.objects.filter(product__product_id=product_id, product__color=color).values_list('size', flat=True)
            sizes = [{"size": size} for size in queryset]
            return JsonResponse(sizes, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



class ProductAmountView(views.APIView):
    '''Класс для получения из таблицы Product информации о количестве товара'''
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        product_id = request.GET.get('product_id', None)
        color = request.GET.get('color', None)
        size = request.GET.get('size', None)

        if product_id and color and size:
            try:
                product = Product.objects.get(product_id=product_id,
                                              color=color, size__size=size)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'},
                                status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer_class(product)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid parameters'},
                            status=status.HTTP_400_BAD_REQUEST)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>По данному url-адресу страница не '
                                'найдена. Переходите в раздел Товары или '
                                'Тренды, чтобы узнать последние новости о моде'
                                '</h1>')
def shop(request):
    ''' Функция отображает главную страницу магазина,  сортировка категорий
    производится через templatetags
    header_menu - переменная импортируется из blog/views.py
    '''

    context = {'header_menu': header_menu,
               'title': 'MDM showroom',
               }
    return render(request, 'shop/shop_main.html', context=context)


def catalog(request, slug):
    ''' Функция отображает html товаров конкретной категории
    header_menu - переменная импортируется из blog/views.py
    '''

    category = Category.objects.get(slug__iexact=slug)
    #things = Product.objects.values('title', 'brend').annotate(total=Count('id')).filter(category=category) - запрос с GROUP BY
    products = Product.objects.filter(category=category).distinct('product_id')  #product_id это дополнительный id товара который группирует одежду по размерам и цветам
    context = {'list_things': products,
              'title': f'MDM SHOP {slug}',
              'header_menu': header_menu,
               }
    return render(request, 'shop/shop_catalog.html', context=context)

def product(request, product_id):
    '''Отображает html конкретного выбранного товара. Для этого делается
    запрос в БД на изображения товара и на количество товара по цвету.
        header_menu - переменная импортируется из blog/views.py
    '''

    product = get_object_or_404(Product, pk=product_id)
    product_id = product.product_id
    products = Product.objects.filter(product_id=product_id)
    image_urls = [image.image_url for product in products for image in product.images.all()]

    color_counts = Product.objects.filter(product_id=product_id).values('color').annotate(color_count=Count('color')).order_by('color')

    context = {'product': product,
               'image_urls': image_urls,
               'colors': color_counts,
               'title': product.title,
               'header_menu': header_menu,
               }
    return render(request, 'shop/shop_thing.html', context=context)


def make_order(request):
    '''Отображает html с формой заказа.
        header_menu - переменная импортируется из blog/views.py
    '''

    context = {'header_menu': header_menu,
               'title': 'order',
               }
    return render(request, 'shop/shop_make_order.html', context=context)


def forgot_password(request):
    '''Функция для представления страницы для восстановления пароля'''

    context = {'header_menu': header_menu,
               'title': 'MDM showroom',
               }
    return render(request, 'shop/forgot_password.html', context=context)


class RegisterUser(CreateView):
    '''formclass джанго предоставляет стандартную форму для регистрации
    пользователя
    template_name ссылка на шаблон
    success_url адрес куда перенаправляется пользователь после успешной
    регистрации'''

    form_class = CustomUserCreationForm
    #CustomUserCreationForm Из form.py джанго предоставляет этот
    # класс его нужно использовать
    template_name = 'shop/form_registration.html'
    success_url = reverse_lazy('login')  #переход в случае успеха

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_menu'] = header_menu
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        '''ф-ия сохраняет объект в базе и передает ф-ии login объект реквест
        и юзера. ф-ия login создана джанго'''

        user = form.save()
        login(self.request, user)
        return redirect('shop')


class LoginUser(LoginView):
    '''Класс который обеспечивает работу нашей собственной формы авторизации'''

    template_name = 'shop/login.html'
    authentication_form = LoginUserForm


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_menu'] = header_menu
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('shop')


class PasswordResetViewUser(PasswordResetView):
    '''Класс для сброса пароля, стандартный'''

    email_template_name = 'shop/registration/password_reset_email.html'
    extra_email_context = None
    template_name = 'shop/registration/password_reset_form.html'
    token_generator = default_token_generator
    form_class = ResetPasswordUserForm

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_menu'] = header_menu
        context['title'] = 'Восстановление Пароля'
        return context


class MyPasswordResetDoneView(PasswordResetDoneView):
    '''Класс для отображения страницы, что восстановление пароля завершено'''

    template_name = 'shop/registration/password_reset_done.html'
   # success_url = reverse_lazy('password_reset_done')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['header_menu'] = header_menu
        context['title'] = 'Восстановление Пароля'
        return context


#@method_decorator(csrf_protect, name='dispatch')
class MyPasswordResetConfirmView(PasswordResetConfirmView):
    '''Класс для изменения проля, стандартный'''

    template_name = 'shop/registration/password_reset_confirm.html'
    form_class = MySetPasswordForm
   # success_url = reverse_lazy('password_reset_done')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['header_menu'] = header_menu
        context['title'] = 'Восстановление Пароля'
        return context

class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'shop/registration/password_reset_complete.html'
    # success_url = reverse_lazy('password_reset_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_menu'] = header_menu
        context['title'] = 'Восстановление Пароля'
        return context


def logout_user(request):
    logout(request)
    return redirect('shop')


def creat_user_popup(request):
    if request.method == 'POST':
        name = request.POST['name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        password2 = request.POST['password2']

        new_profile = CustomUser(name=name, last_name=last_name, email=email, phone=phone, password=password, password2=password2)
        new_profile.save()
        return render(HttpResponse('Вы успешно зарегистрировались'))


# def get_sizes(request):
#   selected_color = request.GET.get('color')
#   # получаем все размеры для выбранного цвета
#   sizes = Size.objects.filter(product_size__product__color=selected_color).values_list('size', flat=True)
#   data = {'sizes': list(sizes)}
#   # возвращаем данные в формате JSON
#   return JsonResponse(data)
#
# def change_amount_in_Product():
#     '''функция для увеличения остатков + 1 по всем товарам, вызывается'''
#
#     products = Product.objects.all()
#     for prod in products:
#         amount = prod.amount
#         prod(amount=amount + 1)
#         prod.save()
#         pass
#
# def update_status_in_Order():
#     orders = Order.objects.filter()
#     if OrderStatus.objects.filter(order_id=order_id, status_id=3).exists():
#         print("Пара OrderStatus дублируется")
#     else:
#         date_today = datetime.now()
#         status_order = Status.objects.get(id=3)
#         order_order = Order.objects.get(id=order_id)
#         OrderStatus.objects.create(
#             date_strat=date_today,
#             date_finish=date_today,
#             flag_finish=False,
#             status_id=status_order,
#             order_id=order_order
#         )
#     pass
#
#


