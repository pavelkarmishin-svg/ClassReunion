from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('user/<slug:username>/', views.ShowUserView.as_view(), name='user_info'),
    path('contacts/', views.contacts, name='contacts'),
]
