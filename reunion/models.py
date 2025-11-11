from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from pytils.translit import slugify
from PIL import Image
# from django.core.files.base import ContentFile
# from io import BytesIO
# import os

class User(AbstractUser):
    # pass


    maiden_name = models.CharField(max_length=150, blank=True, null=True)
    telegram = models.CharField(max_length=150, blank=True, null=True)
    vk_profile = models.CharField(max_length=150, blank=True, null=True)
    ok_profile = models.CharField(max_length=150, blank=True, null=True)
    username = None  # полностью убираем username
    email = models.EmailField(unique=True)
    picture_young = models.ImageField(upload_to='pictures', blank=True, null=True, default='defaults/default_young.png')
    picture_teenager = models.ImageField(upload_to='pictures', blank=True, null=True, default='defaults/default_teenager.png')
    picture_old = models.ImageField(upload_to='pictures', blank=True, null=True, default='defaults/default_old.png')
    history = models.TextField(blank=True, null=True)
    slug = models.SlugField(db_index=True, default='', null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

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

    def get_url(self):
        return reverse('user_info', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.email)
        super(User, self).save(*args, **kwargs)
        if self.picture_young:
            User.compress_image(self.picture_young.path)
        if self.picture_teenager:
            User.compress_image(self.picture_teenager.path)
        if self.picture_old:
            User.compress_image(self.picture_old.path)

    @staticmethod
    def compress_image(img_path):
        img = Image.open(img_path)

        # Максимальный размер (ширина, высота)
        max_size = (800, 800)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Сохраняем в том же месте (перезаписываем)
        img.save(img_path, quality=85, optimize=True)

class UserGallery(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='gallery/')

    def save(self, *args, **kwargs):
        # Сначала сохраняем обычным способом
        super().save(*args, **kwargs)

        # Затем открываем изображение
        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)

            # Максимальный размер (ширина, высота)
            max_size = (800, 800)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Сохраняем в том же месте (перезаписываем)
            img.save(img_path, quality=85, optimize=True)

    def __str__(self):
        return f"Фото {self.user.email}"


class PhotoComment(models.Model):
    photo = models.ForeignKey('UserGallery', on_delete=models.CASCADE, related_name='comments')  # комментарии под фото
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='written_comments')  # комментарии, написанные пользователем
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class GroupPhotos(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='group_photos')
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=False)

    def save(self, *args, **kwargs):
        # Сначала сохраняем обычным способом
        super().save(*args, **kwargs)

        # Затем открываем изображение
        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)

            # Максимальный размер (ширина, высота)
            max_size = (800, 800)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Сохраняем в том же месте (перезаписываем)
            img.save(img_path, quality=85, optimize=True)

    def __str__(self):
        return f"Групповое фото {self.description}"

class GroupPhotoComment(models.Model):
    photo = models.ForeignKey('GroupPhotos', on_delete=models.CASCADE, related_name='gp_comments')  # комментарии под фото
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='gp_written_comments')  # комментарии, написанные пользователем
    text = models.TextField()

class Teachers(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='teacher_photos')
    image = models.ImageField(upload_to='gallery/')
    name = models.TextField(blank=False)
    subject = models.TextField(blank=False)

    def save(self, *args, **kwargs):
        # Сначала сохраняем обычным способом
        super().save(*args, **kwargs)

        # Затем открываем изображение
        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)

            # Максимальный размер (ширина, высота)
            max_size = (800, 800)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Сохраняем в том же месте (перезаписываем)
            img.save(img_path, quality=85, optimize=True)

    def __str__(self):
        return f"Учитель {self.subject} {self.name}"

class TeacherComment(models.Model):
    photo = models.ForeignKey('Teachers', on_delete=models.CASCADE, related_name='teacher_comments')  # комментарии под фото
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='teacher_written_comments')  # комментарии, написанные пользователем
    text = models.TextField()