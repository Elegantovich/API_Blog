from django.contrib.auth.models import AbstractUser
from django.db import models


class Date(models.Model):

    date = models.DateField(
        auto_now_add=True,
        verbose_name='Date of create post'
        )


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
    is_read = models.BooleanField(
        default=False,
        verbose_name='Set flag about reading the post',
        )

    def __str__(self):
        return self.heading


class Follow(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Follower',
        related_name='follower'
        )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Blog',
        related_name='following')


class Read(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='user',
        related_name='User'
        )
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Read posts',
        related_name='Read_posts')
