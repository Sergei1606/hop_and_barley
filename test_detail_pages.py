# test_detail_pages.py
import requests

test_products = [
    {'name': 'Сидр', 'slug': 'sidr', 'expected_price': '10.00'},
    {'name': 'Saare leib', 'slug': 'saare-leib', 'expected_price': '15.00'},
    {'name': 'Saku', 'slug': 'saku', 'expected_price': '20.00'},
]

for product in test_products:
    url = f'http://localhost:8005/products/{product["slug"]}/'
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            if product["name"] in response.text:
                print(f"✅ {product['name']}: Страница работает")
                if f'${product["expected_price"]}' in response.text:
                    print(f"   ✓ Цена правильная: ${product['expected_price']}")
                else:
                    print(f"   ⚠️  Цена не найдена или неправильная")
            else:
                print(f"⚠️  {product['name']}: Страница загружается, но нет названия товара")
        elif response.status_code == 404:
            print(f"❌ {product['name']}: 404 Not Found")
        else:
            print(f"❌ {product['name']}: Ошибка {response.status_code}")
    except Exception as e:
        print(f"❌ {product['name']}: Ошибка запроса - {e}")
