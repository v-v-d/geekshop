def user_basket(request):
    return {'user_basket': request.user.basket.all()} if request.user.is_authenticated else {'user_basket': []}


# def products_total_quantity(request):
#     return {'products_total_quantity': request.user.basket.get_products_total_price_by_user}
#     # return {'products_total_quantity': user_basket(request.user)[0].get_products_total_quantity_by_user}
#
#
# def products_total_price(request):
#     return {'products_total_price': request.user.basket.get_products_total_price_by_user}
#     # return {'products_total_price': user_basket(request.user)[0].get_products_total_price_by_user}
