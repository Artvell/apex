# Generated by Django 2.1.3 on 2019-03-02 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0003_auto_20190302_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pizzerias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название пиццерии')),
            ],
            options={
                'verbose_name': 'Пиццерия',
                'verbose_name_plural': 'Пиццерии',
            },
        ),
        migrations.AlterModelOptions(
            name='roles',
            options={'verbose_name': 'Роль', 'verbose_name_plural': 'Роли'},
        ),
        migrations.AddField(
            model_name='roles',
            name='place',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='roles.Pizzerias', verbose_name='Пиццерия'),
        ),
    ]
