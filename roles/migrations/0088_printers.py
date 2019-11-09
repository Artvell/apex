# Generated by Django 2.2.5 on 2019-10-15 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0087_remove_nakl_for_zagot_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Printers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('ip_address', models.CharField(max_length=15, verbose_name='IP адрес')),
            ],
            options={
                'verbose_name': 'IP принтер',
                'verbose_name_plural': 'IP принтеры',
            },
        ),
    ]