import json

from django.db.transaction import atomic
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView

from workshop.cart import GuestCart
from workshop.email import send_order_mail_in_background
from workshop.models import JewelryType, Jewelry, Client, Order, OrderItem
from workshop.serializers import CartIdSerializer, CartUpdateSerializer, OrderInfoSerializer
from workshop.utils.mixins.view_data_mixin import ViewDataMixin


class MainPageView(ViewDataMixin, ListView):
    model = JewelryType
    template_name = "workshop/index/index.html"
    context_object_name = "jewelry_types"

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        mixin_context = self.get_mixin_context()
        return base_context | mixin_context

    def get_queryset(self):
        return self.model.objects.order_by('id')


class JewelryTypeView(ViewDataMixin, ListView):
    model = Jewelry
    template_name = "workshop/category_list/listofitems.html"
    context_object_name = "jewelries"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        mixin_context = self.get_mixin_context(jewelry_type=get_object_or_404(JewelryType, slug=self.kwargs["slug"]))
        return base_context | mixin_context

    def get_queryset(self):
        jewelries = self.model.objects.select_related("type").filter(
            type__slug=self.kwargs["slug"]
        ).order_by("id")
        return jewelries


class JewelryView(ViewDataMixin, DetailView):
    model = Jewelry
    template_name = "workshop/jewelry/itemPage.html"
    context_object_name = "jewelry"

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        cart = GuestCart(self.request)
        item_in_cart = cart.is_item_in_cart(str(self.object.id))
        mixin_context = self.get_mixin_context(jewelry_type=self.object.type, item_in_cart=item_in_cart)
        return base_context | mixin_context

    def get_object(self, queryset=None):
        jewelry = (self.model.objects
                   .prefetch_related("materials")
                   .prefetch_related("gems")
                   .get(slug=self.kwargs["slug"]))
        return jewelry


class OrderView(ViewDataMixin, TemplateView):
    template_name = "workshop/order/orderReview.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        cart = GuestCart(self.request)
        order_data = cart.get_order_data()
        items_quantity = cart.get_items_quantity()
        mixin_context = self.get_mixin_context(items=order_data["items"], total_price=order_data["total_price"],
                                               cart_items_quantity=items_quantity)
        return base_context | mixin_context


def post_add_product_to_cart(request):
    if request.method == "POST":
        body_data = json.loads(request.body.decode("utf-8"))
        serializer = CartIdSerializer(data=body_data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            cart = GuestCart(request)
            cart.add(validated_data["id"])
            items_quantity = cart.get_items_quantity()
            response_content = json.dumps({"cart_items_quantity": items_quantity, "added_item": validated_data["id"]})
            return HttpResponse(response_content, status=200)
    return HttpResponse(status=400)


def post_remove_product_to_cart(request):
    if request.method == "POST":
        body_data = json.loads(request.body.decode("utf-8"))
        serializer = CartIdSerializer(data=body_data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            cart = GuestCart(request)
            cart.remove(validated_data["id"])
            items_quantity = cart.get_items_quantity()
            response_content = json.dumps({"cart_items_quantity": items_quantity, "removed_item": validated_data["id"]})
            return HttpResponse(response_content, status=200)
    return HttpResponse(status=400)


def post_edit_cart(request):
    if request.method == "POST":
        body_data = json.loads(request.body.decode("utf-8"))
        serializer = CartUpdateSerializer(data=body_data, many=True)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            cart = GuestCart(request)
            cart.update(validated_data)
            items_quantity = cart.get_items_quantity()
            response_content = json.dumps({"cart_items_quantity": items_quantity})
            return HttpResponse(response_content, status=200)
    return HttpResponse(status=400)


def post_make_order(request):
    if request.method == "POST":
        body_data = json.loads(request.body.decode("utf-8"))
        serializer = OrderInfoSerializer(data=body_data)
        cart = GuestCart(request)
        if cart.is_not_empty() and serializer.is_valid():
            validated_data = serializer.validated_data
            if len(validated_data["cart"]) == 0:
                return HttpResponseBadRequest("You cannot make order without items", status=400)
            client, created = Client.objects.update_or_create(phone_number=validated_data["client"]["phone_number"],
                                                              defaults=validated_data["client"])

            order = Order(client=client)
            with atomic():
                client.save()
                order.save()
                for cart_item in validated_data["cart"]:
                    order_item = OrderItem(jewelry_id=cart_item["id"], order=order, quantity=cart_item["quantity"])
                    order_item.save()
            cart.remove_all()

            send_order_mail_in_background(order.id)

            return redirect("home")
    return HttpResponse(status=400)
