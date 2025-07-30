from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .services import (
    #movies
    get_trending_movies,
    get_popular_movies,
    get_upcoming_movies,
    get_top_rated_movies,
    get_movie_details,
    search_movies,

    #tv shows
    get_trending_tv_shows,
    get_popular_tv_shows,
    get_top_rated_tv_shows,
)
from .models import Movie, Genre, Watchlist

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

import json

def home(request):

    # Get Movies Data
    trending_movies = get_trending_movies().get('results')
    popular_movies = get_popular_movies().get('results')
    upcoming_movies = get_upcoming_movies().get('results')
    top_rated_movies = get_top_rated_movies().get('results')

    # Get TV Shows Data
    trending_tv_shows = get_trending_tv_shows().get('results')
    popular_tv_shows = get_popular_tv_shows().get('results')
    top_rated_tv_shows = get_top_rated_tv_shows().get('results')

    context = {
        'trending_movies': trending_movies,
        'popular_movies': popular_movies,
        'upcoming_movies': upcoming_movies,
        'top_rated_movies': top_rated_movies,
        'trending_tv_shows': trending_tv_shows,
        'popular_tv_shows': popular_tv_shows,
        'top_rated_tv_shows': top_rated_tv_shows,
    }
    return render(request, 'home.html', context)

def movie_detail(request, movie_id):
    movie_data = get_movie_details(movie_id)

    # Get or create movie in database
    movie, created = Movie.objects.get_or_create(
        tmdb_id=movie_id,
        defaults={
            'title': movie_data.get('title'),
            'overview': movie_data.get('overview'),
            'poster_path': movie_data.get('poster_path'),
            'backdrop_path': movie_data.get('backdrop_path'),
            'release_date': movie_data.get('release_date'),
            'vote_average': movie_data.get('vote_average'),
            'vote_count': movie_data.get('vote_count'),
            'popularity': movie_data.get('popularity'),
            'runtime': movie_data.get('runtime'),
             'IMAGE_BASE_URL': 'https://image.tmdb.org/t/p/',
        }
    )

    # Update genres
    if 'genres' in movie_data:
        for genre_data in movie_data['genres']:
            genre, _ = Genre.objects.get_or_create(
                tmdb_id=genre_data['id'],
                defaults={'name': genre_data['name']}
            )
            movie.genres.add(genre)

    # Check if movie is in user's watchlist
    in_watchlist = False
    if request.user.is_authenticated:
        in_watchlist = Watchlist.objects.filter(
            user=request.user,
            movie=movie
        ).exists()

    # Get trailer video
    trailer = None
    if 'videos' in movie_data and movie_data['videos']['results']:
        for video in movie_data['videos']['results']:
            if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                trailer = video
                break

    context = {
        'movie': movie_data,
        'in_watchlist': in_watchlist,
        'trailer': trailer,
        'cast': movie_data.get('credits', {}).get('cast', [])[:10],
        'similar_movies': movie_data.get('similar', {}).get('results', [])[:10],
    }
    return render(request, 'movie_detail.html', context)

def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        search_data = search_movies(query)
        results = search_data.get('results', [])

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'search.html', context)

@login_required
@require_POST
def toggle_watchlist(request):
    movie_id = request.POST.get('movie_id')
    if not movie_id:
        return JsonResponse({'error': 'Movie ID is required'}, status=400)

    # Get or create movie
    movie_data = get_movie_details(movie_id)
    movie, created = Movie.objects.get_or_create(
        tmdb_id=movie_id,
        defaults={
            'title': movie_data.get('title'),
            'overview': movie_data.get('overview'),
            'poster_path': movie_data.get('poster_path'),
            'backdrop_path': movie_data.get('backdrop_path'),
            'release_date': movie_data.get('release_date'),
            'vote_average': movie_data.get('vote_average'),
            'vote_count': movie_data.get('vote_count'),
            'popularity': movie_data.get('popularity'),
            'runtime': movie_data.get('runtime'),
        }
    )

    # Update genres if needed
    if 'genres' in movie_data:
        for genre_data in movie_data['genres']:
            genre, _ = Genre.objects.get_or_create(
                tmdb_id=genre_data['id'],
                defaults={'name': genre_data['name']}
            )
            movie.genres.add(genre)

    # Toggle watchlist status
    watchlist_item, created = Watchlist.objects.get_or_create(
        user=request.user,
        movie=movie
    )

    if not created:
        watchlist_item.delete()
        return JsonResponse({'status': 'removed', 'in_watchlist': False})

    return JsonResponse({'status': 'added', 'in_watchlist': True})

@login_required
def watchlist(request):
    watchlist_movies = Watchlist.objects.filter(user=request.user).select_related('movie')
    context = {
        'watchlist_movies': [item.movie for item in watchlist_movies],
    }
    return render(request, 'watchlist.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')