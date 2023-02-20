from django.urls import path
from workshop.views import (MainPageView, JewelryTypeView, JewelryView, post_add_product_to_cart,
                            post_remove_product_to_cart, post_edit_cart, OrderView, post_make_order)

urlpatterns = [
    path("", MainPageView.as_view(), name="home"),
    path("category/<slug:slug>/", JewelryTypeView.as_view(), name="category"),
    path("jewelry/<slug:slug>/", JewelryView.as_view(), name="jewelry"),
    path("cart/add", post_add_product_to_cart, name="cart_add"),
    path("cart/remove", post_remove_product_to_cart, name="cart_remove"),
    path("cart/edit", post_edit_cart, name="cart_edit"),
    path("order", OrderView.as_view(), name="order"),
    path("order/create", post_make_order, name="order_create"),
]
