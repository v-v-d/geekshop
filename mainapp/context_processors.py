def user_basket(request):
    user_basket = request.user.basket.all().select_related('product__category') if request.user.is_authenticated else []
    return {'user_basket': user_basket}
