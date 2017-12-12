import sqlite3
from sqlite3 import Error
import tmdbApi
import radarrApi
import json
import time


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def select_all_tasks(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Movies")

    rows = cur.fetchall()
    print(len(rows))
    print(rows[0])
    #for row in rows:
    #    print(row)


def select_by_imdb(conn, imdb):
    cur = conn.cursor()
    cur.execute("SELECT MovieFileId FROM Movies WHERE ImdbId=?", (imdb,))

    rows = cur.fetchall()
    if len(rows) != 1:
        return -1
    if rows[0][0] == 0:
        return 0
    return 1


def main():
    print("Started!")
    with open('settings.json') as json_data:
        settings = json.load(json_data)
        json_data.close()

    api_key = settings['api_key_tmdb']
    session_id = settings['session_id']
    api_key_radarr = settings['api_key_radarr']
    path = settings['path']
    profile_id = settings['profile_id']
    search_bool = True
    database = settings['database_file']
    conn = create_connection(database)
    #search = "Tom Cruise"
    search = input("Actor name to search for: ")

    actor_id = tmdbApi.searchByActorName(api_key, search)
    list_id = tmdbApi.createList(api_key, session_id, search)
    movie_ids = tmdbApi.moviesByActorId(api_key, actor_id)
    tmdbApi.addIdsToList(api_key, session_id, movie_ids, list_id)
    list_movie_ids = tmdbApi.getTMDBListDetails(api_key, list_id)
    counter = 0
    print("Sleeping for 15 seconds so we don't go over API limit!")
    time.sleep(15)
    print("Continuing..")
    for movie_id in list_movie_ids:
        counter += 1
        if counter % 30 == 0:
            print("Sleeping for 15 seconds so we don't go over API limit!")
            time.sleep(15)
            print("Continuing..")
        imdb_id = tmdbApi.TMDBtoIMDB(api_key, movie_id)
        if imdb_id == '':
            print("Movie was not found on imdb: " + str(movie_id))
            continue
        found = select_by_imdb(conn, imdb_id)
        #if found == 1: found and downloaded
        #if found == 0:  found and not downloaded
        if found == -1:
            print("Not found - " + str(imdb_id))
            result = radarrApi.RadarrImdbSearch(api_key_radarr, str(imdb_id))
            radarrApi.AddMovieFromSearch(result, path, api_key_radarr, profile_id, search_bool)


if __name__ == '__main__':
    main()
