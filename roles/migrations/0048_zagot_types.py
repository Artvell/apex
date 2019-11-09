# Generated by Django 2.2 on 2019-07-07 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roles', '0047_nakl_money_other_types'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zagot_types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(limit_choices_to={'prigot': True}, on_delete=django.db.models.deletion.PROTECT, to='roles.Products', verbose_name='Продукт')),
                ('user', models.ForeignKey(limit_choices_to={'roles__role': 4}, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Заготовщик')),
            ],
            options={
                'verbose_name': 'Заготовщик',
                'verbose_name_plural': 'Заготовщики',
            },
        ),
    ]