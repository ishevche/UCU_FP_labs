"""search directories by regex"""
import argparse
import os
import re

from colorama import Fore, Style


def get_args():
    """
    Get args specified in the cmd
    :return: Namespace object with all arguments
    """
    parser = argparse.ArgumentParser(
        description='Searches directories that matches regex'
    )
    parser.add_argument(
        'regex',
        type=str,
        help='regex to search',
        metavar='regex'
    )
    parser.add_argument(
        'path',
        type=str,
        help='path to start directory',
        metavar='path'
    )
    return parser.parse_args()


def print_dir(path: str, regex: re):
    """
    Prints directory and all subdirectories if it matches regex
    :param path: path to provided directory
    :param regex: regex to match
    :return: None
    """
    try:
        path_copy = path
        match_object: re.Match = regex.search(path)
        if match_object is not None:
            while match_object is not None:
                print(f'{path[:match_object.span()[0]]}'
                      f'{Fore.RED}{Style.BRIGHT}'
                      f'{match_object.group()}'
                      f'{Style.RESET_ALL}', end='')
                path = path[match_object.span()[1]:]
                match_object = regex.search(path)
            print(path)
        print_sub(path_copy, regex)
    except OSError:
        pass


def print_sub(path: str, regex: re):
    """
    Prints dirs matching regex at path and below
    :param path: dir location
    :param regex: regex to match
    :return: None
    """
    files = sorted(os.listdir(path), key=lambda x: x.replace('.', '')
                   .replace('_', "").lower())
    for object_name in files:
        new_path = os.path.join(path, object_name)
        if os.path.isdir(new_path):
            print_dir(new_path, regex)


def main():
    """
    A main function
    :return: None
    """
    args = get_args()
    if os.path.isdir(args.path):
        print_dir(args.path, re.compile(args.regex))
    else:
        print(f"No such directory: \'{args.path}\'")


if __name__ == '__main__':
    main()
