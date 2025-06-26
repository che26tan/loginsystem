from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_ready
import os

# Set environment for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings.dev_settings')

# Create and configure Celery app
app = Celery('dev_celery')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in your app
app.autodiscover_tasks(['celery_autorun'])

# Periodic task schedule
app.conf.beat_schedule = {
    # 'payment-confirm-from-portal-hourly': {
    #     'task': 'celery_autorun.tasks.payment_confirm_from_portal',
    #     'schedule': crontab(minute=0),
    # },
    # 'payment-confirm-to-email-hourly': {
    #     'task': 'celery_autorun.tasks.payment_confirm_to_email',
    #     'schedule': crontab(minute=0),
    # },
    # 'payment-confirm-to-phone-hourly': {
    #     'task': 'celery_autorun.tasks.payment_confirm_to_phone',
    #     'schedule': crontab(minute=0),
    # },
    # 'payment-failed-to-phone-hourly': {
    #     'task': 'celery_autorun.tasks.payment_failed_to_phone',
    #     'schedule': crontab(minute=0),
    # },
}

# Run metadata_initialised only once on worker start
@worker_ready.connect
def at_start(sender, **kwargs):
    # import django
    # django.setup()
    sender.app.send_task("celery_autorun.tasks.metadata_initialised")