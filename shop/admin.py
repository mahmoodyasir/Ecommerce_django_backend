from django.contrib import admin
from .models import *


class ChoicesAdmin(admin.ModelAdmin):
    search_fields = ['id', 'choice_name']
    list_display = ['id', 'choice_name', 'date']
    list_per_page = 10


class OrderAdmin(admin.ModelAdmin):
    search_fields = ['id', 'cart']
    list_display = ['id', 'cart', 'mobile', 'address', 'order_list', 'payment_complete', 'payment_type', 'transaction_id', 'transaction_medium']
    list_per_page = 10


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['id', 'title']
    list_display = ['id', 'title']
    list_per_page = 10


class WishListAdmin(admin.ModelAdmin):
    search_fields = ['id', 'wishedProduct']
    list_display = ['id', 'date']
    list_per_page = 10


admin.site.register(Profile)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order, OrderAdmin)
admin.site.register(Choice, ChoicesAdmin)
admin.site.register(WishList, WishListAdmin)

