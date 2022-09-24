from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from accounts import views


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('profile/', views.profile, name='profile'),
    path('favorite/', views.favorite, name='favorite'),
    path('favorite_add/<int:user_id>', views.favorite_add, name='favorite_add'),
    path('favorite/favorite_delete/<int:user_id>', views.favorite_delete, name='favorite_delete'),
    path('settings/', views.settings, name='settings'),
    path('enter_code/', views.enter_code, name='enter_code'),
    path('enter_code/submit_code', views.submit_code, name='submit_code'),
]
