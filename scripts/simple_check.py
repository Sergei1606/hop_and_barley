# simple_check.py
from products.models import Product

print("=== PRODUCT CHECK ===")
products = Product.objects.all()
print(f"Total products: {products.count()}")

for p in products:
    print(f"\nProduct ID: {p.id}")
    print(f"Name: {p.name}")
    print(f"Price: {p.price}")
    print(f"Price type: {type(p.price)}")
    print(f"Category: {p.category}")
    print(f"Active: {p.is_active}")
    print(f"Has image: {bool(p.image)}")
    
    # Проверим все поля
    print("All fields:")
    for field in p._meta.fields:
        field_name = field.name
        field_value = getattr(p, field_name)
        print(f"  {field_name}: {field_value}")
