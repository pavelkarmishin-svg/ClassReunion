from django.urls import path
from donation import views

app_name = 'donation'

urlpatterns = [
    path('', views.donate, name='donate'),
    path('thanks/', views.thanks, name='thanks'),
    path('notification/', views.payment_notification, name='notification'),
    path('return/', views.yoomoney_return, name='yoomoney_return'),
    path("start/", views.start_payment, name="start_payment")


]
