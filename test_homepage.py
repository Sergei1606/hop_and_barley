# test_homepage.py
import requests

try:
    response = requests.get('http://localhost:8005/', timeout=5)
    print(f"✅ Статус главной страницы: {response.status_code}")
    
    # Проверим есть ли товары в ответе
    content = response.text
    if 'Showing' in content and 'products from database' in content:
        print("✅ Динамические данные загружаются")
    
    # Простые проверки
    checks = [
        ('ProductListView', 'View загружен'),
        ('add-to-cart-btn', 'Кнопки корзины'),
        ('data-product-id', 'ID товаров'),
    ]
    
    for text, description in checks:
        if text in content:
            print(f"✅ {description}: найдено")
        else:
            print(f"⚠️  {description}: не найдено")
            
except Exception as e:
    print(f"❌ Ошибка: {e}")
