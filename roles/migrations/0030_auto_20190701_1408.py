# Generated by Django 2.2 on 2019-07-01 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roles', '0029_auto_20190622_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nakl_money_other',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Кому')),
                ('for_why', models.TextField(verbose_name='Зачем')),
                ('kolvo', models.FloatField(verbose_name='Сколько')),
            ],
            options={
                'verbose_name': 'Выдача денег(не закупщики)',
                'verbose_name_plural': 'Выдача денег(не закупщики)',
            },
        ),
        migrations.CreateModel(
            name='Nakl_money_zakup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kolvo', models.FloatField(verbose_name='Сколько')),
                ('name', models.ForeignKey(limit_choices_to={'roles__role': 3}, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Кому')),
            ],
            options={
                'verbose_name': 'Выдача денег(закупщики)',
                'verbose_name_plural': 'Выдача денег(закупщики)',
            },
        ),
        migrations.AlterField(
            model_name='spis',
            name='nak_id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='ID накладной'),
        ),
        migrations.DeleteModel(
            name='Nakl_money',
        ),
    ]
