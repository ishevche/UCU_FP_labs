"""names.py"""
import re


def read_names(file_path):
    """
    Reads data from file
    :param file_path: path to file
    :return: dict with data
    """
    with open(file_path, 'r') as input_file:
        ans = {}
        for line in input_file:
            if re.match(r'^(.+?)\s+\((\d+)\)$', line):
                name, amount = re.findall(r'^(.+?)\s+\((\d+)\)$', line)[0]
                ans[name] = int(amount)
    return ans


def most_popular_names(names, amount):
    """
    Searches <amount> most popular names in <names> dictionary
    :param names: dictionary of words
    :param amount: amount of words
    :return: a set of names
    >>> most_popular_names({'МАКСИМ':680, 'АРТЕМ':477, \
    'МАТВІЙ':816, 'bgv':100}, 3) == {'МАКСИМ', 'АРТЕМ', 'МАТВІЙ'}
    True
    """
    names_list = list(names.items())
    list.sort(names_list, key=lambda x: x[1], reverse=True)
    names_list = names_list[:amount]
    return set(map(lambda x: x[0], names_list))


def names_appeared(names, amount):
    """
    Searches all names appeared exactly <amount> times
    :param names: names to search in
    :param amount: amount of appearances
    :return: tuple with amount and set of these names
    >>> names_appeared({'МАКСИМ':680, 'АРТЕМ':477, \
    'МАТВІЙ':816, 'bgv':100}, 816) == (1, {'МАТВІЙ'})
    True
    """
    names_list = list(names.items())
    names_list = list(filter(lambda x: x[1] == amount, names_list))
    return len(names_list), set(map(lambda x: x[0], names_list))


def most_popular_first_letter(names):
    """
    Finds most common first letter, amount of names on these letter,
    amount of kids on these letter
    :param names: dict of names
    :return: tuple
    >>> most_popular_first_letter({'МАКСИМ':680, 'АРТЕМ':477, \
    'МАТВІЙ':816, 'bgv':100})
    ('М', 2, 1496)
    """
    ans_dict = {}
    for name, amount in names.items():
        amount_names = ans_dict.get(name[0], (0, 0))[0]
        amount_kids = ans_dict.get(name[0], (0, 0))[1]
        ans_dict[name[0]] = amount_names + 1, amount_kids + amount
    ans_list = list(ans_dict.items())
    list.sort(ans_list, key=lambda x: x[1][0], reverse=True)
    return ans_list[0][0], ans_list[0][1][0], ans_list[0][1][1]


def find_names(file_path):
    """
    Deals with statistic about names in 2017 year
    :param file_path: path to the file with names
    :return: tuple: (a set of three most usable names,
        tuple: (amount of once appeared names, set of these names),
        tuple: (most common first letter,
            amount of names starting with it,
            amount of kids who have these names)
    """
    names = read_names(file_path)
    most_popular = most_popular_names(names, 3)
    once_appeared = names_appeared(names, 1)
    first_letter = most_popular_first_letter(names)
    return most_popular, once_appeared, first_letter
