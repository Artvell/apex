# Generated by Django 2.2 on 2019-07-02 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0037_spis_nak_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spis',
            name='nak_id',
        ),
    ]