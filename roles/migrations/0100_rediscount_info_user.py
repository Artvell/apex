# Generated by Django 2.2.5 on 2019-12-19 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roles', '0099_auto_20191220_0337'),
    ]

    operations = [
        migrations.AddField(
            model_name='rediscount_info',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Провел'),
        ),
    ]