from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from apps import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.search, name='search'),
    path('home/', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('toggle-watchlist/', views.toggle_watchlist, name='toggle_watchlist'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]
