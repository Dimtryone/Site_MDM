from django.db import models
from django.shortcuts import reverse  # для передачи url slug

# Create your models here.

class MainPosts(models.Model):
    title = models.CharField(max_length=150, db_index=True,
                             verbose_name='Заголовок')
    body = models.TextField(max_length=1500, db_index=True,
                            verbose_name='Текст')
    slug = models.SlugField(max_length=1000, unique=True, verbose_name='URL')
    image = models.ImageField(upload_to="blog/icon/%Y/%m/%d",
                                   verbose_name='Иконки')

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name = 'Посты'
        verbose_name_plural = 'Посты'
