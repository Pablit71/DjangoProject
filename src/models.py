from django.contrib.auth.models import AbstractUser
from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Фото')
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    page_count = models.PositiveIntegerField(verbose_name='Кол-во страниц')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    available_copies = models.PositiveIntegerField(verbose_name='Кол-во')
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Reader(AbstractUser):
    phone_number = models.BigIntegerField(verbose_name='Телефон')
    is_active = models.BooleanField(default=True)
    books = models.ManyToManyField(Book, verbose_name='Книги', blank=True, null=True)
    date_update = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='myuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    # связь с правами доступа, используем свойство related_name, чтобы избежать конфликтов
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='myuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
