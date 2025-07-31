from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from apps.movie import views as movie_views

urlpatterns = [
    # Admin (Unfold-enabled)
    path('admin/', admin.site.urls),

    # Public Movie Routes
    path('', movie_views.search, name='search'),
    path('home/', movie_views.home, name='home'),
    path('movie/<int:movie_id>/', movie_views.details, name='details'),

    # Watchlist
    path('watchlist/', movie_views.watchlist, name='watchlist'),
    path('toggle-watchlist/', movie_views.toggle_watchlist, name='toggle_watchlist'),

    # Auth
    path('register/', movie_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    # Optional: Password Reset Flow (recommended for production)
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
