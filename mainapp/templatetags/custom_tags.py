from django import template

register = template.Library()


@register.filter
def get_products_total_price_by_user(user):
    if user.is_anonymous:
        return 0
    else:
        items = user.basket.select_related('product').all()
        return sum([item.product.price*item.quantity for item in items])


@register.filter
def get_products_total_quantity_by_user(user):
    if user.is_anonymous:
        return 0
    else:
        items = user.basket.select_related('product').all()
        return sum([item.quantity for item in items])
