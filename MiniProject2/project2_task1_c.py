"""Caesar en/decrypting"""
import argparse
import sys


def get_args():
    """
    Get args specified in the cmd
    :return: Namespace object with all arguments
    """
    parser = argparse.ArgumentParser(
        description='Encrypts / decrypts file content using caesar code'
    )
    parser.add_argument(
        'path',
        type=str,
        help='file in which changes should be done',
        metavar='path'
    )
    parser.add_argument(
        '--offset',
        type=int,
        default=13,
        help='offset for cesar code',
        metavar='offset'
    )
    parser.add_argument(
        '--decrypt',
        action='store_const',
        const=decrypt,
        default=encrypt,
        dest='process',
        help='decrypt file (default encrypt)',
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


def get_alphabet(char: str) -> str:
    """
    Finds alphabet, char belongs to
    :param char: char to check
    :return: a string of letters
    >>> get_alphabet('я')
    'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
    >>> get_alphabet('Я')
    'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'
    >>> get_alphabet('z')
    'abcdefghijklmnopqrstuvwxyz'
    >>> get_alphabet('Z')
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    >>> get_alphabet(' ')
    """
    ua_lower = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
    ua_upper = ua_lower.upper()
    en_lower = 'abcdefghijklmnopqrstuvwxyz'
    en_upper = en_lower.upper()
    if char in ua_lower:
        return ua_lower
    if char in ua_upper:
        return ua_upper
    if char in en_lower:
        return en_lower
    if char in en_upper:
        return en_upper


def transform_char(char: str, offset: int) -> str:
    """
    Transforms char for caesar code
    :param char: char to transform
    :param offset: number of positions to move
    :return: transformed char
    >>> transform_char('я', 2)
    'б'
    >>> transform_char('Я', 2)
    'Б'
    >>> transform_char('z', 2)
    'b'
    >>> transform_char('Z', 2)
    'B'
    >>> transform_char(' ', 2)
    ' '
    """
    if len(char) != 1:
        raise ValueError("Only chars are allowed")
    alphabet = get_alphabet(char)
    if alphabet is None:
        return char
    new_index = (alphabet.index(char) + offset) % len(alphabet)
    return alphabet[new_index]


def encrypt(text: str, offset: int) -> str:
    """
    Encrypts using caesar code
    :param text: text to encrypt
    :param offset: number of positions to move
    :return: encrypted text
    >>> encrypt('яЯzZ bB 123', 2)
    'бБbB dD 123'
    """
    answer = ''
    for char in text:
        answer += transform_char(char, offset)
    return answer


def decrypt(text: str, offset: int) -> str:
    """
    Decrypts caesar code
    :param text: text to decrypt
    :param offset: offset used while encrypting
    :return: decrypted text
    >>> decrypt('бБbB dD 123', 2)
    'яЯzZ bB 123'
    """
    return encrypt(text, -offset)


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
    content = read_from_file(args.path)
    result = args.process(content, args.offset)
    args.out(args.path, result)


if __name__ == '__main__':
    main()
