Выполнено:
1. Привести магазин к требованиям, которые вы озвучили на уроке.
2. Организовать выдачу сообщения об успешной отправке письма с кодом подтверждения в окне регистрации пользователя.
3. Реализовать активацию пользователя при переходе по ссылке из письма.
4. Создать контекстный процессор для корзины и скорректировать код контроллеров основного приложения.

Проблемы, с которыми я столкнулся:

1 При активации юзера через реальный почтовый сервер я столкнулся с ошибкой. Она возникла при переходе по ссылке из письма
на страницу verification.html. Текст ошибки: You have multiple authentication backends configured and therefore must
provide the `backend` argument or set the `backend` attribute on the user. Погуглив, нашел решение - надо в
authapp/views.py в контроллере verify строку с логином оформить вот так
auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
После этого все волшебным образом заработало. Поясните, пожалуйста, как работает эта магия.

2 Поясните, пожалуйста, почему при указании в settings.py DOMAIN_NAME = 'http://localhost:8000' и указании в настройках
приложения ВК Адрес сайта: http://127.0.0.1:8000 не работает логин через ВК. А если заменить в сэттингах DOMAIN_NAME на
http://127.0.0.1:8000 все работает

3 Если подтверждения ждет несколько юзеров с одной и той же почтой, то вываливается ошибка
error activation user : ('get() returned more than one ShopUser -- it returned 11!',)
где 11 - кол-во юзеров с одинаковой почтой.
Видимо, надо в модели юзера на поле email установить флаг unique = True?

4 Для уведомления юзера о том, что ему на почту пришло письмо я сделал страницу email_confirmation.html. Если контроллеру
register в ветке if register_form.is_valid(): -> if send_verify_mail(user): указать, что надо просто отрендерить страницу
return render(request, 'authapp/email_confirmation.html', {'title': 'email confirmation'})
вываливается ошибка ValueError: The view authapp.views.register didn't return an HttpResponse object. It returned None instead.
Видимо, контроллер ожидает HttpResponse вместо render. Пришлось сделать контроллер и урл для рендера email_confirmation.html.
Поясните, пожалуйста, почему так происходит.

