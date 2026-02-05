from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'phone', 'email']
        widgets = {
            'shipping_address': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Введите полный адрес доставки: город, улица, дом, квартира',
                'class': 'form-input'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+7 (XXX) XXX-XX-XX',
                'class': 'form-input'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your@email.com',
                'class': 'form-input'
            }),
        }
        labels = {
            'shipping_address': 'Адрес доставки',
            'phone': 'Телефон для связи',
            'email': 'Email для уведомлений',
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # Простая валидация телефона
        if len(phone) < 5:
            raise forms.ValidationError('Введите корректный номер телефона')
        return phone