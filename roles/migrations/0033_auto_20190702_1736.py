# Generated by Django 2.2 on 2019-07-02 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0032_auto_20190701_1525'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lastcost',
            options={'verbose_name': 'Последняя цена', 'verbose_name_plural': 'Последние цены'},
        ),
        migrations.AddField(
            model_name='spis',
            name='user',
            field=models.CharField(default='-----', max_length=20, verbose_name='Кто'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='nakl_for_zagot',
            name='user',
            field=models.CharField(default='-----', max_length=20, verbose_name='Заготовщик'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='ostat',
            field=models.FloatField(default=0.0, verbose_name='Осталось на складе'),
        ),
    ]
