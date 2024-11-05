from watch.models import CartItem

def cart_items_count(request):
    if request.user.is_authenticated:
        cart_items_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_items_count = 0

    return {'cart_items_count': cart_items_count}