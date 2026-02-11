from django.urls import reverse
from django.conf import settings

print('===  URL Я Ш ===')

urls_to_check = [
    ('products:product_list', 'лавная/товары'),
    ('cart:cart_detail', 'орзина'),
    ('users:login', 'ход'),
    ('users:register', 'егистрация'),
    ('users:profile', 'рофиль'),
]

for url_name, description in urls_to_check:
    try:
        url = reverse(url_name)
        print(f'✓ {description}: {url_name} -> {url}')
    except Exception as e:
        print(f'✗ {description}: {url_name} - Ш: {e}')
