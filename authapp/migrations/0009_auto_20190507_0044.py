# Generated by Django 2.1.7 on 2019-05-06 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0008_auto_20190507_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuserprofile',
            name='user_url',
            field=models.URLField(blank=True, verbose_name='user url'),
        ),
    ]
