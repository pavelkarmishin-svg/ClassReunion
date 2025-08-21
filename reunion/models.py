from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
    # nickname = models.CharField(max_length=150, unique=True)
    # director_nickname = models.CharField(max_length=150, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Уникальное имя
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Уникальное имя
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )