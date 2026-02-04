from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .cart import Cart
from products.models import Product


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if product.stock > 0:
        cart.add(product_id)
        messages.success(request, f'Товар "{product.name}" добавлен в корзину')
    else:
        messages.error(request, f'Товар "{product.name}" нет в наличии')

    return redirect('products:product_detail', slug=product.slug)


def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product_id)
    messages.success(request, f'Товар "{product.name}" удален из корзины')
    return redirect('cart:cart_detail')


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, 'Корзина очищена')
    return redirect('cart:cart_detail')