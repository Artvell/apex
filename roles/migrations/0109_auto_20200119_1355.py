# Generated by Django 2.2.5 on 2020-01-19 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0108_without_nakl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='without_nakl',
            name='nak_id',
            field=models.IntegerField(default=0, verbose_name='Номер накладной'),
        ),
    ]