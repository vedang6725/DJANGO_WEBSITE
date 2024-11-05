from django.shortcuts import render, redirect
from users.forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from watch.models import CartItem
from watch.views import create_orders_from_cart
from django.http import JsonResponse
import json

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')

            if User.objects.filter(username=username).exists():
                messages.error(
                    request, 'Username already exists. Please choose a different username.')
            else:
                messages.success(
                    request,
                    'Welcome {}, your account has been successfully created. Now you may log in'.format(
                        username)
                )
                form.save()
                return redirect('login')

    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)


def login_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.success(
                request,
                'Invalid Login, try again'
            )
            return redirect('login')

        elif user.is_superuser:
            login(request, user)
            messages.success(
                request,
                'Welcome Superuser {}, you have been successfully logged in'.format(
                    request.user.username)
            )
            return redirect('watch:index')

        elif user is not None:
            login(request, user)
            messages.success(
                request,
                'Welcome {}, you have been successfully logged in'.format(
                    request.user.username)
            )
            return redirect('watch:index')

    return render(request, 'users/login.html')


def logout_view(request):

    if request.method == 'POST':
        messages.success(
            request,
            '{}, you have been successfully logged out'.format(
                request.user.username)
        )
        logout(request)

        return redirect('watch:index')
    return render(request, 'users/logout.html')


@login_required
def profilepage(request):
    return render(request, 'users/profile.html')


def payment_view(request, grand_total):
    context = {
        'grand_total': grand_total,
    }

    return render(request, 'users/payment.html', context)


def OnApprove(request):

    if request.method == 'POST':
        body = json.loads(request.body)
        print(body)

        context = {

        }

        return JsonResponse(context)


def PaymentSuccess(request):
    cart_items = CartItem.objects.filter(user=request.user)

    orders_created = create_orders_from_cart(request, cart_items)

    cart_items.delete()

    return render(request, 'users/pymtsuccess.html', {'orders_created': orders_created})
