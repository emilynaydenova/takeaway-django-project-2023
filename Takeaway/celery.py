# https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Takeaway.settings')
# make Celery instance
app = Celery('Takeaway', include=['app.tasks', 'accounts.tasks', ])

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
