from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_view, name='contact'),
    path('messages/', views.message_list, name='message_list'),
]