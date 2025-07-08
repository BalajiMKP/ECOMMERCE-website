from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order, _ = Order.objects.get_or_create(user=request.user, ordered=False)
    item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    order = Order.objects.filter(user=request.user, ordered=False).first()
    return render(request, 'store/cart_detail.html', {'order': order})

@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user, ordered=False).first()
    if order:
        order.ordered = True
        order.save()
    return render(request, 'store/checkout.html', {'order': order})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})
