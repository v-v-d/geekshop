from django.db import models

from django.conf import settings
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCELED = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'forming'),
        (SENT_TO_PROCEED, 'sent to proceed'),
        (PAID, 'paid'),
        (PROCEEDED, 'proceeded'),
        (READY, 'ready'),
        (CANCELED, 'canceled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='created', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='updated', auto_now=True)
    status = models.CharField(verbose_name='status', max_length=3, choices=ORDER_STATUS_CHOICES, default=FORMING)
    is_active = models.BooleanField(verbose_name='is active', db_index=True, default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f'Current order: {self.id}'

    def get_total_quantity(self):
        return sum(self.orderitems.values_list('quantity', flat=True))

    def get_product_type_quantity(self):
        return self.orderitems.count()

    def get_total_cost(self):
        return sum([i.quantity * i.product.price for i in self.orderitems.select_related()])

    # переопределяем метод, удаляющий объект
    def delete(self):
        for item in self.orderitems.all():
            item.product.quantity += item.quantity
            item.product.save()

        self.status, self.is_active = 'CNC', False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="orderitems", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='quantity', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return __class__.objects.filter(pk=pk).first()
