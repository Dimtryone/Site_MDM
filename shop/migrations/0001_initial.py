# Generated by Django 4.1.3 on 2022-12-01 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_brend', models.CharField(db_index=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_category', models.CharField(db_index=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=50)),
                ('material', models.CharField(max_length=80)),
                ('description', models.TextField(blank=True)),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d')),
                ('amount', models.IntegerField()),
                ('brend', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='shop.brend')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='shop.category')),
            ],
        ),
    ]