# Generated by Django 2.2 on 2019-07-22 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0055_auto_20190712_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='rashod',
            field=models.FloatField(default=1, verbose_name='Ср.расход в день'),
        ),
    ]