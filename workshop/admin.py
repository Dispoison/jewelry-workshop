from django.contrib import admin

from workshop.models import JewelryType, Material, Gem, Jewelry, Client, Order

admin.site.register(Jewelry)
admin.site.register(Order)
admin.site.register(Client)
admin.site.register(JewelryType)
admin.site.register(Material)
admin.site.register(Gem)
