# Generated by Django 2.2 on 2019-05-04 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0010_auto_20190504_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='min_srok',
        ),
    ]
