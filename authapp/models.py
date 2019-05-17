from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver


def get_activation_key_expires():
    return now() + timedelta(hours=48)


class ShopUser(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(verbose_name='username', max_length=150, validators=[username_validator])
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='age', null=True)
    email = models.EmailField(verbose_name='email', blank=True, unique=True)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=get_activation_key_expires)

    def is_activation_key_expired(self):
        return now() > self.activation_key_expires


class ShopUserProfile(models.Model):
    MALE, FEMALE = 'M', 'F'

    GENDER_CHOICES = (
        (MALE, 'MALE'),
        (FEMALE, 'FEMALE'),
    )

    user = models.OneToOneField(ShopUser, primary_key=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='tags', max_length=128, blank=True)
    aboutMe = models.TextField(verbose_name='about me', max_length=512, blank=True)
    gender = models.CharField(verbose_name='gender', max_length=1, choices=GENDER_CHOICES, blank=True)
    user_url = models.URLField(verbose_name='user url', blank=True)
    user_lang = models.CharField(verbose_name='user language', max_length=50, blank=True)

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)
        else:
            instance.shopuserprofile.save()
