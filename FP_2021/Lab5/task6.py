def create_acronym(message):
    """
    Makes acronyms out of message
    :param message: message to be converted
    :return: string with acronyms and their definitions

    >>> print(create_acronym("random access memory\\nAs soon As possible"))
    RAM - random access memory
    ASAP - As soon As possible
    """
    list_of_phrases = message.split('\n')
    ans = ''
    for idx, phrase in enumerate(list_of_phrases):
        ans += ''.join([word[0].upper() for word in phrase.split(' ')])
        ans += ' - '
        ans += phrase
        if idx != len(list_of_phrases) - 1:
            ans += '\n'
    return ans
