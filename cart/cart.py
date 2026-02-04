from decimal import Decimal
from products.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id, quantity=1):
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(self.get_product_price(product_id))
            }

        self.cart[product_id]['quantity'] += quantity

        # Не даем добавить больше чем есть на складе
        product = Product.objects.get(id=product_id)
        if self.cart[product_id]['quantity'] > product.stock:
            self.cart[product_id]['quantity'] = product.stock

        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            product = Product.objects.get(id=product_id)
            if quantity > product.stock:
                quantity = product.stock
            self.cart[product_id]['quantity'] = quantity
            self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def get_total_items(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_items(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        items = []
        for product in products:
            item = self.cart[str(product.id)]
            item['product'] = product
            item['total_price'] = Decimal(item['price']) * item['quantity']
            items.append(item)

        return items

    def get_product_price(self, product_id):
        try:
            product = Product.objects.get(id=product_id)
            return product.price
        except Product.DoesNotExist:
            return Decimal('0')

    def save(self):
        self.session.modified = True