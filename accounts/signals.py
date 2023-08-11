import logging
from datetime import datetime

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver

from Takeaway import settings

from .models import Profile
from .tasks import send_registration_email


# 'def ready(self)' in apps.py to work signals

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)  #instance=email

        # send email -delay calls Celery
        send_registration_email.delay(instance.pk)


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logging.info(f" {user} logged-in  at {datetime.now()}")


@receiver(user_logged_out)
def log_user_login(sender, request, user, **kwargs):
    logging.info(f" {user} logged-out  at {datetime.now()}")
