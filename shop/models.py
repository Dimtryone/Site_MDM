from django.db import models
from django.urls import reverse
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, last_name, password=None, phone=None):
        if not email:
            raise ValueError('Пожалуйста, введите свой e-mail')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            last_name=last_name,
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, last_name, password, phone=None):
        user = self.create_user(
            email=self.normalize_email(email,),
            name=name,
            last_name=last_name,
            phone=phone,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Without PremissionsMixin will be Error (admin.E019)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Покупатели'

    def get_full_name(self):
        return self.name + ' ' + self.last_name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Product(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Наименование')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    material = models.CharField(max_length=80, verbose_name='Материал')
    description = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name='Фото')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    brend = models.ForeignKey('Brend', on_delete=models.PROTECT, null=True, verbose_name='Бренд')
    amount = models.IntegerField(verbose_name='Количество')
    size = models.ManyToManyField('Size', verbose_name='Размер')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_id = models.IntegerField(verbose_name='Каталожный номер')

    def __str__(self):
        return f'{self.title} - {self.pk}'

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_id': self.pk})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('id'), related_name='images')
    image = models.ImageField(_('image'), upload_to='products/images/', blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('product', args=[str(self.id)])

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


class Category(models.Model):
    name_category = models.CharField(max_length=100, unique=True,
                                     db_index=True, verbose_name='Название')
    #поэтому
    # полю будет создан индекс БД, уникальность обеспечивается автоматом
    link_icons = models.ImageField(upload_to="shop/icons_cat/%Y/%m/%d",
                                   verbose_name='Иконка')
    slug = models.CharField(max_length=50, unique=True, db_index=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name_category

    def get_absolute_url(self):
        return reverse('catalog', kwargs={'slug': self.slug})


class Brend(models.Model):
    name_brend = models.CharField(max_length=100, db_index=True,
                                  verbose_name='Наименование бренда')

    def __str__(self):
        return self.name_brend

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Size(models.Model):
    size = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.size

class Order(models.Model):
    description = models.TextField(blank=True)
    adress = models.CharField(max_length=200,  default='')
    payment_method = models.CharField(max_length=80)
    emploee = models.ForeignKey('Emploee', on_delete=models.SET_NULL, null=True)
    #status = models.ManyToManyField('Status', through='OrderStatus')
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь',on_delete=models.CASCADE)

class OrderProduct(models.Model):
    count = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Emploee(models.Model):
    name_emp = models.CharField(max_length=80)
    surname_emp = models.CharField(max_length=80)
    patronymic_emp = models.CharField(max_length=80)

class Status(models.Model):
    name_status = models.CharField(max_length=80)

    def __str__(self):
        return self.name_status

class OrderStatus(models.Model):
    date_strat = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_finish = models.DateTimeField(auto_now=True, auto_now_add=False)
    flag_finish = models.BooleanField(default=False)
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)





