# Generated by Django 2.2 on 2019-05-28 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0016_auto_20190518_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='kolvo',
            field=models.FloatField(verbose_name='Кол-во на 1 удиницу товара'),
        ),
        migrations.AlterField(
            model_name='postavsh',
            name='name',
            field=models.CharField(default='', max_length=20, unique=True, verbose_name='Контактное лицо'),
        ),
    ]
