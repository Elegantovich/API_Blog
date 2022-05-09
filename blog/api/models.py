from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    username = models.CharField(
        unique=True,
        max_length=30,
        verbose_name='Login of user'
        )
    first_name = models.CharField(
        max_length=100,
        verbose_name='Name of user'
        blank=True,
        null=True
        )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Surname of user',
        blank=True,
        null=True
        )
    password = models.CharField(
        verbose_name='Password of account',
        max_length=100
        )
    is_subscribed = models.BooleanField(
        default=False,
        verbose_name='Subscribe to user',

        )
    User = 'user'
    Admin = 'admin'

    ROLES = (
        (User, 'user'),
        (Admin, 'admin')
        )

    role = models.CharField(
        choices=ROLES,
        default='user',
        max_length=5,
        verbose_name='Статус',
        blank=True,
        null=True
        )

    def __str__(self):
        return self.username


class Blog(models.Model):
    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Author of blog'
        )
    description = models.TextField(
        verbose_name='Description of blog',
        blank=True,
        null=True
        )

    def __str__(self):
        return self.description


class Post(models.Model):
    heading = models.CharField(
        max_length=100,
        verbose_name='Heading of post',
        )
    text = models.TextField(
        verbose_name='text of post'
        )
    date_create = models.DateTimeField(
        verbose_name='Date of create post'
        )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Blog'
        )

    def __str__(self):
        return self.heading