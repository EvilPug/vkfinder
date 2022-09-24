from django.urls import path

from . import views

app_name = 'finder'

urlpatterns = [
    path('', views.MainPage.as_view(), name='index'),
    path('auth/', views.auth, name='auth'),
]
