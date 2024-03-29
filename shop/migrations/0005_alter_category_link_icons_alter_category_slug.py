# Generated by Django 4.1.3 on 2023-02-03 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_brend_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='link_icons',
            field=models.ImageField(upload_to='icons/categories/%Y/%m/%d', verbose_name='Иконки'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(db_index=True, max_length=50, unique=True),
        ),
    ]
