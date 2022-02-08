"""tree analog"""
import argparse
import os

from colorama import Fore, Style


def get_args():
    """
    Get args specified in the cmd
    :return: Namespace object with all arguments
    """
    parser = argparse.ArgumentParser(
        description='Builds tree of folders and files'
    )
    parser.add_argument(
        'path',
        type=str,
        help='path to start directory',
        metavar='path'
    )
    return parser.parse_args()


def print_link(name, parent_path, string_prefix):
    """
    Prints link object
    :param name: link name
    :param parent_path: path to parent directory
    :param string_prefix: prefix printed before content
    :return: None
    """
    print(f"{string_prefix} "
          f"{Fore.CYAN}{Style.BRIGHT}"
          f"{name}"
          f"{Style.RESET_ALL}"
          f" -> ", end='')
    path_to_link = os.path.join(parent_path, name)
    path_to_content = os.readlink(path_to_link)
    if os.path.isdir(os.path.join(parent_path, path_to_content)):
        print(f'{Fore.BLUE}{Style.BRIGHT}'
              f'{path_to_content}'
              f'{Style.RESET_ALL}')
    else:
        print(f'{path_to_content}')


def print_dir(name, path, string_prefix, new_prefix):
    """
    Prints directory and its content
    :param name: name of directory
    :param path: path to provided folder
    :param string_prefix: prefix for current folder
    :param new_prefix: prefix for every immediate child of provided dir
    :return: None
    """
    try:
        print(f"{string_prefix}"
              f"{Fore.BLUE}{Style.BRIGHT}"
              f"{name}"
              f"{Style.RESET_ALL}",
              end='')
        print_tree(path, new_prefix)
    except OSError:
        print(' [error opening dir]')


def print_tree(path: str, upper_dirs_prefix: str):
    """
    Prints tree for object at path
    :param path: dir location
    :param upper_dirs_prefix: prefix before each file in cur dir
    :return: None
    """
    files = sorted(os.listdir(path), key=lambda x: x.replace('.', '')
                   .replace('_', "").lower())
    print()
    for idx, object_name in enumerate(files):
        is_last = (idx == len(files) - 1)

        file_symbol = '└' if is_last else '├'
        cur_prefix = upper_dirs_prefix + file_symbol + '── '

        new_path = os.path.join(path, object_name)
        new_prefix = upper_dirs_prefix + ('    ' if is_last else '│   ')

        if os.path.islink(new_path):
            print_link(object_name, path, cur_prefix)
        elif os.path.isdir(new_path):
            print_dir(object_name, new_path, cur_prefix, new_prefix)
        else:
            print(f"{cur_prefix}{object_name}")


def main():
    """
    A main function
    :return: None
    """
    args = get_args()
    print_dir(os.path.normpath(args.path), args.path, '', '')


if __name__ == '__main__':
    main()
