from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser


def login(request):
    login_form = ShopUserLoginForm(data=request.POST)

    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main:index'))

    context = {
        'title': 'login',
        'login_form': login_form,
        'next': next,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            # auth.login(request, register_form.save())
            user = register_form.save()
            if send_verify_mail(user):
                # print('сообщение подтверждения отправлено')
                # return render(request, 'authapp/email_confirmation.html', {'title': 'email confirmation'})
                # return HttpResponseRedirect(reverse('auth:register'))
                return HttpResponseRedirect(reverse('auth:email_confirmation'))
            else:
                # print('ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('auth:register'))
                # return HttpResponseRedirect(reverse('main:index'))
    else:
        register_form = ShopUserRegisterForm()
        context = {'title': 'register', 'register_form': register_form}
        return render(request, 'authapp/register.html', context)


def edit(request):
    title = 'edit'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        context = {'title': title, 'edit_form': edit_form}

    return render(request, 'authapp/edit.html', context)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', kwargs={
        'email': user.email,
        'activation_key': user.activation_key,
    })

    title = f'Complete the {user.username} verification'

    message = f'Please click on the link below to complete the verification on {settings.DOMAIN_NAME}:\n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            # auth.login(request, user)
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html', {'title': 'verification'})
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html', {'title': 'verification'})
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('main:index'))


def email_confirmation(request):
    return render(request, 'authapp/email_confirmation.html', {'title': 'email confirmation'})
