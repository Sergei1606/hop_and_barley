# check_products.py
from products.models import Product

print("=== ТОВАРЫ В БАЗЕ ===")
products = Product.objects.all()
print(f"Всего: {products.count()} товаров")
print()

for p in products:
    print(f"📦 {p.name}")
    print(f"   ID: {p.id}")
    print(f"   Slug: {p.slug}")
    print(f"   Цена: ${p.price}")
    print(f"   Активен: {p.is_active}")
    if p.category:
        print(f"   Категория: {p.category.name}")
    else:
        print(f"   Категория: Без категории")
    print()
