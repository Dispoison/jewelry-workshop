from collections import namedtuple

from core.settings import CART_SESSION_KEY
from workshop.models import Jewelry


class GuestCart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = dict()
        self.cart = cart

    def get_order_data(self):
        order_data = {"items": [], "total_price": 0}
        order_item_ids = list(self.cart.keys())
        OrderItem = namedtuple("OrderItem", "id name quantity price total_price href img_url")
        db_items = Jewelry.objects.filter(id__in=order_item_ids)
        for item in db_items:
            quantity = self.cart[str(item.id)]["quantity"]
            order_item = OrderItem(
                id=item.id,
                name=item.name,
                quantity=quantity,
                price=item.price,
                total_price=item.price*quantity,
                href=item.get_absolute_url(),
                img_url=item.photo.url,
            )
            order_data["items"].append(order_item)
            order_data["total_price"] += order_item.total_price
        return order_data

    def get_items_quantity(self):
        quantity = 0
        for item_id, item_data in self.cart.items():
            item_quantity = item_data.get("quantity")
            if isinstance(item_quantity, int) and item_quantity > 0:
                quantity += item_quantity
        return quantity

    def is_item_in_cart(self, item_id: str):
        return item_id in self.cart

    def add(self, item_id, quantity=1):
        if quantity < 1:
            return
        if item_id not in self.cart:
            self.cart[item_id] = {"quantity": 0}

        self.cart[item_id]["quantity"] = quantity
        self.save()

    def update(self, order_items):
        new_ids = set([item["id"] for item in order_items])
        for item_id in list(self.cart.keys()):
            if item_id not in new_ids:
                del self.cart[item_id]
        for item in order_items:
            self.add(item["id"], item["quantity"])
        self.save()

    def remove(self, item_id):
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def remove_all(self):
        self.cart = self.session[CART_SESSION_KEY] = dict()
        self.save()

    def is_not_empty(self):
        return bool(self.cart)

    def save(self):
        self.session.modified = True
