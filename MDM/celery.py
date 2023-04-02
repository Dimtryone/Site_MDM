import os
from datetime import timedelta
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MDM.MDM.settings')
app = Celery('MDM')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# для запуска периодических задач
app.conf.beat_schedule = {
    'check_orders': {
        'task': 'tasks.check_orders',
        'schedule': timedelta(minutes=2), #для теста 2 минуты, исправить на 10
    },

    'process_delivered_orders': {
        'task': 'tasks.process_delivered_orders',
        'schedule': timedelta(minutes=2), #для теста 2 минуты, исправить на 10
    },
}