# Generated by Django 2.2 on 2019-07-12 03:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0052_auto_20190712_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nakl_for_zagot',
            name='name',
            field=models.ForeignKey(limit_choices_to={'prigot': True}, on_delete=django.db.models.deletion.CASCADE, to='roles.Products', verbose_name='Товар'),
        ),
    ]
