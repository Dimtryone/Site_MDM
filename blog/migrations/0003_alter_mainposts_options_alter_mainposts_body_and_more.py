# Generated by Django 4.1.3 on 2023-02-03 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_mainposts_pub_date_mainposts_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mainposts',
            options={'verbose_name': 'Посты', 'verbose_name_plural': 'Посты'},
        ),
        migrations.AlterField(
            model_name='mainposts',
            name='body',
            field=models.TextField(db_index=True, max_length=1000, verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='mainposts',
            name='slug',
            field=models.SlugField(max_length=1000, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='mainposts',
            name='title',
            field=models.CharField(db_index=True, max_length=150, verbose_name='Заголовок'),
        ),
    ]
