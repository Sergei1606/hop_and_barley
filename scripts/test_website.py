# test_website.py - быстрая проверка сайта
import requests
import time

BASE_URL = "http://localhost:8005"
print("🔍 Тестирование сайта Hop & Barley...")

# 1. роверяем главную страницу
try:
    response = requests.get(BASE_URL + "/", timeout=5)
    print(f"✅ лавная страница: {response.status_code}")
    
    # роверяем наличие ключевых элементов
    html = response.text
    checks = [
        ("Hop & Barley", "азвание сайта"),
        ("product-card", "арточки товаров"),
        ("btn-add-cart", "нопки корзины"),
        ("header-container", "Шапка сайта"),
        ("footer-container", "одвал сайта")
    ]
    
    for text, description in checks:
        if text in html:
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description}")
            
except Exception as e:
    print(f"❌ шибка: {e}")

# 2. роверяем статические файлы
static_files = [
    "/static/css/main.css",
    "/static/js/main.js",
    "/static/img/logo.svg"
]

print(f"\n📁 роверка статических файлов:")
for file in static_files:
    try:
        response = requests.get(BASE_URL + file, timeout=3)
        size_kb = len(response.content) / 1024
        print(f"   ✅ {file} ({size_kb:.1f} KB)")
    except:
        print(f"   ❌ {file}")

print("\n🎯 Тестирование завершено!")
print(f"\n🌐 ткройте в браузере: {BASE_URL}")
