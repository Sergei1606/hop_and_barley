from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'get_total')
    fields = ('product', 'quantity', 'price', 'get_total')

    def get_total(self, obj):
        return obj.get_total()

    get_total.short_description = 'Сумма'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = 'admin/orders/order/change_list.html'
    list_display = ('id', 'user', 'status', 'total_price', 'created_at', 'items_count')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'email', 'phone', 'shipping_address')
    readonly_fields = ('created_at', 'updated_at', 'total_price_display')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'status', 'total_price_display')
        }),
        ('Информация о доставке', {
            'fields': ('shipping_address', 'phone', 'email')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def items_count(self, obj):
        return obj.items.count()

    items_count.short_description = 'Товаров'

    def total_price_display(self, obj):
        return f'{obj.total_price} руб.'

    total_price_display.short_description = 'Общая сумма'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'get_total_display')
    list_filter = ('order__status',)
    search_fields = ('product__name', 'order__id')

    def get_total_display(self, obj):
        return f'{obj.get_total()} руб.'

    get_total_display.short_description = 'Сумма'