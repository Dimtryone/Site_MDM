from django.template.defaulttags import url
from django.urls import path, include, re_path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth import views
from rest_framework import routers

#
# router = routers.SimpleRouter()
# router.register(r'product_size', ProductWievSet)
context = {'header_menu': header_menu}
# app_name = 'make_order'
urlpatterns = [
    path('shop/', shop, name='shop'),
    path('shop/<slug>', catalog, name='catalog'),
    path('product/<int:product_id>', product, name='product'),
    path('login/', LoginUser.as_view(), name='login_test'),
    path('logout/', logout_user, name='logout_test'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('create_user', creat_user_popup, name='create_user'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('make_order/', make_order, name='make_order'),
    path('api/size/', ProductAPIList.as_view(), name='product_apiList'),
    path('api/amount/', ProductAmountView.as_view(), name='amount_product'),
    path('api/orders/', OrderAPICreate.as_view(), name='order_orm'),
    path('api/order_products/', OrderProductCreateView.as_view(), name='order_prod_orm'),
    path('api/getstatus/', GetStatus.as_view(), name='status_sql'),
    path('api/gettoken/', CustomAuthToken.as_view()),
    # path('api/drf-auth/', include('rest_framework.urls',)),
    # path('api/auth/', include('djoser.urls',)),
    # re_path(r'^auth/', include('djoser.urls.authtoken',)),
    # re_path(r'^api/size/(?P<product_id>\d+)/(?P<color>\w+)/$', ProductAPIList.as_view(), name='product_apiList'),
    #reset password
    path('password_reset/', PasswordResetViewUser.as_view(), name='password_reset'),
    path('password_reset/done/', MyPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/', MyPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)