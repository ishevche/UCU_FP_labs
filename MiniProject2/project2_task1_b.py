"""Replaces some string on other specified as arguments"""
import argparse
import sys


def get_args():
    """
    Get args specified in the cmd
    :return: Namespace object with all arguments
    """
    parser = argparse.ArgumentParser(
        description='Replace all strings in given file'
    )
    parser.add_argument(
        'source',
        type=str,
        help='string to replace',
        metavar='old-string'
    )
    parser.add_argument(
        'dest',
        type=str,
        help='string on which replace',
        metavar='new-string'
    )
    parser.add_argument(
        'path',
        type=str,
        help='file in which changes should be done',
        metavar='path'
    )
    parser.add_argument(
        '--inplace',
        action='store_const',
        const=write_result_in_file,
        default=lambda x, y: print(y),
        dest='out',
        help='changes the file (default: prints changed content)'
    )
    return parser.parse_args()


def read_from_file(path: str) -> str:
    """
    Reads content from file located at <path>
    :param path: file location
    :return: content of the file
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f'No such file: \'{path}\'')
        sys.exit()
    except IsADirectoryError:
        print(f'Found directory by path \'{path}\' (should be a file)')
        sys.exit()
    except OSError:
        print(f'Something went wrong upon reading file \'{path}\'')
        sys.exit()


def write_result_in_file(path, content):
    try:
        with open(path, 'w') as output:
            output.write(content)
    except OSError:
        print(f'Something went wrong upon writing to file \'{path}\'')


def main():
    """
    A main function
    :return: None
    """
    args = get_args()
    content = read_from_file(args.path) \
        .replace(args.source, args.dest)
    args.out(args.path, content)


if __name__ == '__main__':
    main()
