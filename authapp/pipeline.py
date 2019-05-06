from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        api_url = urlunparse(('https',
                              'api.vk.com',
                              '/method/users.get',
                              None,
                              urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'country', 'photo_id')),
                                                    access_token=response['access_token'],
                                                    v='5.92')),
                              None
                              ))

        resp = requests.get(api_url)
        # if resp.status_code != 200:
        #     return

        data = resp.json()['response'][0]
        if data['sex']:
            if data['sex'] == 2:
                user.shopuserprofile.gender = ShopUserProfile.MALE
            else:
                user.shopuserprofile.gender = ShopUserProfile.FEMALE

        if data['about']:
            user.shopuserprofile.aboutMe = data['about']

        if data['bdate']:
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
            age = timezone.now().date().year - bdate.year
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        if data['id']:
            user_id = data['id']
            user.shopuserprofile.user_url = f'https://vk.com/id{user_id}'

        if data['country']:
            user.shopuserprofile.user_lang = data['country']['title']

        if data['photo_id']:
            photo_id = data['photo_id']
            user.shopuserprofile.userpic_url = f'https://vk.com/photo{photo_id}'


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
