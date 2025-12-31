from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserGallery, PhotoComment, GroupPhotos, GroupPhotoComment
from .forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User

    list_display = ("email", "first_name", "last_name", "is_staff", "is_active", "vk_profile", "ok_profile", "telegram",
                    'picture_young', 'picture_teenager', 'picture_old')
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)  # <-- ВАЖНО! username здесь больше нельзя

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Персональные данные", {"fields": ("first_name", "last_name")}),
        ("Права доступа", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active"),
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserGallery)
admin.site.register(PhotoComment)
admin.site.register(GroupPhotos)
admin.site.register(GroupPhotoComment)
