from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from reunion import views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView
from reunion.views import CustomPasswordChangeView

# urlpatterns = [
#     path('accounts/', include('django.contrib.auth.urls')),
#     path('', views.index),
#     path('mainpage/', views.mainpage, name='mainpage'),
#     path('admin/', admin.site.urls),
#
#     path('accounts/register/', include('reunion.urls')),
#
# ]

urlpatterns = [
    path("password/change/", PasswordChangeView.as_view(), name="password_change_custom"),
    path('', views.index),
    path('mainpage/', views.ShowUsersList.as_view(), name='mainpage'),

    path('group_photos/', views.group_photos, name='group_photos'),

    path('teachers/', views.teachers, name='teachers'),

    path('profile/', views.user_profile, name='profile'),
    path('admin/', admin.site.urls),

    # встроенные auth-urls (login, logout, reset password и т.д.)
    path('accounts/', include('django.contrib.auth.urls')),

    # твои кастомные urls для регистрации и логина
    path('accounts/', include('reunion.urls')),
    path("logout/", LogoutView.as_view(), name="logout"),

    path('user/<slug:username>/', views.ShowUserView.as_view(), name='user_info'),
    path('donation/', include('donation.urls', namespace='donation')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)