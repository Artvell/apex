# Generated by Django 2.2 on 2019-09-02 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0080_auto_20190902_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer_balans',
            name='balans',
            field=models.FloatField(default=0.0, verbose_name='Баланс'),
        ),
        migrations.AlterField(
            model_name='buyer_balans',
            name='debt',
            field=models.FloatField(default=0.0, verbose_name='Долг'),
        ),
    ]