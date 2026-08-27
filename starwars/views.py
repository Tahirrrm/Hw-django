import json
import urllib.request
from urllib.error import URLError, HTTPError

from django.shortcuts import render

# swapi.dev — основной источник, но он периодически не работает.
# swapi.py4e.com — рабочее зеркало того же API (запасной вариант).
SWAPI_BASES = [
    'https://swapi.dev/api',
    'https://swapi.py4e.com/api',
]


def _open_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Hw-django homework)'})
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode('utf-8'))


def swapi_get(path):
    """Запрос к SWAPI. Пробует базовые URL по очереди. Возвращает dict или None."""
    for base in SWAPI_BASES:
        try:
            return _open_json(f'{base}/{path}')
        except (URLError, HTTPError, json.JSONDecodeError, OSError):
            continue
    return None


def swapi_names(urls):
    """Преобразует список ссылок SWAPI в список имён."""
    names = []
    for url in urls:
        try:
            data = _open_json(url)
            names.append(data.get('name') or data.get('title') or url)
        except (URLError, HTTPError, json.JSONDecodeError, OSError):
            names.append(url)
    return names


def film_list(request):
    """Список всех фильмов серии."""
    data = swapi_get('films/')
    films = []
    if data:
        for film in data['results']:
            film_id = film['url'].rstrip('/').split('/')[-1]
            films.append({
                'id': film_id,
                'title': film['title'],
                'episode_id': film['episode_id'],
                'release_date': film['release_date'],
                'director': film['director'],
            })
    films.sort(key=lambda f: f['episode_id'])
    context = {'films': films, 'error': data is None}
    return render(request, 'starwars/film_list.html', context)


def film_detail(request, film_id):
    """Информация о конкретном фильме."""
    data = swapi_get(f'films/{film_id}/')
    if not data:
        return render(request, 'starwars/film_detail.html', {
            'film': None,
            'error': True,
            'film_id': film_id,
        })

    film = {
        'title': data['title'],
        'episode_id': data['episode_id'],
        'release_date': data['release_date'],
        'director': data['director'],
        'producer': data['producer'],
        'opening_crawl': data['opening_crawl'],
        'characters': swapi_names(data['characters']),
        'planets': swapi_names(data['planets']),
        'starships': swapi_names(data['starships']),
        'vehicles': swapi_names(data['vehicles']),
        'species': swapi_names(data['species']),
    }
    return render(request, 'starwars/film_detail.html', {
        'film': film,
        'error': False,
        'film_id': film_id,
    })
