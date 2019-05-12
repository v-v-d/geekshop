from django.core.management.base import BaseCommand
from authapp.models import ShopUser, ShopUserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        to_update = ShopUser.objects.filter(shopuserprofile__isnull=True)
        [ShopUserProfile.objects.create(user=user) for user in to_update]
