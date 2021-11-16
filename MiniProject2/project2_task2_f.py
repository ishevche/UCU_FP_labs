"""grep analog"""
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
        description='Searches matches in files matching regex'
    )
    parser.add_argument(
        'regex',
        type=str,
        help='regex to search',
        metavar='regex'
    )
    parser.add_argument(
        'files_regex',
        type=str,
        help='files matches this regex will be checked',
        metavar='files_regex'
    )
    parser.add_argument(
        '--show_lines',
        action='store_true',
        help='show_numbers_of_line'
    )
    parser.add_argument(
        '--only_show_counts',
        action='store_true',
        help='show only number of lines matched'
    )
    return parser.parse_args()


def print_file(new_path: str, file_regex: re, regex: re,
               show_lines: bool, count: bool):
    """
    Prints all matches in file if its name matches regex
    :param new_path: path to the file
    :param file_regex: regex to path the name
    :param regex: regex to path the content
    :param show_lines: show numbers of lines
    :param count: show only count of lines
    :return: None
    """
    match_object: re.Match = file_regex.match(new_path)
    if match_object is None:
        return
    try:
        with open(new_path, 'r') as file:
            content = file.read().split('\n')
            print_matched_string(new_path, file_regex, Fore.BLUE)
            if count:
                content = list(filter(lambda x: regex.search(x) is not None,
                                      content))
                print(f': {len(content)}')
            else:
                print()
                for idx, line in enumerate(content):
                    if regex.search(line) is None:
                        continue
                    if show_lines:
                        print(f'{Fore.GREEN}{Style.BRIGHT}'
                              f'{idx + 1}'
                              f'{Style.RESET_ALL}: ', end='')
                    print_matched_string(line, regex, Fore.RED)
                    print()
    except OSError:
        pass


def print_matched_string(string, regex, color):
    """
    Prints matched string with colors
    :param string: string that matched
    :param regex: regex that matched
    :param color: color to print with
    :return: None
    >>> print_matched_string("./.idea/.gitignore", re.compile('.*'), Fore.BLUE)
    """
    match_object: re.Match = regex.search(string)
    if match_object is not None:
        while match_object is not None and len(string) != 0:
            print(f'{string[:match_object.span()[0]]}'
                  f'{color}{Style.BRIGHT}'
                  f'{match_object.group()}'
                  f'{Style.RESET_ALL}', end='')
            string = string[match_object.span()[1]:]
            match_object = regex.search(string)
        print(string, end='')


def print_matches_in_dir(path: str, file_regex: re, regex: re,
                         show_lines: bool, count: bool):
    """
    Prints matching lines in matching files
    :param path: path to provided directory
    :param file_regex: regex to match files
    :param regex: regex to match lines
    :param show_lines: show numbers of lines
    :param count: show only count of lines
    :return: None
    """
    try:
        files = sorted(os.listdir(path), key=lambda x: x.replace('.', '')
                       .replace('_', "").lower())
        for object_name in files:
            new_path = os.path.join(path, object_name)
            if os.path.isfile(new_path):
                print_file(new_path, file_regex, regex, show_lines, count)
            elif os.path.isdir(new_path):
                print_matches_in_dir(new_path, file_regex, regex,
                                     show_lines, count)

    except OSError:
        pass


# def print_sub(path: str, regex: re):
#     """
#     Prints dirs matching regex at path and below
#     :param path: dir location
#     :param regex: regex to match
#     :return: None
#     """
#     files = sorted(os.listdir(path), key=lambda x: x.replace('.', '')
#                    .replace('_', "").lower())
#     for object_name in files:
#         new_path = os.path.join(path, object_name)
#         if os.path.isdir(new_path):
#             print_dir(new_path, regex)


def main():
    """
    A main function
    :return: None
    """
    args = get_args()
    print_matches_in_dir(os.path.curdir, re.compile(args.files_regex),
                         re.compile(args.regex), args.show_lines,
                         args.only_show_counts)


if __name__ == '__main__':
    main()
