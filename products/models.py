from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """Категория товаров"""
    name = models.CharField("Название", max_length=200, db_index=True)
    slug = models.SlugField("URL", max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])


class Product(models.Model):
    """Товар"""
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    name = models.CharField("Название", max_length=200, db_index=True)
    slug = models.SlugField("URL", max_length=200, db_index=True)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField(
        "Цена",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    image = models.ImageField(
        "Изображение",
        upload_to='products/%Y/%m/%d',
        blank=True
    )
    is_active = models.BooleanField("Активен", default=True)
    stock = models.IntegerField("Количество на складе", default=0)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f"{self.name} - {self.price} руб."

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id, self.slug])

    @property
    def is_available(self):
        """Доступен ли товар для покупки"""
        return self.is_active and self.stock > 0