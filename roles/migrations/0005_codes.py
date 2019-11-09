# Generated by Django 2.2 on 2019-05-01 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0004_delete_codes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Codes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shtrih', models.CharField(default='', editable=False, max_length=50, verbose_name='Штрих-код')),
                ('kolvo', models.FloatField(default=0.0, verbose_name='Кол-во')),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='roles.Products', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Штрих код',
                'verbose_name_plural': 'Штрих коды',
            },
        ),
    ]