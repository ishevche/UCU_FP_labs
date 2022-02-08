"""copy files containing regex to a new zip file"""
import re
import zipfile
import os
import argparse


def get_args():
    """
    Get args specified in the cmd
    :return: Namespace object with all arguments
    """
    parser = argparse.ArgumentParser(
        description='Copy files containing regex to a new zip file'
    )
    parser.add_argument(
        'regex',
        type=str,
        help='regex to search in names',
        metavar='regex'
    )
    parser.add_argument(
        'path',
        type=str,
        help='path to zip file',
        metavar='path'
    )
    parser.add_argument(
        'dest',
        type=str,
        help='path to save new zip file',
        metavar='dest'
    )
    return parser.parse_args()


def search_in_source(path: str, regex: re):
    """
    Searches files in zip at <path> that containing regex in their names
    :param path: location of zip file
    :param regex: regex to contain
    :return: a list of tuples. Each of them is a name of file and its content
    """
    try:
        files_to_copy = []
        with zipfile.ZipFile(path, 'r') as source:
            for file in source.infolist():
                if regex.search(file.filename) is None:
                    continue
                files_to_copy += [(file.filename, source.read(file.filename))]
        return files_to_copy
    except OSError as e:
        print(e)
    except UnicodeDecodeError as e:
        print(e)


def write_to_zip(dest: str, files: list):
    """
    Writes founded files in zip file
    :param dest: location of zip file
    :param files: files to write (from search_in_source)search_in_source
    :return: None
    """
    try:
        parent = os.path.dirname(dest)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with zipfile.ZipFile(dest, 'w') as destination:
            for file_name, content in files:
                destination.writestr(file_name, content)
    except OSError as e:
        print(e)


def main():
    """
    A main function
    :return: None
    """
    args = get_args()
    read_files = search_in_source(args.path, re.compile(args.regex))
    write_to_zip(args.dest, read_files)


if __name__ == '__main__':
    main()
