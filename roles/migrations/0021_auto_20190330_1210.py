# Generated by Django 2.1.7 on 2019-03-30 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0020_stock_shtrih'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='srok',
            field=models.DateField(blank=True, verbose_name='Срок годности'),
        ),
    ]