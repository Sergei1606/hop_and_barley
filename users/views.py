from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from .forms import (
    UserRegisterForm,
    UserLoginForm,
    UserUpdateForm,
    ProfileUpdateForm,
    DeliveryAddressForm
)
# from orders.models import Order
from .models import DeliveryAddress


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Автоматический вход после регистрации
            login(request, user)

            messages.success(
                request,
                f'Аккаунт создан для {user.username}! '
                f'Теперь вы вошли в систему.'
            )
            return redirect('users:profile')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')

                # Редирект на следующую страницу или профиль
                next_page = request.GET.get('next', 'users:profile')
                return redirect(next_page)
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('products:product_list')


@login_required
def profile(request):
    user = request.user
    # orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
    # Временно пустой список заказов
    orders = []

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=user.profile if hasattr(user, 'profile') else None
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль обновлен!')
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(
            instance=user.profile if hasattr(user, 'profile') else None
        )

    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'orders': orders,
    })


@login_required
def order_history(request):
    # orders = Order.objects.filter(user=request.user).order_by('-created_at')
    # Временно возвращаем пустой список
    orders = []
    return render(request, 'users/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    # order = Order.objects.get(id=order_id, user=request.user)
    # return render(request, 'users/order_detail.html', {'order': order})
    # Временно редирект или сообщение
    messages.info(request, 'История заказов временно недоступна')
    return redirect('users:profile')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('users:profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'users/change_password.html', {'form': form})


@login_required
def addresses(request):
    addresses_list = DeliveryAddress.objects.filter(user=request.user)

    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Адрес добавлен!')
            return redirect('users:addresses')
    else:
        form = DeliveryAddressForm()

    return render(request, 'users/addresses.html', {
        'addresses': addresses_list,
        'form': form,
    })


@login_required
def delete_address(request, address_id):
    address = DeliveryAddress.objects.get(id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Адрес удален!')
    return redirect('users:addresses')