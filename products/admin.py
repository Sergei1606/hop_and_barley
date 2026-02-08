# products/admin.py ПОСЛЕ изменений:
from django.contrib import admin
from django.db.models import Count, Sum, Q
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    change_list_template = 'admin/products/product/change_list.html'
    list_display = ['name', 'slug', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'category']
    list_editable = ['price', 'stock', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

    # ДОБАВЛЯЕМ аналитику
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Общая статистика товаров
        total_products = Product.objects.count()
        active_products = Product.objects.filter(is_active=True).count()
        low_stock = Product.objects.filter(stock__lt=10, stock__gt=0).count()
        out_of_stock = Product.objects.filter(stock=0).count()

        # Топ продаваемых товаров
        try:
            from orders.models import OrderItem
            top_selling = Product.objects.annotate(
                total_sold=Sum('orderitem__quantity', default=0)
            ).order_by('-total_sold')[:10]
        except Exception:
            top_selling = Product.objects.none()

        # Статистика по категориям
        categories_stats = Category.objects.annotate(
            product_count=Count('products'),
            active_count=Count('products', filter=Q(products__is_active=True))
        )[:10]

        # Топ по выручке
        revenue_stats = []
        try:
            from orders.models import OrderItem
            products_with_orders = Product.objects.filter(
                orderitem__isnull=False
            ).distinct()

            for product in products_with_orders[:10]:
                total_revenue = OrderItem.objects.filter(
                    product=product
                ).aggregate(
                    total=Sum('price')
                )['total'] or 0

                if total_revenue > 0:
                    revenue_stats.append({
                        'product': product.name,
                        'revenue': float(total_revenue)
                    })
        except Exception:
            revenue_stats = []

        # Сортируем по выручке
        revenue_stats.sort(key=lambda x: x['revenue'], reverse=True)

        # Добавляем данные в контекст
        extra_context.update({
            'total_products': total_products,
            'active_products': active_products,
            'low_stock': low_stock,
            'out_of_stock': out_of_stock,
            'top_selling': top_selling,
            'categories_stats': categories_stats,
            'revenue_stats': revenue_stats,
        })

        return super().changelist_view(request, extra_context=extra_context)

    # ДОБАВЛЯЕМ actions для массовых операций
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Активировано {updated} товаров')

    make_active.short_description = "Активировать выбранные товары"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Деактивировано {updated} товаров')

    make_inactive.short_description = "Деактивировать выбранные товары"