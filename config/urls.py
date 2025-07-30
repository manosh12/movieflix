from django.contrib import admin
from django.urls import path
from apps import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.search, name='search'),
    path('home/', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('toggle-watchlist/', views.toggle_watchlist, name='toggle_watchlist'),
]
