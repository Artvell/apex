# Generated by Django 2.2.5 on 2020-01-19 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0109_auto_20200119_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='without_nakl',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата'),
        ),
    ]
