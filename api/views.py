from django.shortcuts import render

# Create your views here.
# api/views.py
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import transaction

from .serializers import (
    UserSerializer, RegisterSerializer,
    CategorySerializer, ProductSerializer,
    OrderSerializer, OrderItemSerializer,
    CartSerializer, ProfileSerializer, DeliveryAddressSerializer
)
from products.models import Category, Product
from orders.models import Order, OrderItem
from users.models import UserProfile as Profile, DeliveryAddress
from cart.cart import Cart


# ===== USER VIEWS =====
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        if self.kwargs.get('pk') == 'me':
            return self.request.user
        return super().get_object()


# ===== PRODUCT VIEWS =====
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)

        # Фильтрация по категории
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Поиск
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)

        # Сортировка
        sort = self.request.query_params.get('sort', 'created_at')
        if sort in ['price', '-price', 'name', '-name', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort)

        return queryset


# ===== ORDER VIEWS =====
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().select_related('user').prefetch_related('items')
        return Order.objects.filter(user=self.request.user).select_related('user').prefetch_related('items')

    def perform_create(self, serializer):
        cart = Cart(self.request)

        with transaction.atomic():
            # Создаем заказ
            order = serializer.save(
                user=self.request.user,
                total_price=cart.get_total_price()
            )

            # Создаем позиции заказа
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )

            # Очищаем корзину
            cart.clear()


# ===== CART VIEWS =====
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart(request)
        serializer = CartSerializer({
            'items': list(cart),
            'total_items': cart.get_total_items(),
            'total_price': cart.get_total_price()
        })
        return Response(serializer.data)

    def post(self, request):
        cart = Cart(request)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id, is_active=True, stock__gte=quantity)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Товар не найден или недостаточно на складе'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart.add(product, quantity)
        return Response({'success': True, 'message': 'Товар добавлен в корзину'})

    def delete(self, request):
        product_id = request.data.get('product_id')
        cart = Cart(request)

        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                cart.remove(product)
                return Response({'success': True, 'message': 'Товар удален из корзины'})
            except Product.DoesNotExist:
                return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)
        else:
            cart.clear()
            return Response({'success': True, 'message': 'Корзина очищена'})


# ===== PROFILE VIEWS =====
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


class DeliveryAddressViewSet(viewsets.ModelViewSet):
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DeliveryAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)