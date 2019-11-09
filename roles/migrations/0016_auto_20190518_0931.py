# Generated by Django 2.2 on 2019-05-18 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0015_auto_20190511_1145'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='postavsh',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='zakupshiki',
            name='name',
            field=models.OneToOneField(limit_choices_to={'prigot': False}, on_delete=django.db.models.deletion.PROTECT, to='roles.Products', verbose_name='Продукт'),
        ),
        migrations.CreateModel(
            name='Salers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_cost', models.FloatField(default=0.0, verbose_name='Последняя цена')),
                ('product', models.ForeignKey(limit_choices_to={'prigot': False}, on_delete=django.db.models.deletion.PROTECT, to='roles.Products', verbose_name='Продукт')),
                ('saler', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='roles.Postavsh', verbose_name='Продавец')),
            ],
            options={
                'verbose_name': 'Продавец',
                'verbose_name_plural': 'Продавцы',
            },
        ),
    ]