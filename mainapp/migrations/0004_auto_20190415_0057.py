# Generated by Django 2.1.7 on 2019-04-14 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_productcategory_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
    ]
