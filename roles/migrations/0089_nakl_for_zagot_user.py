# Generated by Django 2.2.5 on 2019-10-17 03:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roles', '0088_printers'),
    ]

    operations = [
        migrations.AddField(
            model_name='nakl_for_zagot',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Заготовщик'),
        ),
    ]
