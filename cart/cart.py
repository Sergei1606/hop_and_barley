from django.conf import settings
from products.models import Product


class Cart:
    """Класс для управления корзиной покупок с использованием сессий Django."""

    def __init__(self, request):
        """Инициализация корзины из сессии пользователя."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product_id, quantity=1, update_quantity=False):
        product_id = str(product_id)

        if update_quantity:
            self.cart[product_id] = {'quantity': quantity}
        else:
            if product_id in self.cart:
                self.cart[product_id]['quantity'] += quantity
            else:
                self.cart[product_id] = {'quantity': quantity}

        self.save()

    def remove(self, product_id):
        """Удаляет товар из корзины."""
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        """Сохраняет изменения в сессии."""
        self.session.modified = True

    def __iter__(self):
        """Перебирает товары в корзине и загружает связанные объекты Product."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids, is_active=True)

        cart = self.cart.copy()
        for product in products:
            product_id = str(product.id)
            cart[product_id]['product'] = product
            cart[product_id]['total_price'] = product.price * cart[product_id]['quantity']

        for item in cart.values():
            yield item

    def __len__(self):
        """Возвращает общее количество товаров в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Возвращает общую стоимость корзины."""
        total = 0
        for product_id, item in self.cart.items():
            try:
                product = Product.objects.get(id=int(product_id))
                total += product.price * item['quantity']
            except Product.DoesNotExist:
                continue
        return total

    def clear(self):
        """Очищает корзину."""
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()