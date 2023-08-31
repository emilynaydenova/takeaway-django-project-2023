# https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
import os

from celery import Celery



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Takeaway.settings')
# make Celery instance
app = Celery('Takeaway', include=['app.tasks', 'accounts.tasks', ])

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


def get_celery_worker_status():
    i = app.control.inspect()
    availability = i.ping()
    stats = i.stats()
    registered_tasks = i.registered()
    active_tasks = i.active()
    scheduled_tasks = i.scheduled()
    result = {
        'availability': availability,
        'stats': stats,
        'registered_tasks': registered_tasks,
        'active_tasks': active_tasks,
        'scheduled_tasks': scheduled_tasks
    }
    return result


def is_celery_working():
    try:
        app.broker_connection().ensure_connection(max_retries=3)
    except Exception as ex:
        raise RuntimeError("Failed to connect to celery broker, {}".format(str(ex)))