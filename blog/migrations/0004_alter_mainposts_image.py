# Generated by Django 4.1.3 on 2023-02-03 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_mainposts_options_alter_mainposts_body_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainposts',
            name='image',
            field=models.ImageField(upload_to='blog/icon/%Y/%m/%d', verbose_name='Иконки'),
        ),
    ]
