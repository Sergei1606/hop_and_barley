from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .cart import Cart
from products.models import Product


def cart_detail(request):
    """Отображение содержимого корзины."""
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if product.stock > 0:
        quantity = 1
        if request.method == 'POST':
            try:
                quantity = int(request.POST.get('quantity', 1))
            except (ValueError, TypeError):
                quantity = 1

        if quantity > product.stock:
            quantity = product.stock
            messages.warning(request, f'Доступно только {product.stock} шт.')

        # Удаляем текущий и добавляем точное количество
        # cart.remove(product_id)
        print(f"🔥 quantity из формы: {quantity}")
        print(f"📦 в корзине ДО: {cart.cart}")
        cart.add(product_id, quantity)
        print(f"📦 в корзине ПОСЛЕ: {cart.cart}")

        messages.success(request, f'Товар "{product.name}" добавлен в корзину ({quantity} шт.)')
    else:
        messages.error(request, f'Товар "{product.name}" нет в наличии')

    return redirect('products:product_detail', slug=product.slug)


def remove_from_cart(request, product_id):
    """Удаление товара из корзины."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product_id)
    messages.success(request, f'Товар "{product.name}" удален из корзины')
    return redirect('cart:cart_detail')


def clear_cart(request):
    """Полная очистка корзины."""
    cart = Cart(request)
    cart.clear()
    messages.success(request, 'Корзина очищена')
    return redirect('cart:cart_detail')