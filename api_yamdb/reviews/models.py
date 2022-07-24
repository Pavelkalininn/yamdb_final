from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

ROLE_CHOICES = (
    ('user', 'USER'),
    ('moderator', 'MODERATOR'),
    ('admin', 'ADMIN'),
)

CODE_LENGTH = 64
PASSWORD_LENGTH = 18


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        username,
        email,
        password='',
        bio='',
        role='user',
        first_name='',
        last_name=''
    ):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            confirmation_code=self.make_random_password(length=CODE_LENGTH),
            password=password,
            role=role,
            bio=bio,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        user.email_user(
            subject='confirmation_code',
            message=user.confirmation_code,
            fail_silently=False
        )

        return user

    def create_superuser(
        self,
        username,
        email,
        password=None,
        bio='',
        role='admin',
        first_name='',
        last_name=''
    ):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(
            username=username,
            email=email,
            password=make_password(password),
            role=role,
            bio=bio,
            first_name=first_name,
            last_name=last_name
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=16,
        choices=ROLE_CHOICES,
        default='user'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=CODE_LENGTH
    )

    objects = CustomUserManager()

    class Meta:
        ordering = ['-date_joined']

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'


class Genre(models.Model):
    name = models.TextField(
        'Жанр',
        help_text='Введите жанр'
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        ordering = ['-name']


class Category(models.Model):
    name = models.TextField(
        'Категория',
        help_text='Введите категорию'
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        ordering = ['-name']


class Title(models.Model):
    name = models.TextField(
        'Произведение',
        help_text='Введите произведение'
    )
    year = models.PositiveSmallIntegerField(
        help_text='Введите год издания'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='title',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    description = models.TextField(
        'Описание',
        help_text='Введите описание',
        null=True,
        blank=True

    )

    class Meta:
        ordering = ['-year']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year'],
                name='unique_title'),
        ]


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    score = models.PositiveSmallIntegerField()

    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    text = models.TextField(
        'Текст поста',
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'),
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    text = models.TextField(
        'Текст поста',
    )

    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
