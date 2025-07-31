import os
import requests
from dotenv import load_dotenv
from django.core.cache import cache
from requests.exceptions import RequestException

load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_ACCESS_TOKEN = os.getenv('TMDB_ACCESS_TOKEN')  # Using v4 auth
BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = os.getenv('IMAGE_BASE_URL')
CACHE_TIMEOUT = 60 * 60 * 6  # 6 hours cache

def get_tmdb_data(endpoint, params=None):
    """
    Get data from TMDB API with proper authentication and error handling
    """
    cache_key = f"tmdb_{endpoint}_{str(params)}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data

    headers = {
        'Authorization': f'Bearer {TMDB_ACCESS_TOKEN}',
        'accept': 'application/json'
    }
    params = params or {}
    params['api_key'] = TMDB_API_KEY  # For backward compatibility

    try:
        response = requests.get(
            f"{BASE_URL}{endpoint}",
            headers=headers,
            params=params,
            timeout=10  # Add timeout to prevent hanging
        )
        response.raise_for_status()
        data = response.json()
        cache.set(cache_key, data, CACHE_TIMEOUT)
        return data
    except RequestException as e:
        print(f"TMDB API Error ({endpoint}): {e}")
        # Return cached data even if stale if available
        stale_data = cache.get(cache_key)
        if stale_data:
            return stale_data
        return None

def get_popular_movies(page=1):
    return get_tmdb_data('/movie/popular', {'page': page})

def get_movie_details(movie_id):
    return get_tmdb_data(
        f'/movie/{movie_id}',
        {'append_to_response': 'videos,credits,similar,recommendations'}
    )

def search_movies(query, page=1):
    return get_tmdb_data('/search/movie', {'query': query, 'page': page})

def get_movie_genres():
    return get_tmdb_data('/genre/movie/list')

def get_trending_movies(time_window='week'):
    return get_tmdb_data(f'/trending/movie/{time_window}')

def get_upcoming_movies():
    return get_tmdb_data('/movie/upcoming')

def get_top_rated_movies():
    return get_tmdb_data('/movie/top_rated')

def get_now_playing_movies():
    return get_tmdb_data('/movie/now_playing')

def get_image_url(path, size='w500'):
    return f"{IMAGE_BASE_URL}{size}{path}" if path else None

def get_movie_providers(movie_id):
    """Get where to watch the movie (streaming/buy/rent info)"""
    return get_tmdb_data(f'/movie/{movie_id}/watch/providers')

#add  tv shows
def get_tv_show_providers(tv_show_id):
    """Get where to watch the TV show (streaming/buy/rent info)"""
    return get_tmdb_data(f'/tv/{tv_show_id}/watch/providers')

def get_tv_show_details(tv_show_id):
    return get_tmdb_data(
        f'/tv/{tv_show_id}',
        {'append_to_response': 'videos,credits,similar,recommendations'}
    )

def search_tv_shows(query, page=1):
    return get_tmdb_data('/search/tv', {'query': query, 'page': page})

def get_tv_show_genres():
    return get_tmdb_data('/genre/tv/list')

def get_trending_tv_shows(time_window='week'):
    return get_tmdb_data(f'/trending/tv/{time_window}')

def get_popular_tv_shows(page=1):
    return get_tmdb_data('/tv/popular', {'page': page})

def get_top_rated_tv_shows():
    return get_tmdb_data('/tv/top_rated')

def get_on_air_tv_shows():
    return get_tmdb_data('/tv/on_the_air')

def get_airing_today_tv_shows():
    return get_tmdb_data('/tv/airing_today')