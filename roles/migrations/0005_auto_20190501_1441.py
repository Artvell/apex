# Generated by Django 2.2 on 2019-05-01 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0004_auto_20190501_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='nak_id',
            field=models.IntegerField(max_length=50, verbose_name='Номер накладной'),
        ),
    ]
