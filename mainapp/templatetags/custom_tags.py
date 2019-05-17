from django import template
from django.conf import settings

register = template.Library()


@register.filter
def get_products_total_price_by_user(user):
    if user.is_anonymous:
        return 0
    else:
        items = user.basket.select_related('product').all()
        return sum([item.product.price * item.quantity for item in items])


@register.filter
def get_products_total_quantity_by_user(user):
    if user.is_anonymous:
        return 0
    else:
        items = user.basket.select_related('product').all()
        return sum([item.quantity for item in items])


def media_folder_products(string, settings=None):
    if not string:
        string = 'products_images/default.svg'
    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='media_folder_users')
def media_folder_users(string):
    if not string:
        string = 'users_avatars/default.svg'
    return f'{settings.MEDIA_URL}{string}'


register.filter('media_folder_products', media_folder_products)
