# Generated by Django 2.2 on 2019-07-02 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0033_auto_20190702_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='spis',
            name='date',
            field=models.DateField(null=True, verbose_name='Дата'),
        ),
    ]
