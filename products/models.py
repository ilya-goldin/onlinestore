from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        null=False,
        verbose_name='Name',
        unique=True,
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Description',
    )
    price = models.IntegerField(
        default=0,
        verbose_name='Price',
        validators=[
            MinValueValidator(0),
        ],
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Date updated',
    )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='User',
        related_name='reviews',
    )
    product = models.ForeignKey(
        Product,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Product',
    )
    review_text = models.TextField(
        blank=True,
        max_length=500,
        verbose_name='Review',
    )
    score = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name='Score',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Date updated',
    )
    
    class Meta:
        unique_together = ('user_id', 'product_id')
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class OrderStatusChoices(models.TextChoices):
    """Order statuses"""

    NEW = 'NEW', 'New'
    IN_PROGRESS = 'IN_PROGRESS', 'In progress'
    DONE = 'DONE', 'Done'


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='User',
        related_name='orders',
    )
    products = models.ManyToManyField(
        Product,
        through='OrderProducts',
        through_fields=('order', 'product'),
        related_name='order',
        verbose_name='Products'
    )
    status = models.TextField(
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.NEW,
    )
    order_value = models.PositiveIntegerField(
        default=0,
        verbose_name='Order Value',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Date updated',
    )

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderProducts(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT,
    )
    qty = models.PositiveIntegerField(
        default=1,
        verbose_name='Qty',
    )


class Collection(models.Model):
    title = models.CharField(
        max_length=150,
        null=False,
        verbose_name='Title',
        unique=True,
    )
    note = models.TextField(
        blank=True,
        verbose_name='Note',
    )
    items = models.ManyToManyField(Product, related_name='items')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Date updated',
    )

    def __str__(self):
        return self.title
