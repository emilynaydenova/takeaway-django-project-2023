from datetime import datetime

from celery import shared_task
from decouple import config
from django.core.mail import send_mail

from app.models import OrderItem, Order
from Takeaway import settings


@shared_task
def send_mail_for_pending_order(order_pk):
    subject = "Order is pending"
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    items = OrderItem.objects.filter(order_id=order_pk)
    items_list = []
    for item in items:
        items_list.append(f"- {item.product.title}: {item.quantity} item(s)")
    items_str = ("\n").join(items_list)
    message = f"""
       Your order is accepted at {current_time}.\n\nThe Order includes:\n{items_str}\n\n
       Bon Apeti from {config('LOGO_NAME')}
       """
    order = Order.objects.get(pk=order_pk)

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [order.user,]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

