from django.apps import AppConfig

# from MDM.MDM import settings


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    verbose_name = 'MDM Showroom'




#
# class ShopConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'shop'
#     verbose_name = 'MDM Showroom'

    # def ready(self):
    #     # Import celery app now that Django is mostly ready.
    #     # This initializes Celery and autodiscovers tasks
    #     # Импортируем celery app из модуля myapp.celery
    #     from celery import app as celery_app
    #     #
    #     # # Задачи будут автоматически обнаружены и зарегистрированы
    #     # # в celery app благодаря вызову метода autodiscover_tasks()
    #     celery_app.autodiscover_tasks()