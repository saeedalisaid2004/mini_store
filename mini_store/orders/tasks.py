from celery import shared_task
from django.core.mail import send_mail

from orders.models import Order


@shared_task
def send_order_confirmation_email(order_id):
    try:
        order = Order.objects.get(id=order_id)
        subject = f"تأكيد الطلب رقم #{order.id}"
        message = f"مرحباً {order.user.username}،\n\nتم استلام طلبك بنجاح! الإجمالي: {order.total_amount} SAR."

        send_mail(
            subject=subject,
            message=message,
            from_email="saeedali@ministore.com",
            recipient_list=[order.user.email],
            fail_silently=True,
        )
    except Order.DoesNotExist:
        pass
