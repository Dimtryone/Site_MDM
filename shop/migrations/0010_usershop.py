# Generated by Django 4.1.3 on 2023-02-09 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_product_product_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('number_phone', models.IntegerField()),
                ('password', models.CharField(max_length=80)),
            ],
        ),
    ]
