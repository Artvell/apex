# Generated by Django 2.2 on 2019-06-06 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0021_delete_nakl_money'),
    ]

    operations = [
        migrations.CreateModel(
            name='Money_receivers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
            ],
        ),
    ]
