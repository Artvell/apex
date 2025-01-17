# Generated by Django 2.2.5 on 2019-10-29 02:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0092_auto_20191019_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nakl_for_zagot',
            name='user',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='roles.Zagot_types', verbose_name='Заготовщик'),
        ),
        migrations.AlterField(
            model_name='zagot_products',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Принято?'),
        ),
    ]
