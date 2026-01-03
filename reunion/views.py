from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import *
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import ListView, DetailView


def index(request):
    return render(request, 'reunion/index.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('login')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    form = CustomAuthenticationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    return render(request, 'registration/login.html', {'form': form})


class ShowUsersList(ListView):
    template_name = 'reunion/manepage.html'
    model = User
    context_object_name = 'users'


def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_form = CustomUserEditForm(instance=request.user)
    young_form = ChangePictureYoungForm(instance=request.user)
    teenager_form = ChangePictureTeenagerForm(instance=request.user)
    old_form = ChangePictureOldForm(instance=request.user)
    my_history_form = MyHistoryForm(instance=request.user)
    user_gallery_form = UserGalleryForm(instance=request.user)
    comment_form = PhotoCommentForm(instance=request.user)

    if request.method == 'POST':

        action = request.POST.get("action")

        if action == 'change_history':
            my_history_form = MyHistoryForm(request.POST, instance=request.user)
            if my_history_form.is_valid():
                my_history_form.save()
        else:
            my_history_form = MyHistoryForm(instance=request.user)

        if action == "save_profile":
            user_form = CustomUserEditForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
        else:
            user_form = CustomUserEditForm(instance=request.user)

        if action == "save_young":
            young_form = ChangePictureYoungForm(request.POST, request.FILES, instance=request.user)
            if young_form.is_valid():
                young_form.save()
        else:
            young_form = ChangePictureYoungForm(instance=request.user)

        if action == "save_teenager":
            teenager_form = ChangePictureTeenagerForm(request.POST, request.FILES, instance=request.user)
            if teenager_form.is_valid():
                teenager_form.save()
        else:
            teenager_form = ChangePictureTeenagerForm(instance=request.user)

        if action == "save_old":
            old_form = ChangePictureOldForm(request.POST, request.FILES, instance=request.user)
            if old_form.is_valid():
                old_form.save()
        else:
            old_form = ChangePictureOldForm(instance=request.user)

        if action == "add_photo":
            user_gallery_form = UserGalleryForm(request.POST, request.FILES)
            if user_gallery_form.is_valid():
                new_photo = user_gallery_form.save(commit=False)
                new_photo.user = request.user  # <--- ВАЖНО! Привязываем к текущему пользователю
                new_photo.save()
                return redirect(request.path + '#load-file')
        else:
            user_gallery_form = UserGalleryForm()

        if action == "delete_photo":
            delete_photo(request, UserGallery)

        if action == "add_comment":
            comment_form = PhotoCommentForm(request.POST)
            return add_comment(request, UserGallery, comment_form)
            # if comment_form.is_valid():
            #     comment = comment_form.save(commit=False)
            #     comment.author = request.user
            #     photo_id = request.POST.get("photo_id")
            #     comment.photo = UserGallery.objects.get(id=photo_id)
            #     comment.save()
            #     return redirect(request.path + f'#photo-{photo_id}')

        if action == "delete_comment":
            delete_comment(request, PhotoComment)

    return render(request, 'reunion/user_profile.html',
                  {'user_form': user_form, 'teenager_form': teenager_form,
                   'old_form': old_form, 'young_form': young_form,
                   'my_history_form': my_history_form, 'user_gallery_form': user_gallery_form,
                   'comment_form': comment_form})


class CustomPasswordChangeView(PasswordChangeView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method != "POST":
            # убираем data, чтобы форма на GET была unbound
            kwargs.pop("data", None)
            kwargs.pop("files", None)
        return kwargs


class ShowUserView(DetailView):
    template_name = 'reunion/user_info.html'
    model = User
    slug_field = 'slug'  # поле модели, по которому ищем
    slug_url_kwarg = 'username'  # имя параметра в path('user/<slug:username>/')
    context_object_name = 'user'  # чтобы в шаблоне обращаться как {{ user }}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = PhotoCommentForm()
        return context

    def post(self, request, *args, **kwargs):
        """
        Обработка отправки комментария.
        Ожидаем:
          - hidden input photo_id
          - поле comment text от PhotoCommentForm
        """
        # получим объект пользователя (страницу которого смотрим)
        self.object = self.get_object()

        # проверка авторизации (если не используем LoginRequiredMixin)
        if not request.user.is_authenticated:
            messages.error(request, "Нужно войти в систему, чтобы оставить комментарий.")
            return redirect('login')

        action = request.POST.get('action')
        if action == 'add_comment':
            photo_id = request.POST.get('photo_id')
            if not photo_id:
                messages.error(request, "Не указан идентификатор фото.")
                return redirect(self.object.get_url())

            # Попытка получить фото, принадлежащее этому пользователю
            photo = get_object_or_404(UserGallery, id=photo_id, user=self.object)

            # собираем форму и валидируем
            form = PhotoCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.photo = photo
                comment.save()
                # по хорошему — уведомление или сообщение
                messages.success(request, "Комментарий добавлен.")
                # PRG — редирект обратно на страницу пользователя, к фото
                return redirect(self.object.get_url() + f'#photo-{photo_id}')
            else:
                # Если форма невалидна — перенести ошибки в контекст и снова показать страницу
                context = self.get_context_data(object=self.object)
                context['comment_form'] = form  # bound-form с ошибками
                return self.render_to_response(context)

        # если action другой — просто вернуть GET
        return redirect(self.object.get_url())


def contacts(request):
    return render(request, 'reunion/contacts.html')


def group_photos(request):
    group_photos_form = GroupPhotoForm()
    comments_form = GroupPhotoCommentForm()
    photos = GroupPhotos.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == "add_photo":
            if not request.user.is_authenticated:
                messages.error(request, "Нужно войти в систему, чтобы оставить комментарий.")
                return redirect('login')
            group_photos_form = GroupPhotoForm(request.POST, request.FILES)
            if group_photos_form.is_valid():
                new_photo = group_photos_form.save(commit=False)
                new_photo.user = request.user  # <--- ВАЖНО! Привязываем к текущему пользователю
                new_photo.save()
                return redirect(request.path + '#load-file')
            else:
                group_photos_form = GroupPhotoForm()

        if action == "delete_photo":
            delete_photo(request, GroupPhotos)

        if action == "add_comment":
            if not request.user.is_authenticated:
                messages.error(request, "Нужно войти в систему, чтобы оставить комментарий.")
                return redirect('login')
            comments_form = GroupPhotoCommentForm(request.POST)
            return add_comment(request, GroupPhotos, comments_form)

        if action == "delete_comment":
            delete_comment(request, GroupPhotoComment)

    return render(request, 'reunion/group_photos.html', {'group_photos_form': group_photos_form,
                                                         'comments_form': comments_form,
                                                         'photos': photos})


def teachers(request):
    teachers_form = TeachersForm()
    comments_form = TeacherCommentForm()
    photos = Teachers.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == "add_photo":
            if not request.user.is_authenticated:
                messages.error(request, "Нужно войти в систему, чтобы оставить комментарий.")
                return redirect('login')
            teachers_form = TeachersForm(request.POST, request.FILES)
            if teachers_form.is_valid():
                new_photo = teachers_form.save(commit=False)
                new_photo.user = request.user  # <--- ВАЖНО! Привязываем к текущему пользователю
                new_photo.save()
                return redirect(request.path + '#load-file')
            else:
                teachers_form = GroupPhotoForm()

        if action == "delete_photo":
            delete_photo(request, Teachers)

        if action == "add_comment":
            if not request.user.is_authenticated:
                messages.error(request, "Нужно войти в систему, чтобы оставить комментарий.")
                return redirect('login')
            comments_form = TeacherCommentForm(request.POST)
            return add_comment(request, Teachers, comments_form)

        if action == "delete_comment":
            delete_comment(request, TeacherComment)

    return render(request, 'reunion/teachers.html', {'teachers_form': teachers_form,
                                                     'comments_form': comments_form,
                                                     'photos': photos})


def delete_photo(request, model):
    photo_id = int(request.POST.get("photo_id"))
    if model == UserGallery:
        photo_ids = list(request.user.gallery.values_list('id', flat=True))
    elif model == Teachers:
        photo_ids = list(request.user.teacher_photos.values_list('id', flat=True))
    else:
        photo_ids = list(request.user.group_photos.values_list('id', flat=True))
    photo_id_index = photo_ids.index(photo_id)
    if photo_id_index == 0:
        next_photo_id = 1
    else:
        next_photo_id = photo_ids[photo_id_index - 1]
    try:
        photo = model.objects.get(id=photo_id, user=request.user)
        photo.delete()
        return redirect(request.path + f'#photo-{str(next_photo_id)}')
    except model.DoesNotExist:
        pass  # на случай, если кто-то подделал форму


def delete_comment(request, model):
    comment_id = request.POST.get("comment_id")
    comment = model.objects.filter(id=comment_id, author=request.user).first()
    if comment:
        photo_id = comment.photo_id
        comment.delete()
        return redirect(request.path + f'#photo-{photo_id}')


def add_comment(request, model, comment_form):
    comment = comment_form.save(commit=False)
    comment.author = request.user
    photo_id = request.POST.get("photo_id")
    comment.photo = model.objects.get(id=photo_id)
    comment.save()
    return redirect(request.path + f'#photo-{photo_id}')
