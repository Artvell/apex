# Generated by Django 2.2 on 2019-07-02 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0034_spis_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='spis',
            name='id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='spis',
            name='nak_id',
            field=models.IntegerField(verbose_name='ID накладной'),
        ),
    ]
