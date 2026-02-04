from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.CharField(max_length=128, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.CharField(max_length=128, unique=True)
    category = models.ForeignKey(to=Category, on_delete=models.SET(None), related_name='products')
    color = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    main_image = models.ImageField(upload_to='products/main/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='product_size')
    size = models.ForeignKey(to=Size, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.size} ({self.stock} in stock) for {self.product}'


class ProductImage(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/extra/')
