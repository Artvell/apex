# Generated by Django 2.2 on 2019-07-01 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roles', '0030_auto_20190701_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='purchase',
            field=models.ForeignKey(limit_choices_to={'roles__role': 3}, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Закупщик'),
        ),
    ]
