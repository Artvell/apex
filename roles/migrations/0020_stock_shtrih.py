# Generated by Django 2.1.7 on 2019-03-28 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0019_auto_20190319_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='shtrih',
            field=models.IntegerField(default=0, verbose_name='Штрих-код'),
            preserve_default=False,
        ),
    ]
