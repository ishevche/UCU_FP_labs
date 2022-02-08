def caesar_encode(message, key):
    """
    Encodes message by shifting each letter of message
    on key position forward
    :param message: text to encode
    :param key: number of positions to shift
    :return: encoded message

    >>> caesar_encode("computer", 3)
    'frpsxwhu'
    >>> caesar_encode("vwxyz", 1)
    'wxyza'
    """
    alphabet_length = ord('z') - ord('a') + 1
    key %= alphabet_length
    ans = ''
    for letter in message:
        if letter == ' ':
            ans += ' '
            continue
        letter_pos = ord(letter) - ord('a')
        new_letter_pos = (letter_pos + key) % alphabet_length
        ans += chr(new_letter_pos + ord('a'))
    return ans


def caesar_decode(message, key):
    """
    Decodes message by shifting each letter of message
    on key position backward
    :param message: text to decode
    :param key: number of positions to shift
    :return: decoded message

    >>> caesar_decode("frpsxwhu", 3)
    'computer'
    >>> caesar_decode("wxyza", 1)
    'vwxyz'
    """
    alphabet_length = ord('z') - ord('a') + 1
    key %= alphabet_length
    ans = ''
    for letter in message:
        if letter == ' ':
            ans += ' '
            continue
        letter_pos = ord(letter) - ord('a')
        new_letter_pos = letter_pos - key + alphabet_length
        new_letter_pos %= alphabet_length
        ans += chr(new_letter_pos + ord('a'))
    return ans
