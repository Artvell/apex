# Generated by Django 2.2 on 2019-08-22 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0071_auto_20190822_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nakl_for_zagot',
            name='is_taken',
        ),
    ]
