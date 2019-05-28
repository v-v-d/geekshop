from django.db import models


class ProductCategory(models.Model):
    class Meta:
        verbose_name = 'Product category'
        verbose_name_plural = 'Product categories'

    name = models.CharField(verbose_name='Category name', max_length=64, unique=True)
    description = models.TextField(verbose_name='Category description', blank=True)
    is_active = models.BooleanField(verbose_name='active', db_index=True, default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Product name', max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(verbose_name='Product short description', max_length=60, blank=True)
    description = models.TextField(verbose_name='Product description', blank=True)
    price = models.DecimalField(verbose_name='Product price', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='Product quantity in stock', default=0)
    is_active = models.BooleanField(verbose_name='active', db_index=True, default=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')


class Contacts(models.Model):
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    name = models.CharField(verbose_name='Location name', max_length=128)
    phone = models.CharField(verbose_name='Phone', max_length=32)
    email = models.EmailField(verbose_name='email', unique=True)
    address = models.CharField(verbose_name='Address', max_length=256)
    is_active = models.BooleanField(verbose_name='active', default=True)

    def __str__(self):
        return self.name
