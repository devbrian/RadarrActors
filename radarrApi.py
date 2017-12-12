import requests
import json
import sys


def RadarrImdbSearch(api_key, search_imdb):
    try:
        payload = {'apikey': api_key}
        my_response = requests.get('http://localhost:7878/api/movies/lookup?term=imdb%3A' + search_imdb, params=payload)
        data = json.loads(my_response.content)
        if len(data) > 0:
            first_result = data[0]
            return first_result
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def AddMovieFromSearch(result, path, apikey, profile_id, search):
    result['monitored'] = True
    result['rootFolderPath'] = path
    result['profileId'] = profile_id
    options = {'ignoreEpisodesWithFiles': False, 'ignoreEpisodesWithoutFiles': False, 'searchForMovie': search}
    result['addOptions'] = options

    try:
        payload = {'apikey': apikey}
        my_response = requests.post('http://localhost:7878/api/movie', params=payload, json=result)
        data = json.loads(my_response.content)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
