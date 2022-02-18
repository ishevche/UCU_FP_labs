import re

import argparse
import firebase_admin
import folium
import haversine
from firebase_admin import credentials
from firebase_admin import firestore
from geopy.geocoders import Nominatim
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

cached_locations = {}


def get_google_docs_credentials():
    """
    Gets a google docs credentials using google docs api
    """
    creds = Credentials.from_authorized_user_info(
        {
            "token": "token"},
        ['https://www.googleapis.com/auth/documents.readonly']
    )

    try:
        return build('docs', 'v1', credentials=creds)
    except HttpError as err:
        print(err)


def get_cached_data_google_docs():
    """
    Gets cached data written down in 10 google documents
    """
    global cached_locations
    documents_id = ['17Iduw2uE0LTuilaE79rjkdIxZdn8RXHTVn0NzqpN8dQ',
                    '1dh69er438XWauj34xMWIeVcJQc4P6y4a-2ku6_n_LFc',
                    '19qe0JnYqyoG8TNAwkxJuLKYw84-NYXeqyZukKi9HF3E',
                    '1aMG_lEdGd4-m8fEbpUym83mXjASrZIxxv9EE0Pv6miE',
                    '1gtPeEalmbl5lk7efUg0akvMxnnOgaQ01Rdl4mtD8xdg',
                    '1g122OV6wMsNMsCqGWuOTTDabmKuNVmneNGZCtyPrMZM',
                    '192wPAKF0pmuOgzj0qkd7YpT9rJ74I9CST3ady_kgP7o',
                    '18UJWf9AGcnUbMuhxMkaeVwe775qNvbnJgiDX6cLHnqo',
                    '1o4Rqioxpk2s1B0MtPY42k8y6Y9JM3sGMmTf9wwXd9Xk',
                    '1L36A2BxY7IBMXqwgZrxa0HJ4UU_SQ934mPngrZ95CUk']
    service = get_google_docs_credentials()
    for idx, document in enumerate(documents_id):
        document = service.documents().get(documentId=document).execute()
        content = document['body']['content']
        ans = ''
        for paragraph in content[1:]:
            text = paragraph['paragraph']['elements'][0]['textRun']['content']
            ans += text[:-1]
        cached_locations = {**cached_locations, **eval(ans)}
        print(f'Loading ... ({idx + 1}0%)')


def get_firebase_document(year: int):
    """
    Gets firestore document with list of locations needed for given <year>
    File firebase_token.json required for appropriate work
    """
    cred = credentials.Certificate('firebase_token.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db.collection('locations').document(str(year))


def get_cached_data_firebase(year: int):
    """
    Gets cache data for specific year written down on firestore
    File firebase_token.json required for appropriate work
    """
    global cached_locations
    firebase_data = get_firebase_document(year).get().to_dict()[str(year)]

    for location in firebase_data:
        coords = location['coords']
        if coords is None:
            cached_locations[location['name']] = None
        else:
            cached_locations[location['name']] = tuple(coords)


def get_args():
    """
    Get args specified in the cmd
    :return: tuple: (year, latitude, longitude, path)
    """
    parser = argparse.ArgumentParser(
        description='Builds html file, containing map with markers'
    )
    parser.add_argument(
        'year',
        type=int,
        help='year to show markers',
        metavar='year'
    )
    parser.add_argument(
        'latitude',
        type=float,
        help='your current latitude',
        metavar='latitude'
    )
    parser.add_argument(
        'longitude',
        type=float,
        help='your current longitude',
        metavar='longitude'
    )
    parser.add_argument(
        'path',
        type=str,
        help='path to film dataset',
        metavar='path'
    )
    return (parser.parse_args().year, parser.parse_args().latitude,
            parser.parse_args().longitude, parser.parse_args().path)


def create_map(year: int, latitude: float, longitude: float, path: str):
    """
    Creates a folium map with films info
    :param year: year of films to display
    :param latitude: latitude to center
    :param longitude: longitude to center
    :param path: path to film database
    :return: None
    """
    get_cache(year)

    folium_map = folium.Map(location=[latitude, longitude],
                            zoom_start=5)
    year_locations = get_sorted_location_list(read_dataset(path, year=year),
                                              latitude, longitude, year)
    if year_locations is None:
        return

    folium_map.add_child(get_year_layer(year_locations[:10], year))

    future_films = read_dataset(path, year=2022) \
        .union(read_dataset(path, year=2023)) \
        .union(read_dataset(path, year=2024))
    future_locations = get_sorted_location_list(future_films, latitude,
                                                longitude, 'future')
    folium_map.add_child(get_year_layer(future_locations, 'future'))

    folium_map.add_child(folium.LayerControl())
    folium_map.save(f'{year}_films.html')


def get_cache(year):
    """
    Gets cached data from firebase for specific year
    (firebase_token.json required) or Google Docs as alternative
    """
    try:
        print('Getting cache from firebase ...')
        get_cached_data_firebase(year)
    except:
        pass
    if not cached_locations:
        print('Failed (cache is empty)')
        print('Getting cache from google docs ...')
        try:
            get_cached_data_google_docs()
        except:
            pass
        if not cached_locations:
            print('Failed! (cache is empty)')
            print('Program will fetch data from geopy')
            print('It might take some time')
    if cached_locations:
        print('Success')


def read_dataset(path: str, year: int) -> set:
    """
    Reads dataset, returns formatted data about films filmed in given year
    :param path: path to dataset
    :param year: year to search films in
    :return: set of tuples (film name, filming location)
    """
    try:
        answer_set = set()
        with open(path, encoding='iso-8859-1') as data:
            regex = re.compile(r'^(.+?) \((\d{4})[)/].*?\t+([^\t\n]+)')
            for data_line in data:
                if regex.match(data_line):
                    film_name, film_year, film_location = \
                        regex.findall(data_line)[0]

                    if film_year == str(year):
                        answer_set.add((film_name, film_location))
        return answer_set
    except OSError:
        print(f'Could not find such file: {path}')


def get_sorted_location_list(film_set, latitude, longitude, label):
    """
    Sorts by distance to center and transforms a set of films
    :param film_set: set of films (film_name, film_location)
    :param latitude: center latitude
    :param longitude: center longitude
    :param label: label for debug info
    :return: sorted list ((latitude, longitude), list of films, made there)
    """
    if film_set is not None:
        print(f'Films in {label} (overall): {len(film_set)}')
        locations_dict = {}

        from_cache = 0
        from_geopy = 0
        could_not_found = 0

        for film in film_set:
            location = find_location(film[1])
            if location[1] == 'Got from cache':
                from_cache += 1
            elif location[1] == 'Got from geopy':
                from_geopy += 1
            else:
                could_not_found += 1
            location = location[0]

            if location is None:
                continue
            if location in locations_dict:
                locations_dict[location].append(film[0])
            else:
                locations_dict[location] = [film[0]]

        print(f'Among them:\n'
              f'{from_cache} got from cache,\n'
              f'{from_geopy} got from geopy,\n'
              f'{could_not_found} could not find at all')

        return sorted(locations_dict.items(),
                      key=lambda x: distance((latitude, longitude), x[0]))


def find_location(location_str: str) -> tuple:
    """
    Returns coordinates on given text address
    :param location_str: text address
    :return: tuple with data:
        ((latitude, longitude), 'Got from cache' or 'Got from geopy') if search
            succeeded
        (None, 'Could not reach') otherwise
    """
    if location_str in cached_locations:
        return cached_locations[location_str], 'Got from cache'

    geo_locator = Nominatim(user_agent="UCU Programing lab")
    location = None

    for i in range(len(location_str.split(', '))):
        location = geo_locator.geocode(', '.join(location_str.split(', ')[i:]),
                                       timeout=10)
        if location is not None:
            break
    if location is None:
        print(location_str)
        return None, 'Could not reach'

    return (location.latitude, location.longitude), 'Got from geopy'


def distance(first_point: tuple, second_point: tuple) -> float:
    """
    Counts shortest distance between two given point on a sphere
    :param first_point: tuple: (latitude, longitude)
    :param second_point: tuple: (latitude, longitude)
    :return: distance in kilometers or
        infinity if at least one of the points is None
    """
    try:
        return haversine.haversine(first_point, second_point)
    except TypeError:
        return float('inf')


def get_year_layer(locations, year):
    """
    Returns a layer for folium map with films markers on it
    :param locations: list of filming locations
    :param year: year of filming
    :return: FeatureGroup object
    """
    map_feather_group = folium.FeatureGroup(name=f'Films in {year}')

    popup_text = """<h4>Films info:</h4>
    Film names: {},<br><br>
    Year: {}
    """

    for point in locations:
        text = folium.IFrame(html=popup_text.format(', '.join(point[1]), year))
        map_feather_group.add_child(folium.Marker(
            location=list(point[0]),
            popup=folium.Popup(text,
                               min_width=250,
                               min_height=150,
                               max_width=1000,
                               max_height=750),
            icon=folium.Icon(color='green')
        ))
    return map_feather_group


if __name__ == '__main__':
    create_map(*get_args())
