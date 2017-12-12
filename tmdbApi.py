import requests
from pprint import pprint
import json
import sys
import time


def TMDBtoIMDB(api_key, tmdb_id):
    try:
        payload = {'api_key': api_key}
        my_response = requests.get('https://api.themoviedb.org/3/movie/' + str(tmdb_id), params=payload)
        data = json.loads(my_response.content)
        try:
            imdb_id = data['imdb_id']
            return imdb_id
        except:
            return -1
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def getTMDBListDetails(api_key, list_id):
    try:
        print("Attempting to get tmdb list details..")
        list_ids = []
        payload = {'api_key': api_key}
        my_response = requests.get('https://api.themoviedb.org/3/list/' + str(list_id), params=payload)
        data = json.loads(my_response.content)
        for item in data['items']:
            list_ids.append(item['id'])
        print("Got list details!")
        return list_ids
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def moviesByActorId(api_key, actor_id):
    movie_ids = []
    try:
        print("Attempting to get movies by actor id..")
        payload = {'with_cast': actor_id, 'sort_by': 'release_date.asc', 'api_key': api_key, 'page': 1}
        my_response = requests.get('http://api.themoviedb.org/3/discover/movie', params=payload)
        data = json.loads(my_response.content)
        page_count = data['total_pages']
        for movie_id in data['results']:
            movie_ids.append(movie_id['id'])
        counter = 2
        while counter <= page_count:
            payload = {'with_cast': actor_id, 'sort_by': 'release_date.asc', 'api_key': api_key, 'page': counter}
            my_response = requests.get('http://api.themoviedb.org/3/discover/movie', params=payload)
            data = json.loads(my_response.content)
            for movie_id in data['results']:
                movie_ids.append(movie_id['id'])
            counter += 1
        print("Got movie list!")
        return movie_ids
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def generateSessionId(api_key, token):
    try:
        payload = {'api_key': api_key, 'request_token': token}
        my_response = requests.get('https://api.themoviedb.org/3/authentication/session/new', params=payload)
        data = json.loads(my_response.content)
        pprint(data)
        return data['session_id']
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def addIdsToList(api_key, session_id, movie_ids, list_id):
    counter = 0
    try:
        print("Attempting to add movies to list..")
        payload = {'api_key': api_key, 'session_id': session_id}
        for id in movie_ids:
            counter += 1
            if counter % 30 == 0:
                print("Sleeping for 15 seconds so we don't go over API limit!")
                time.sleep(15)
                print("Continuing..")
            my_response = requests.post('http://api.themoviedb.org/3/list/' + str(list_id) + '/add_item',
                                        params=payload,
                                        json={"media_id": id})
            data = json.loads(my_response.content)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    print("Added all movies to list!")


def clearList(api_key, session_id, list_id):
    try:
        pprint("Clearing list!")
        payload = {'api_key': api_key, 'session_id': session_id, 'confirm': 'true'}
        my_response = requests.post('https://api.themoviedb.org/3/list/' + list_id + '/clear', params=payload)
        data = json.loads(my_response.content)
        pprint(data)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def createList(api_key, session_id, name):
    try:
        print("Attempting to create list..")
        payload = {'api_key': api_key, 'session_id': session_id}
        my_response = requests.post('https://api.themoviedb.org/3/list', params=payload,
                                    json={"name": name, "description": "radarrList"})
        data = json.loads(my_response.content)
        print("Created list!")
        return data['list_id']
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def searchByActorName(api_key, name):
    try:
        payload = {'api_key': api_key, 'query': name}
        my_response = requests.post('https://api.themoviedb.org/3/search/person', params=payload,
                                    json={"name": name, "description": "radarrList"})
        data = json.loads(my_response.content)
        results = data['results']
        if len(results) != 1:
            print("Search ended, one actor was not returned (either 0 or more than 1)")
            pprint(data['results'])
            return -1
        else:
            print("Found one actor when searching by name: " + results[0]['name'])
            actor_id = results[0]['id']
            return actor_id

    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
