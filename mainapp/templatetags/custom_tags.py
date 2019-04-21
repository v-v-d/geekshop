from django import template

register = template.Library()


@register.filter
def get_products_total_price_by_user(user):
    if user.is_anonymous:
        return 0
    else:
        items = user.basket.select_related('product').all()
        # return sum(list(map(lambda x: x.product.price*x.quantity, items)))
        return sum([items[i].product.price*items[i].quantity for i in range(len(items))])


@register.filter
def get_products_total_quantity_by_user(user):
    if user.is_anonymous:
        return 0
    else:
        items = user.basket.select_related('product').all()
        # return sum(list(map(lambda x: x.product.price*x.quantity, items)))
        return sum([items[i].quantity for i in range(len(items))])
