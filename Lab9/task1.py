"""keyword_processor.py"""


def find_film_keywords(film_keywords: dict, film_name: str):
    """
    Finds all keywords used in film <film_name>
    :param film_keywords: database with keywords and films
    :param film_name: film to search
    :return: set of all keywords
    >>> find_film_keywords({'a':['aba', 'bab'], 'b':['aba']} \
    ,'aba') == {'a', 'b'}
    True
    >>> find_film_keywords({'a':['aba', 'bab'], 'b':['aba']} ,'bab') == {'a'}
    True
    >>> find_film_keywords({'a':['aba', 'bab'], 'b':['aba']} ,'aaa') == set()
    True
    """
    answer = set()
    for keyword, films in film_keywords.items():
        if film_name in films:
            answer.add(keyword)
    return answer


def find_films_with_keywords(film_keywords: dict, num_of_films: int):
    """
    Finds <num_of_films> films with greatest amount of keywords
    :param film_keywords: database with keywords and films
    :param num_of_films: number of films to search
    :return: list of tuples with films and number of keywords for this film
    >>> find_films_with_keywords({'a':['aba', 'bab'], 'b':['aba']}, 3)
    [('aba', 2), ('bab', 1)]
    >>> find_films_with_keywords({'a':['aba', 'bab'], 'b':['aba']}, 2)
    [('aba', 2), ('bab', 1)]
    >>> find_films_with_keywords({'a':['aba', 'bab'], 'b':['aba']}, 1)
    [('aba', 2)]
    >>> find_films_with_keywords({'a':['aba', 'bab'], 'b':['aba']}, 0)
    []
    """
    films_keywords = {}
    for _, films in film_keywords.items():
        for film in films:
            films_keywords[film] = films_keywords.get(film, 0) + 1
    return sorted(list(films_keywords.items()),
                  key=lambda x: x[1], reverse=True)[:num_of_films]
