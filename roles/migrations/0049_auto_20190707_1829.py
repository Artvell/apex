# Generated by Django 2.2 on 2019-07-07 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0048_zagot_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nakl_for_zagot',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='roles.Zagot_types', verbose_name='Заготовщик'),
        ),
    ]