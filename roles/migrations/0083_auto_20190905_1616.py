# Generated by Django 2.2.5 on 2019-09-05 11:16

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0082_auto_20190905_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products_consumption',
            name='consumption',
            field=jsonfield.fields.JSONField(default=[0], verbose_name='Расход'),
        ),
    ]
