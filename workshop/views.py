from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from workshop.models import JewelryType, Jewelry
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
        mixin_context = self.get_mixin_context(jewelry_type=self.object.type)
        return base_context | mixin_context

    def get_object(self, queryset=None):
        jewelry = (self.model.objects
                   .prefetch_related("materials")
                   .prefetch_related("gems")
                   .get(slug=self.kwargs["slug"]))
        return jewelry
