# Generated by Django 2.1.7 on 2019-04-28 17:20

import authapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_auto_20190419_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='activation_key',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=authapp.models.get_activation_key_expires),
        ),
    ]
