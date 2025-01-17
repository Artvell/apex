# Generated by Django 2.2 on 2019-08-27 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0077_zagot_products'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='zagot_products',
            options={'verbose_name': 'Списано заготовщику', 'verbose_name_plural': 'Списано заготовщику'},
        ),
        migrations.CreateModel(
            name='Harvester_Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kol', models.FloatField(verbose_name='Кол-во')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='roles.Products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='roles.Zagot_types', verbose_name='Заготовщик')),
            ],
            options={
                'verbose_name': 'Склад заготовщика',
                'verbose_name_plural': 'Склад заготовщика',
            },
        ),
    ]
