from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    id = models.AutoField(
        primary_key=True,
        verbose_name='Unique number'
    )
    username = models.CharField(
        unique=True,
        max_length=30,
        verbose_name='Login of user'
        )
    first_name = models.CharField(
        max_length=100,
        verbose_name='Name of user',
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

    id = models.AutoField(
        primary_key=True,
        verbose_name='Unique number'
    )
    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='blog',
        verbose_name='Author of blog'
        )
    description = models.CharField(
        max_length=500,
        verbose_name='Description of blog',
        blank=True,
        null=True
        )

    def __str__(self):
        return str(self.id)


class Post(models.Model):

    id = models.AutoField(
        primary_key=True,
        verbose_name='Unique number'
    )
    heading = models.CharField(
        max_length=100,
        verbose_name='Heading of post',
        )
    text = models.TextField(
        max_length=140,
        verbose_name='text of post'
        )
    date_create = models.DateTimeField(
        auto_now_add=True,
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
