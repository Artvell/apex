# Generated by Django 2.2.5 on 2020-02-01 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0113_auto_20200126_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='rediscount',
            name='st_kol',
            field=models.FloatField(default=0.0, verbose_name='На складе'),
        ),
    ]
