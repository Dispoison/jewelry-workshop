from core.settings import WEBSITE_TITLE
from workshop.cart import GuestCart


class ViewDataMixin:
    def get_mixin_context(self, **kwargs):
        context = kwargs
        cart = GuestCart(self.request)
        context.update({
            "title": WEBSITE_TITLE,
            "cart_items_quantity": cart.get_items_quantity()
        })
        return context
