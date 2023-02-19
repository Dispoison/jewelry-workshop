from django.urls import path
from workshop.views import MainPageView, JewelryTypeView, JewelryView

urlpatterns = [
    path("", MainPageView.as_view(), name="home"),
    path("category/<slug:slug>/", JewelryTypeView.as_view(), name="category"),
    path("jewelry/<slug:slug>/", JewelryView.as_view(), name="jewelry"),
]
