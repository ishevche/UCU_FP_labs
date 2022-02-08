"""Sorts songs"""
from typing import List, Tuple


def song_length(song: Tuple[str]) -> float:
    """Returns the length of the song"""
    return float(song[1])


def title_length(song: Tuple[str]) -> int:
    """Returns the length of the title"""
    return len(song[0])


def last_word(song: Tuple[str]) -> str:
    """Returns the first symbol in the last word of the song title"""
    return song[0].split()[-1][0].lower()


def to_string_array(param: List[Tuple[str]]) -> List[str]:
    """Converts list of tuples to list of strings"""
    return [
        f"('{song_title}', '{length_song}')"
        for song_title, length_song in param
    ]


def sort_songs(song_titles: List[str], length_songs: List[str],
               key) -> List[tuple]:
    """

    :param song_titles:
    :param length_songs:
    :param key:
    :return:

    >>> print('\\n'.join(to_string_array(sort_songs(
    ... ['Янанебібув', 'Той день', 'Мало мені', 'Сосни', 'Кавачай', 'Відпусти',
    ... 'Африка', 'Поясни', 'Фіалки', 'Коли тебе нема', 'Етюд'],
    ... ['3.19', '3.58', '5.06', '4.31', '4.39', '3.52', '4.24', '3.39',
    ... '3.43', '3.17', '2.21'],
    ... song_length
    ... ))))
    ('Етюд', '2.21')
    ('Коли тебе нема', '3.17')
    ('Янанебібув', '3.19')
    ('Поясни', '3.39')
    ('Фіалки', '3.43')
    ('Відпусти', '3.52')
    ('Той день', '3.58')
    ('Африка', '4.24')
    ('Сосни', '4.31')
    ('Кавачай', '4.39')
    ('Мало мені', '5.06')
    >>> print('\\n'.join(to_string_array(sort_songs(
    ... ['Янанебібув', 'Той день', 'Мало мені', 'Сосни', 'Кавачай', 'Відпусти',
    ... 'Африка', 'Поясни', 'Фіалки', 'Коли тебе нема', 'Етюд'],
    ... ['3.19', '3.58', '5.06', '4.31', '4.39', '3.52', '4.24', '3.39',
    ... '3.43', '3.17', '2.21'],
    ... title_length
    ... ))))
    ('Етюд', '2.21')
    ('Сосни', '4.31')
    ('Африка', '4.24')
    ('Поясни', '3.39')
    ('Фіалки', '3.43')
    ('Кавачай', '4.39')
    ('Той день', '3.58')
    ('Відпусти', '3.52')
    ('Мало мені', '5.06')
    ('Янанебібув', '3.19')
    ('Коли тебе нема', '3.17')
    >>> print('\\n'.join(to_string_array(sort_songs(
    ... ['Янанебібув', 'Той день', 'Мало мені', 'Сосни', 'Кавачай', 'Відпусти',
    ... 'Африка', 'Поясни', 'Фіалки', 'Коли тебе нема', 'Етюд'],
    ... ['3.19', '3.58', '5.06', '4.31', '4.39', '3.52', '4.24', '3.39',
    ... '3.43', '3.17', '2.21'],
    ... last_word
    ... ))))
    ('Африка', '4.24')
    ('Відпусти', '3.52')
    ('Той день', '3.58')
    ('Етюд', '2.21')
    ('Кавачай', '4.39')
    ('Мало мені', '5.06')
    ('Коли тебе нема', '3.17')
    ('Поясни', '3.39')
    ('Сосни', '4.31')
    ('Фіалки', '3.43')
    ('Янанебібув', '3.19')
    >>> sort_songs([], ['1'], last_word)
    >>> sort_songs(['dfdfdf'], ['fdf'], song_length)
    """
    if len(song_titles) != len(length_songs):
        return None
    lst = []
    for i in range(len(song_titles)):
        lst.append((song_titles[i], length_songs[i]))
    try:
        return sorted(lst, key=key)
    except ValueError:
        pass
