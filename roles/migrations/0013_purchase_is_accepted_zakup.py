# Generated by Django 2.2 on 2019-05-07 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0012_purchase_min_srok'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='is_accepted_zakup',
            field=models.BooleanField(default=False, verbose_name='Накладная принята закупщиком?'),
        ),
    ]
