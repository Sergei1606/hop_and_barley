from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.profile, name='profile'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('change-password/', views.change_password, name='change_password'),
    path('addresses/', views.addresses, name='addresses'),
    path('addresses/delete/<int:address_id>/', views.delete_address, name='delete_address'),
]