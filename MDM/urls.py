"""MDM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
from shop.views import pageNotFound

"""Include фунция для передачи адресов маршрутизации страницы, функцият 
принимает путь к файлу, в котором будут маршруты к приложению на сайте"""

admin.autodiscover()

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('', include('blog.urls')),
]

handler404 = pageNotFound  #если пользователь введет некорректный путь в строке

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)