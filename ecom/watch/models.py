from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Item(models.Model):
    CATEGORY_CHOICES = (
        ('m', 'Mens'),
        ('w', 'Womens'),
        ('u', 'Unisex'),
    )
    item_name = models.CharField(max_length=50)
    item_desc = models.CharField(max_length=300)
    item_price = models.IntegerField()
    item_image = models.CharField(
        max_length=500, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8T1KpczAfbyEEVvBEOTQGMHBl1_WqtC9ZtA&s')
    item_quantity = models.IntegerField(default=0)  # New field for quantity
    item_offer = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(
        max_length=1, choices=CATEGORY_CHOICES, default="m")

    def __str__(self):
        return self.item_name

class CusOrders(models.Model):
    order_status_choices = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),

    )
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_status = models.CharField(max_length=20, choices=order_status_choices, default='Order Confirmed')

    def __str__(self):
        return f"[Order ID: {self.order_id}] {self.quantity} x {self.item.item_name} {self.user.username}'s order (Status: {self.order_status})"
    
    
class CartItem(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.item_name} in {self.user.username}'s cart"
