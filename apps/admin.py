from django.contrib import admin
from unfold.admin import ModelAdmin
# from unfold.contrib.forms.admin import ModelFormAdmin  # For enhanced forms
from .models import Genre, Movie, Watchlist
from django.utils.html import format_html

@admin.register(Genre)
class GenreAdmin(ModelAdmin):
    list_display = ('tmdb_id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)
    list_per_page = 20

    # Unfold specific customizations
    actions_on_top = True
    actions_on_bottom = False

@admin.register(Movie)
class MovieAdmin(ModelAdmin):
    list_display = (
        'poster_thumbnail',
        'title',
        'release_year',
        'vote_average_display',
        'popularity_display',
        'runtime_display'
    )
    search_fields = ('title', 'overview', 'tmdb_id')
    list_filter = (
        'release_date',
        'vote_average',
        'genres',
        ('vote_average', admin.ChoicesFieldListFilter),
    )
    ordering = ('-release_date',)
    filter_horizontal = ('genres',)
    list_per_page = 20
    date_hierarchy = 'release_date'

    # Custom display methods
    @admin.display(description='Poster')
    def poster_thumbnail(self, obj):
        if obj.poster_path:
            return format_html(
                '<img src="https://image.tmdb.org/t/p/w92{}" style="height: 50px;" />',
                obj.poster_path
            )
        return "-"

    @admin.display(description='Year', ordering='release_date')
    def release_year(self, obj):
        return obj.release_date.year if obj.release_date else "-"

    @admin.display(description='Rating')
    def vote_average_display(self, obj):
        return f"{obj.vote_average:.1f}" if obj.vote_average else "-"

    @admin.display(description='Popularity')
    def popularity_display(self, obj):
        return f"{obj.popularity:.0f}" if obj.popularity else "-"

    @admin.display(description='Runtime')
    def runtime_display(self, obj):
        if obj.runtime:
            hours = obj.runtime // 60
            minutes = obj.runtime % 60
            return f"{hours}h {minutes}m"
        return "-"

@admin.register(Watchlist)
class WatchlistAdmin(ModelAdmin):
    list_display = ('user', 'movie_display', 'added_at')
    search_fields = ('user__username', 'movie__title')
    list_filter = ('added_at', 'user')
    ordering = ('-added_at',)
    list_per_page = 20
    raw_id_fields = ('user', 'movie')  # Better for large user/movie databases

    @admin.display(description='Movie')
    def movie_display(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            f"/admin/movies/movie/{obj.movie.id}/change/",
            obj.movie.title
        )

    # Optimize queries
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'movie')