def user_basket(request):
    return {'user_basket': request.user.basket.all() if request.user.is_authenticated else []}
