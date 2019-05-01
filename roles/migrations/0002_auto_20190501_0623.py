# Generated by Django 2.2 on 2019-05-01 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='scena',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='shtrih',
        ),
        migrations.AlterField(
            model_name='products',
            name='artikul',
            field=models.CharField(max_length=6, verbose_name='Артикул'),
        ),
        migrations.AlterField(
            model_name='products',
            name='rashod',
            field=models.IntegerField(default=1, verbose_name='Ср.расход в день'),
        ),
    ]
