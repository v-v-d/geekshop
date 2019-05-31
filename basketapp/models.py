from django.db import models
from django.conf import settings
from mainapp.models import Product
from django.utils.functional import cached_property


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='quantity', default=0)
    add_datetime = models.DateTimeField(verbose_name='datetime', auto_now_add=True)

    @cached_property
    def get_items_cached(self):
        return Basket.objects.filter(user_id=self.user).select_related()

    @property
    def get_product_total_price(self):
        return self.quantity * self.product.price

    @property
    def get_products_total_quantity_by_user(self):
        return sum([item.quantity for item in self.get_items_cached])

    @property
    def get_products_total_price_by_user(self):
        return sum([item.get_product_total_price for item in self.get_items_cached])

    @staticmethod
    def get_item(pk):
        return __class__.objects.filter(pk=pk).first()
