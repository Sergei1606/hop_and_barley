# config/context_processors.py - ОБЪЕДИНЕННАЯ ВЕРСИЯ
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import datetime


def admin_stats(request):
    """Контекст-процессор для статистики в админке (ваша версия + дополнения)"""
    if request.path.startswith('/admin/'):
        try:
            from orders.models import Order, OrderItem
            from products.models import Product
            from django.contrib.auth.models import User

            # ===== ВАША СТАТИСТИКА =====
            # Статистика заказов
            order_stats = {
                'total': Order.objects.count(),
                'by_status': []
            }

            status_choices = {
                'pending': ('🕒 Ожидает', '#ffc107'),
                'paid': ('💰 Оплачен', '#28a745'),
                'shipped': ('🚚 Отправлен', '#007bff'),
                'delivered': ('✅ Доставлен', '#20c997'),
                'cancelled': ('❌ Отменен', '#dc3545'),
            }

            for status, (display, color) in status_choices.items():
                count = Order.objects.filter(status=status).count()
                if count > 0:
                    order_stats['by_status'].append({
                        'status': status,
                        'status_display': display,
                        'count': count,
                        'color': color
                    })

            # Статистика продуктов
            product_stats = {
                'total': Product.objects.count(),
                'active': Product.objects.filter(is_active=True).count(),
                'low_stock': Product.objects.filter(stock__lt=10, stock__gt=0).count(),
                'out_of_stock': Product.objects.filter(stock=0).count(),
            }

            # Статистика пользователей
            user_stats = {
                'total': User.objects.count(),
                'active': User.objects.filter(is_active=True).count(),
                'staff': User.objects.filter(is_staff=True).count(),
                'superusers': User.objects.filter(is_superuser=True).count(),
            }

            # Финансовая статистика
            today = timezone.now().date()
            today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))

            revenue_agg = Order.objects.aggregate(total_revenue=Sum('total_price'))
            total_revenue = revenue_agg['total_revenue'] or 0

            total_orders = Order.objects.count()
            avg_order = total_revenue / total_orders if total_orders > 0 else 0

            today_orders = Order.objects.filter(created_at__gte=today_start)
            today_revenue = today_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

            finance_stats = {
                'total_revenue': total_revenue,
                'avg_order': avg_order,
                'today_orders': today_orders.count(),
                'today_revenue': today_revenue,
            }

            # ===== ДОПОЛНИТЕЛЬНАЯ СТАТИСТИКА ДЛЯ DASHBOARD =====
            # Последние заказы
            recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]

            # Популярные товары
            popular_products = Product.objects.annotate(
                total_sold=Sum('orderitem__quantity', default=0),
                total_revenue=Sum('orderitem__price', default=0)
            ).order_by('-total_sold')[:5]

            # Статусы заказов (отдельные переменные для шаблона)
            pending_orders = Order.objects.filter(status='pending').count()
            paid_orders = Order.objects.filter(status='paid').count()
            shipped_orders = Order.objects.filter(status='shipped').count()
            delivered_orders = Order.objects.filter(status='delivered').count()
            cancelled_orders = Order.objects.filter(status='cancelled').count()

            return {
                # Ваши данные
                'order_stats': order_stats,
                'product_stats': product_stats,
                'user_stats': user_stats,
                'finance_stats': finance_stats,

                # Данные для dashboard шаблона
                'total_orders': order_stats['total'],
                'total_products': product_stats['total'],
                'total_users': user_stats['total'],
                'total_revenue': total_revenue,
                'avg_order_value': round(avg_order, 2),
                'pending_orders': pending_orders,
                'paid_orders': paid_orders,
                'shipped_orders': shipped_orders,
                'delivered_orders': delivered_orders,
                'cancelled_orders': cancelled_orders,
                'recent_orders': recent_orders,
                'popular_products': popular_products,
            }

        except Exception as e:
            # Если что-то пошло не так, возвращаем пустую статистику
            print(f"Error in admin_stats: {e}")
            return {
                'order_stats': {'total': 0, 'by_status': []},
                'product_stats': {'total': 0, 'active': 0, 'low_stock': 0, 'out_of_stock': 0},
                'user_stats': {'total': 0, 'active': 0, 'staff': 0, 'superusers': 0},
                'finance_stats': {'total_revenue': 0, 'avg_order': 0, 'today_orders': 0, 'today_revenue': 0},
                # Пустые данные для dashboard
                'total_orders': 0,
                'total_products': 0,
                'total_users': 0,
                'total_revenue': 0,
                'avg_order_value': 0,
                'pending_orders': 0,
                'paid_orders': 0,
                'shipped_orders': 0,
                'delivered_orders': 0,
                'cancelled_orders': 0,
                'recent_orders': [],
                'popular_products': [],
            }

    return {}