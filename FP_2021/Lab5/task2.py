def dyvo_insert(sentence, flag):
    """
    Inserting word "диво" before every word that starts with flag.

    >>> dyvo_insert("hah", "ha")
    'дивоhah'
    >>> dyvo_insert("abcd", "bac")
    'abcd'
    """
    return sentence.lower().replace(flag, "диво" + flag)
