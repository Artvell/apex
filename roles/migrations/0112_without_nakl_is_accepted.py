# Generated by Django 2.2.5 on 2020-01-26 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0111_codes_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='without_nakl',
            name='is_accepted',
            field=models.BooleanField(default=True, verbose_name='Отправдено'),
        ),
    ]