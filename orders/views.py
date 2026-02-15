from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from .forms import OrderCreateForm
from .models import Order, OrderItem
from products.models import Product
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)

    # Проверяем, что корзина не пуста
    if len(cart) == 0:
        messages.error(request, 'Ваша корзина пуста')
        return redirect('cart:cart_detail')

    # Проверяем наличие товаров на складе
    for item in cart:
        product = item['product']
        quantity = item['quantity']

        if quantity > product.stock:
            messages.error(
                request,
                f'Товара "{product.name}" недостаточно на складе. '
                f'Доступно: {product.stock} шт.'
            )
            return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            try:
                # Делаем копию корзины ДО транзакции
                cart_items = list(cart)

                with transaction.atomic():
                    order = form.save(commit=False)

                    if request.user.is_authenticated:
                        order.user = request.user
                    else:
                        from django.contrib.auth.models import User
                        anonymous_user, created = User.objects.get_or_create(
                            username='anonymous',
                            defaults={'email': 'anonymous@example.com'}
                        )
                        order.user = anonymous_user

                    order.total_price = cart.get_total_price()
                    order.save()

                    # Используем копию корзины
                    for item in cart_items:
                        product = item['product']
                        quantity = item['quantity']

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            price=product.price
                        )

                        product.stock -= quantity
                        product.save()

                    cart.clear()
                    send_order_emails(order, request)

                    messages.success(
                        request,
                        f'Заказ #{order.id} успешно оформлен! '
                        f'На сумму {order.total_price} руб.'
                    )

                    return redirect('orders:order_created', order_id=order.id)

            except Exception as e:
                messages.error(request, f'Ошибка при оформлении заказа: {str(e)}')
                return redirect('cart:cart_detail')

    else:
        # Предзаполняем форму данными
        initial_data = {}
        if request.user.is_authenticated and request.user.email:
            initial_data['email'] = request.user.email

        form = OrderCreateForm(initial=initial_data)

    return render(request, 'orders/order_create.html', {
        'form': form,
        'cart': cart,
    })


def order_created(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Проверяем, что пользователь видит только свои заказы (если авторизован)
    if request.user.is_authenticated and order.user != request.user and order.user.username != 'anonymous':
        messages.error(request, 'У вас нет доступа к этому заказу')
        return redirect('products:product_list')

    return render(request, 'orders/order_created.html', {'order': order})


def send_order_emails(order, request):
    """Отправка email уведомлений"""
    try:
        # 1. Email пользователю
        user_subject = f'Заказ #{order.id} оформлен'
        user_message = f'''
        Здравствуйте, {order.user.username if order.user.username != 'anonymous' else 'клиент'}!

        Ваш заказ #{order.id} успешно оформлен.

        Детали заказа:
        - Номер заказа: #{order.id}
        - Статус: {order.get_status_display()}
        - Сумма: {order.total_price} руб.
        - Адрес доставки: {order.shipping_address}
        - Телефон: {order.phone}

        Спасибо за покупку!

        С уважением,
        Hop & Barley
        '''

        send_mail(
            user_subject,
            user_message,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            fail_silently=True,
        )

        # 2. Email администратору
        admin_subject = f'Новый заказ #{order.id}'
        admin_message = f'''
        Новый заказ от пользователя {order.user.username} ({order.user.email})

        Детали заказа:
        - ID: {order.id}
        - Пользователь: {order.user.username} (ID: {order.user.id})
        - Email: {order.email}
        - Телефон: {order.phone}
        - Адрес: {order.shipping_address}
        - Сумма: {order.total_price} руб.
        - Статус: {order.status}

        Товары:
        {chr(10).join([f"- {item.product.name}: {item.quantity} x {item.price} = {item.get_total()} руб." for item in order.items.all()])}
        '''

        send_mail(
            admin_subject,
            admin_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=True,
        )

    except Exception as e:
        # Логируем ошибку, но не прерываем выполнение
        print(f"Ошибка отправки email: {e}")