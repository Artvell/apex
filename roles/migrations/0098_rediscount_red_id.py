# Generated by Django 2.2.5 on 2019-12-18 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0097_rediscount'),
    ]

    operations = [
        migrations.AddField(
            model_name='rediscount',
            name='red_id',
            field=models.IntegerField(default=0, verbose_name='Номер переучета'),
        ),
    ]