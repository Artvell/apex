# Generated by Django 2.2 on 2019-05-28 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0017_auto_20190528_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='ingr',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='ingr', to='roles.Products', verbose_name='Ингридиент'),
        ),
    ]