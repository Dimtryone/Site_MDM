# Generated by Django 4.1.3 on 2023-01-27 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainPosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(db_index=True, max_length=150)),
                ('body', models.TextField(db_index=True, max_length=1000)),
                ('slug', models.SlugField(max_length=1000, unique=True)),
            ],
        ),
    ]
