# Generated by Django 2.2.5 on 2019-10-12 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0086_auto_20190910_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nakl_for_zagot',
            name='user',
        ),
    ]
