from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, DeliveryAddress


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'
    fields = ('phone', 'avatar', 'birth_date', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


class DeliveryAddressInline(admin.TabularInline):
    model = DeliveryAddress
    extra = 0
    fields = ('title', 'full_name', 'phone', 'city', 'street', 'house', 'is_primary')


class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline, DeliveryAddressInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'birth_date', 'created_at')
    search_fields = ('user__username', 'phone')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'city', 'street', 'house', 'is_primary', 'created_at')
    list_filter = ('city', 'is_primary')
    search_fields = ('user__username', 'full_name', 'city', 'street')
    readonly_fields = ('created_at',)


# Перерегистрируем User с кастомным админом
admin.site.unregister(User)
admin.site.register(User, UserAdmin)