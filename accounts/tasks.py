from celery import shared_task
from decouple import config
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from Takeaway import settings

UserModel = get_user_model()


@shared_task
def send_registration_email(user_pk):
    print("Sending registration email")
    user = UserModel.objects.get(pk=user_pk)
    subject = f"Register in {config('LOGO_NAME')}"

    message = f"""
           Registration with this mail {user.email} was made.\n\n
           Welcome from {config('LOGO_NAME')} !
           """

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)



