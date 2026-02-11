# fix_prices.py
from products.models import Product
from decimal import Decimal

print("=== FIXING PRICES ===")
products = Product.objects.all()
updated_count = 0

# Примерные цены для товаров
default_prices = {
    'Сидр': Decimal('5.99'),
    'Saare leib': Decimal('3.49'), 
    'Saku': Decimal('4.99')
}

for p in products:
    print(f"\nChecking: {p.name}")
    print(f"Current price: {p.price}")
    
    # Если цена None или 0
    if p.price is None or p.price == 0:
        # Пытаемся найти цену по имени
        new_price = default_prices.get(p.name, Decimal('9.99'))
        p.price = new_price
        p.save()
        updated_count += 1
        print(f"Updated price to: {new_price}")
    else:
        print("Price OK")

print(f"\n✅ Updated {updated_count} products")
print("Final check:")
for p in Product.objects.all():
    print(f"  - {p.name}: ${p.price}")
