"""counries.py"""
import re


def read_file(path: str) -> list:
    """ Return list of lines from file """
    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.readlines()


def country_dict(lines_list: list, year: int) -> dict:
    """
    Return dict from list of lines with the country as key and
    name as a value in that year
    """
    ans = {}
    cur_pos = 0
    while lines_list[cur_pos].__contains__('=============='):
        cur_pos += 1
    cur_pos += 1
    regex = re.compile(r'^\"(.+?)\"\s+?\((\d{4}).*\).+?\s+?(\w+)')
    while cur_pos < len(lines_list):
        if regex.match(lines_list[cur_pos]):
            name, cur_year, country = regex.findall(lines_list[cur_pos])[0]
            cur_year = int(cur_year)
            if cur_year == year:
                if country in ans:
                    ans[country] += [name]
                else:
                    ans[country] = [name]
        cur_pos += 1
    return ans


def country_num(dict_country: dict) -> list:
    """
    Return sorted by the number of films list of tuples
    that each consists country and number of films
    """
    ans_list = []
    for key, val in dict_country.items():
        ans_list += [(key, len(val))]
    list.sort(ans_list, key=lambda x: x[1], reverse=True)
    return ans_list


def write_films(film_list: list) -> None:
    """ Write country and number of films to file
    """
    with open('answer', 'w') as output:
        for entry in film_list:
            output.write(f'{entry[0]} - {entry[1]}\n')


def films_year(year: int = 2019) -> None:
    """ Find countries and write to file
    """
    lines_list = read_file('countries.list')
    dict_country = country_dict(lines_list, year)
    film_list = country_num(dict_country)
    write_films(film_list)
