"""
Builds trees and also demonstrates its work
"""

import json

from task3.linkedbst import LinkedBST


def read_file(path):
    """
    Reads data from json file
    """
    with open(path, 'r') as input_file:
        data = json.load(input_file)["Косівщина"]
    return data


def population_trees(path_to_file):
    """
    Builds trees from file data
    """
    data_list = read_file(path_to_file)
    data = {}
    for data_piece in data_list:
        town = data_piece["населений пункт"]
        if town not in data:
            data[town] = {}
        population = (data_piece["гр-кат."] + data_piece["лат."] +
                      data_piece["вірм."] + data_piece["жид."] +
                      data_piece["акат."])
        classes_per_1000 = data_piece["школа"] / population * 1000
        data[town][data_piece["рік"]] = classes_per_1000
    trees = {}
    for town, town_data in data.items():
        tree = LinkedBST()
        for year, classes_per_1000 in town_data.items():
            tree.add((classes_per_1000, year))
        tree.rebalance()
        trees[town] = tree
    return trees


def demo():
    """
    demonstration of module work
    """
    result = population_trees('Kosiv_state.json')
    for town_name, tree_object in result.items():
        print(town_name, end=': ')
        range_found = tree_object.range_find((1, 0), (20, 0))
        # Returns tuples in form (classes_per_100, year)
        range_found = list(map(lambda x: x[1], range_found))
        print(', '.join(map(str, range_found)))


if __name__ == '__main__':
    demo()
