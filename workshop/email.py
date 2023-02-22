from threading import Thread

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from workshop.models import Order


def send_order_mail(order_id):
    order = (Order.objects
             .select_related("client")
             .prefetch_related("orderitem_set")
             .prefetch_related("orderitem_set__jewelry")
             .get(id=order_id))
    order_price = 0
    for item in order.orderitem_set.all():
        item.total_price = item.jewelry.price * item.quantity
        order_price += item.total_price
    order.price = order_price

    html_message = render_to_string('workshop/email/email.html', {"order": order})
    plain_message = strip_tags(html_message)

    send_mail(
        subject=f"Ваше замовлення №{ order.id } прийняте",
        message=plain_message,
        from_email=None,
        recipient_list=[order.client.email],
        html_message=html_message,
    )


def send_order_mail_in_background(order_id):
    thread = Thread(target=send_order_mail, kwargs={"order_id": order_id})
    thread.start()
