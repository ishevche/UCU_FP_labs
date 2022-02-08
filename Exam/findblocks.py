def find_sentences_block(path):
    """
    Finds the longest N*N block and all numbers
    that have equal amount of blocks
    :param path: path to the file with text
    :return: list of lists with N sentences of N words where N is maximal
        and tuple of numbers M that have equal amount of blocks
    """
    input_lines = read_file(path)
    counted_words = count_words(input_lines)
    blocks = get_blocks(counted_words)
    max_sentences_block_len = get_max_sentence_block_len(blocks)
    max_sentences_block = get_sentence_block(blocks[max_sentences_block_len],
                                             counted_words,
                                             max_sentences_block_len)
    return max_sentences_block, get_tuple(blocks)


def read_file(path: str):
    """
    Reads file and returns its lines
    :param path: path to the file to read
    :return: list of strings with data
    """
    lines = []
    with open(path, 'r', encoding='utf-8') as input_file:
        for line in input_file.readlines():
            lines += [line.replace('\n', '')]
    return lines


def count_words(lines: list):
    """
    Counts amount of words in every sentence
    :param lines: list of sentences
    :return: list of tuples, each of them is number of words in
        corresponding sentence and list of these words
    >>> count_words(['— Давай - давай !', 'Таке , як у Києві .'])
    [(2, ['Давай', 'давай']), (4, ['Таке', 'як', 'у', 'Києві'])]
    """
    symbols = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЭЮЯІЇҐЄ' \
              'абвгдежзийклмнопрстуфхцчшщьюяєіїґє' \
              "1234567890'"
    answer_list = []
    for sentence in lines:
        words = []
        entries = sentence.split(' ')
        words_counter = 0
        for entry in entries:
            if not entry:
                continue
            if entry[0] in symbols:
                words_counter += 1
                words += [entry]
        answer_list += [(words_counter, words)]
        if words_counter == 0:
            pass
    return answer_list


def get_blocks(sentences: list):
    """
    Gets sentences index for each N
    :param sentences: list from count_words function
    :return: dictionary with keys - amount of words,
        values - list of indexes of sentences with this amount of words

    >>> get_blocks([(2, ['Давай', 'давай']), \
    (4, ['Таке', 'як', 'у', 'Києві']), \
    (4, ['от', 'знайдибіда', 'авантюрист', 'шмаркатий'])]) == \
    {2: [0], 4: [1, 2]}
    True
    """
    ans_dict = {}
    for idx, sentence in enumerate(sentences):
        words_amount = sentence[0]
        if words_amount in ans_dict:
            ans_dict[words_amount].append(idx)
        else:
            ans_dict[words_amount] = [idx]
    return ans_dict


def get_max_sentence_block_len(blocks: dict):
    """
    Gets the maximum N that has a block
    >>> get_max_sentence_block_len({2: [0, 10], 4: [1, 2, 3, 4], \
    5: [5, 6, 7, 8]})
    4
    """
    block_amounts = list(map(lambda x: (x[0], len(x[1])), blocks.items()))
    numbers_with_blocks = list(filter(lambda x: x[0] <= x[1], block_amounts))
    sorted_blocks_amount = list(sorted(numbers_with_blocks,
                                       key=lambda x: x[0], reverse=True))
    return sorted_blocks_amount[0][0]


def get_sentence_block(sentences, words, length):
    """
    Gets block of given length
    :param sentences: sentences indexes with such amount pf words
    :param words: list of tuples (words amount, words list)
    :param length: length of the block
    :return:
    >>> get_sentence_block([1, 2, 3, 4, 5], \
    [(2, ['Давай', 'давай']), \
    (4, ['Таке', 'як', 'a', 'Києві']), \
    (4, ['Таке', 'як', 'b', 'Києві']), \
    (4, ['Таке', 'як', 'c', 'Києві']), \
    (4, ['Таке', 'як', 'd', 'Києві']), \
    (4, ['Таке', 'як', 'e', 'Києві'])], 4)
    [['Таке', 'як', 'a', 'Києві'], ['Таке', 'як', 'b', 'Києві'], \
['Таке', 'як', 'c', 'Києві'], ['Таке', 'як', 'd', 'Києві']]
    """
    ans = []
    for i in range(length):
        ans += [words[sentences[i]][1]]
    return ans


def get_tuple(blocks):
    """
    Gets tuple with numbers that have equa; amount of blocks
    :param blocks: dictionary with keys - number of words,
        values - sentences indexes with such amount of words
    :return: tuple with numbers
    >>> get_tuple({1: {0, 1}, 2: {0, 1, 2, 3}, 3: {0, 1, 2}, 4: {1}, \
    5: {0, 1, 2, 3, 4}})
    (1, 2, 3, 5)
    """
    lst = list(map(lambda x: (x[0], len(x[1]) // x[0]), blocks.items()))
    dictionary = {}
    ans = []
    for num, amount in lst:
        if amount in dictionary:
            dictionary[amount] += [num]
        else:
            dictionary[amount] = [num]
    for a in dictionary.items():
        if len(a[1]) > 1:
            ans += a[1]
    return tuple(ans)


if __name__ == '__main__':
    print(find_sentences_block('Nestayko_sents.txt'))
