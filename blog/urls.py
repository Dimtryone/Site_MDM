from shop.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', BlogHome.as_view(), name='my_site'),
    path('post/<str:slug>', BlogDetail.as_view(), name='post'),
    path('achievement/', achievement, name='achievement'),
    path('development/', development, name='development'),
    path('shop/', shop, name='shop')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)