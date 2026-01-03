from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import ClearableFileInput
from .models import User, UserGallery, PhotoComment, GroupPhotos, GroupPhotoComment, Teachers, TeacherComment
from django.core.exceptions import ValidationError


class SocialLinksCleanMixin:
    def clean_vk_profile(self):
        value = self.cleaned_data.get("vk_profile", "")
        return self.normalize_link(value, "vk.com")

    def clean_telegram(self):
        value = self.cleaned_data.get("telegram", "")
        return self.normalize_link(value, "t.me")

    def clean_ok_profile(self):
        value = self.cleaned_data.get("ok_profile", "")
        return self.normalize_link(value, "ok.ru")

    @staticmethod
    def normalize_link(value, soc_media):
        if not value:
            return ""
        value = value.strip().lstrip("@")
        if value.startswith("http"):
            return value
        return f"https://{soc_media}/{value}"


class CustomUserCreationForm(UserCreationForm, SocialLinksCleanMixin):
    first_name = forms.CharField(max_length=150, label="Имя")
    last_name = forms.CharField(max_length=150, label="Фамилия")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'maiden_name',
                  'telegram', 'vk_profile', 'ok_profile', 'control_question')

    def clean_control_question(self):
        # Проверка контрольного вопроса
        answer = self.cleaned_data.get('control_question', '')
        # пример: ожидаемый ответ
        EXPECTED_ANSWER = ['шеф', 'шэф']
        if answer.lower() not in  EXPECTED_ANSWER:
            raise ValidationError("Неверный ответ на контрольный вопрос")
        return answer


class CustomUserEditForm(forms.ModelForm, SocialLinksCleanMixin):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'maiden_name', 'telegram', 'vk_profile', 'ok_profile')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
    # email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')


class CustomClearableFileInput(ClearableFileInput):
    initial_text = ''
    input_text = ''


class ChangePictureYoungForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('picture_young',)
        widgets = {
            "picture_young": forms.FileInput(
                attrs={
                    "id": "id_picture_young",
                    "class": "file-input",
                }
            ),
        }


class ChangePictureTeenagerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('picture_teenager',)
        widgets = {
            "picture_teenager": forms.FileInput(
                attrs={
                    "id": "id_picture_teenager",
                    "class": "file-input",
                }
            ),
        }


class ChangePictureOldForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('picture_old',)
        widgets = {
            "picture_old": forms.FileInput(
                attrs={
                    "id": "id_picture_old",
                    "class": "file-input",
                }
            ),

        }


class UserGalleryForm(forms.ModelForm):
    class Meta:
        model = UserGallery
        fields = ('image',)
        labels = {'image': 'Загрузи фото для альбома'}


class MyHistoryForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('history',)
        widgets = {
            "history": forms.Textarea(attrs={
                "class": "auto-resize",
                "placeholder": "Напиши свою историю..."
            })
        }


class PhotoCommentForm(forms.ModelForm):
    class Meta:
        model = PhotoComment
        fields = ('text',)
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Напиши комментарий...',
                'class': 'auto-resize',
            })
        }


class GroupPhotoForm(forms.ModelForm):
    class Meta:
        model = GroupPhotos
        fields = ('image', 'description')
        labels = {'image': 'Загрузи фото для альбома', 'description': 'Описание: год, класс, событие'}


class GroupPhotoCommentForm(forms.ModelForm):
    class Meta:
        model = GroupPhotoComment
        fields = ('text',)
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Напиши комментарий...',
                'class': 'auto-resize',
            })
        }


class TeachersForm(forms.ModelForm):
    class Meta:
        model = Teachers
        fields = ('image', 'name', 'subject')
        labels = {'image': 'Загрузи фото учителя', 'name': 'Имя:', 'subject': 'Предмет:'}


class TeacherCommentForm(forms.ModelForm):
    class Meta:
        model = TeacherComment
        fields = ('text',)
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Напиши комментарий...',
                'class': 'auto-resize',
            })
        }
