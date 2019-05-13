from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.core.files.base import ContentFile
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        api_url = urlunparse(('https',
                              'api.vk.com',
                              '/method/users.get',
                              None,
                              urlencode(OrderedDict(fields=','.join((
                                  'bdate',
                                  'sex',
                                  'about',
                                  'country',
                                  'photo_200',
                                  'domain'
                              )),
                                access_token=response['access_token'],
                                v='5.92')),
                              None
                              ))

        resp = requests.get(api_url)

        if resp.status_code == 200:

            data = resp.json()['response'][0]
            if data.get('sex', None) and data['sex'] != 0:
                if data['sex'] == 2:
                    user.shopuserprofile.gender = ShopUserProfile.MALE
                else:
                    user.shopuserprofile.gender = ShopUserProfile.FEMALE

            if data.get('about', None):
                user.shopuserprofile.aboutMe = data['about']

            if data.get('bdate', None):
                bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
                age = timezone.now().date().year - bdate.year
                if age < 18:
                    user.delete()
                    raise AuthForbidden('social_core.backends.vk.VKOAuth2')

            if data.get('domain', None):
                user.shopuserprofile.user_url = f'https://vk.com/{data["domain"]}'

            if data.get('country', None):
                user.shopuserprofile.user_lang = data['country']['title']

            if data.get('photo_200', None):
                user.avatar.delete() if user.avatar else None
                user.avatar.save(f"pk_{user.pk}_photo.jpg", ContentFile(requests.get(data['photo_200']).content))

    if backend.name == 'google-oauth2':
        # keys = {'gender', 'tagline', 'aboutMe', 'ageRange'}
        # for key in keys:
        #     user.shopuserprofile.key = response[key] if key in response.keys() else

        if 'gender' in response.keys():
            if response['gender'] == 'male':
                user.shopuserprofile.gender = ShopUserProfile.MALE
            else:
                user.shopuserprofile.gender = ShopUserProfile.FEMALE

        if 'tagline' in response.keys():
            user.shopuserprofile.tagline = response['tagline']

        if 'ageRange' in response.keys():
            min_age = response['ageRange']['min']
            if int(min_age) < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.google.GoogleOAuth2')

    user.save()
