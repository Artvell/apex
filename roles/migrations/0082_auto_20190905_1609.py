# Generated by Django 2.2.5 on 2019-09-05 11:09

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0081_auto_20190902_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneys',
            name='types',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='roles.Types_of_money', verbose_name='Тип'),
        ),
        migrations.CreateModel(
            name='Products_Consumption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.IntegerField(verbose_name='Всего дней')),
                ('consumption', jsonfield.fields.JSONField(verbose_name='Расход')),
                ('name', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='roles.Products', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Расход продуктов',
                'verbose_name_plural': 'Расход продуктов',
            },
        ),
    ]