from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, DeliveryAddress


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'your@email.com'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Иван'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Иванов'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'ivanov'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется')
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Имя пользователя'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Пароль'
        })
    )


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'avatar', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+7 (XXX) XXX-XX-XX'}),
        }


class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ['title', 'full_name', 'phone', 'country', 'city', 'street', 'house', 'apartment', 'postal_code',
                  'is_primary']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Дом, Работа и т.д.'}),
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Иванов Иван Иванович'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+7 (XXX) XXX-XX-XX'}),
            'country': forms.TextInput(attrs={'class': 'form-input', 'value': 'Россия'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Москва'}),
            'street': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ул. Ленина'}),
            'house': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'д. 10'}),
            'apartment': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'кв. 25'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '123456'}),
        }