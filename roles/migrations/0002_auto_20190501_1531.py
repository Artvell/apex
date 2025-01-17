# Generated by Django 2.2 on 2019-05-01 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='purchase',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='products',
            name='artikul',
        ),
        migrations.RemoveField(
            model_name='products',
            name='scena',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='shtrih',
        ),
        migrations.AddField(
            model_name='codes',
            name='kolvo',
            field=models.FloatField(default=0.0, verbose_name='Кол-во'),
        ),
        migrations.AlterField(
            model_name='nakl_for_zagot',
            name='name',
            field=models.ForeignKey(limit_choices_to={'prigot': True}, on_delete=django.db.models.deletion.PROTECT, to='roles.Products', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='products',
            name='rashod',
            field=models.IntegerField(default=1, verbose_name='Ср.расход в день'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='fact_kol',
            field=models.FloatField(default=0.0, verbose_name='Фактическое кол-во'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='is_accepted',
            field=models.BooleanField(default=False, verbose_name='Накладная принята?'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='is_delivered',
            field=models.BooleanField(default=False, verbose_name='Поступил на склад?'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='min_srok',
            field=models.DateField(null=True, verbose_name='Мин.срок годности'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='nak_id',
            field=models.IntegerField(verbose_name='Номер накладной'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='roles.Products', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='new_cost',
            field=models.FloatField(default=0.0, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='purchased_kol',
            field=models.FloatField(default=0.0, verbose_name='Купленное кол-во'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='srok',
            field=models.DateField(null=True, verbose_name='Cрок годности'),
        ),
        migrations.CreateModel(
            name='LastCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.FloatField(default=0.0, verbose_name='Последняя цена')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='roles.Products', verbose_name='Продукт')),
            ],
        ),
    ]
