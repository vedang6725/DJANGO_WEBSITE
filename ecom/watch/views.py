from django.shortcuts import render
from watch.models import Item
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from watch.models import Item, CusOrders, CartItem
from django.contrib import messages
from .utils import send_email_to_user

# Create your views here.

def index(request):
    itemlist = Item.objects.all()
    
    # for search functionality
    item_name = request.POST.get('item_name')
    if item_name != '' and item_name is not None:
        itemlist = Item.objects.filter(item_name__icontains=item_name)
    else:
        itemlist = Item.objects.all()
        
    context = {
        'itemlist':itemlist
    }
    
    if not itemlist:
        messages.info(request, 'No search results found.')
        
    return render(request, 'watch/index.html', context)

def detail(request, item_id):
    item = Item.objects.get(pk=item_id)
    
    context = {
        'item':item,
    }
    
    return render(request, 'watch/detail.html', context)


def mens(request):
    itemlist = Item.objects.filter(category='m')

    context = {
        'itemlist': itemlist
    }

    return render(request, 'watch/mens.html', context)


def womens(request):
    itemlist = Item.objects.filter(category='w')

    context = {
        'itemlist': itemlist
    }

    return render(request, 'watch/womens.html', context)


def unisex(request):
    itemlist = Item.objects.filter(category='u')
    
    context = {
        'itemlist': itemlist
    }

    return render(request, 'watch/unisex.html', context)


@login_required
def Orders(request):
    user = request.user

    if request.method == 'POST':
        Obj_CusOrds = CusOrders(
            user=user,
            quantity=request.POST.get('qty')
        )
        Obj_CusOrds.save()

    else:
        previous_orders = CusOrders.objects.filter(user=user)
        for order in previous_orders:
            order.total_amount = order.item.item_price * order.quantity
        grand_total = sum(order.item.item_price * order.quantity for order in previous_orders)
        context = {'previous_orders': previous_orders, 'grand_total': grand_total,}
        return render(request, 'watch/myorders.html', context)

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('qty', 1))

        if quantity < 1:
            quantity = 1
        elif quantity > 10:
            quantity = 10
        if request.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user, item=item
            )

            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity

            cart_item.save()

        return redirect('watch:cart_view')

    return redirect('watch:cart_view')


def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('item')
    
    # Count the number of cart items
    cart_items_count = cart_items.count()

    # Calculate the grand total for all items in the cart
    grand_total = sum(cart_item.item.item_price * cart_item.quantity for cart_item in cart_items)

    # Calculate the total price for each cart item
    for cart_item in cart_items:
        cart_item.total_price = cart_item.item.item_price * cart_item.quantity

    # Pass the cart items, grand total, and cart items count to the template
    return render(request, 'watch/cart.html', {
        'cart_items': cart_items, 
        'grand_total': grand_total, 
        'cart_items_count': cart_items_count  # Add this to your context
    })


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)

    if request.user == cart_item.user:
        cart_item.delete()

    return redirect('watch:cart_view')



from django.core.mail import send_mail

def send_email_to_user(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)

def create_order(cart_item, user, request):
    try:
        # Create a new order in the database
        order = CusOrders.objects.create(
            user=user,
            item=cart_item.item,
            quantity=cart_item.quantity,
        )
        # Send an email confirmation to the user
        send_email_to_user(
            "Your Order has been successfully placed",
            f"Dear {order.user},\n\n"
            f"Your order #{order.pk} has been successfully placed!\n"
            f"Here are the details:\n"
            f"{order.item.item_image}\n"
            f"- Item Name: {order.item.item_name}\n"
            f"- Quantity: {order.quantity}\n"
            f"- Price: ₹{order.item.item_price} x {order.quantity} = ₹{order.item.item_price * order.quantity}\n\n"
            f"Thank you for your purchase!",
            'vedangrane430@gmail.com',  # Your email address
            [user.email],  # Send to the user's email
        )
        return order
    except Exception as e:
        # Handle any errors and send a message to the user
        messages.error(request, f"Error creating order for {cart_item.item.item_name}: {str(e)}")
        return None



from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

def cancel_order(request, order_id):
    order = get_object_or_404(CusOrders, pk=order_id, user=request.user)  # Ensure the user owns the order
    
    if request.method == 'POST':
        user = request.user
        order.delete()  # Delete the order from the database
        
        # Send a cancellation confirmation email
        send_email_to_user(
            "Your Order has been Cancelled",
            f"Dear {order.user},\n\n"
            f"Your order has been cancelled!\n"
            f"Here are the details:\n"
            f"- Item Name: {order.item.item_name}\n"
            f"- Quantity: {order.quantity}\n"
            f"- Price: ₹{order.item.item_price} x {order.quantity} = ₹{order.item.item_price * order.quantity}\n\n"
            f"We're sorry to see you go! If you ever change your mind, we'll be here to welcome you back.",
            'vedangrane430@gmail.com',  # Your email address
            [user.email],  # Send to the user's email
        )
        messages.success(request, 'Order cancelled successfully!')
        return redirect('watch:myorders')  # Redirect to 'myorders' after cancellation
    
    # Render the order cancellation page if GET request
    context = {'order': order}
    return render(request, 'watch/cancel_order.html', context)


def create_orders_from_cart(request, cart_items):
    user = request.user
    orders_created = []

    for cart_item in cart_items:
        order = create_order(cart_item, user, request)
        if order:
            orders_created.append(order)

    return orders_created


