# Generated by Django 2.1.3 on 2019-03-05 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0010_auto_20190305_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='edizm',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='roles.Units', verbose_name='Ед.измерения'),
        ),
    ]