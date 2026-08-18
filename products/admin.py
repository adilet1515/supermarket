from django.contrib import admin

from .models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    def desc_short(self, obj: Product):
        return obj.description[:30]

    list_display = 'name', 'description', 'desc_short'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
