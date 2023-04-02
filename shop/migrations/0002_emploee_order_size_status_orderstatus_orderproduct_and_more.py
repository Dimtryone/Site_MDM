# Generated by Django 4.1.3 on 2022-12-01 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emploee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_emp', models.CharField(max_length=80)),
                ('surname_emp', models.CharField(max_length=80)),
                ('patronymic_emp', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('payment_method', models.CharField(max_length=80)),
                ('emploee', models.ManyToManyField(to='shop.emploee')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(db_index=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_status', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_strat', models.DateTimeField(auto_now_add=True)),
                ('date_finish', models.DateTimeField(auto_now=True)),
                ('flag_finish', models.BooleanField(default=False)),
                ('name_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.status')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(through='shop.OrderProduct', to='shop.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ManyToManyField(through='shop.OrderStatus', to='shop.status'),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(to='shop.size'),
        ),
    ]