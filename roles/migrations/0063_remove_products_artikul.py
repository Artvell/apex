# Generated by Django 2.2 on 2019-08-08 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0062_products_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='artikul',
        ),
    ]
