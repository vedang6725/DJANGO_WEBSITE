from django.contrib import admin
from .models import Item, CusOrders, CartItem

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name', 'item_desc', 'item_price', 'category')
    
# Register your models here.

admin.site.register(Item)
admin.site.register(CartItem)
admin.site.register(CusOrders)