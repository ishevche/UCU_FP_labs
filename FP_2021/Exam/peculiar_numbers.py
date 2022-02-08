"""
This module deals with math teacher problem computing right answer
"""


def read_numbers(path: str) -> list:
    """
    Read the numbers file and return a list of numbers as strings.
    :param path: path to the file to read

    >>> read_numbers("digits.txt")
    ['731711196', '116410407', '???324321', '995549301', '672734697', \
'158484???', '456???233']
    """
    with open(path, 'r', encoding='utf-8') as input_file:
        cols = []
        for line in input_file.readlines():
            line = line.replace('\n', '')
            if not cols:
                cols = [''] * len(line)
            for idx, digit in enumerate(line):
                cols[idx] += digit
        return cols


def find_missing_numbers(numbers: list) -> list:
    """
    Find positions where the missing numbers "???" are located.
    Return list of tuples (column_index, name_of_the_digit)
    where name_of_the_digit could be any of {first, central, last}
    depending on their position.

    >>> find_missing_numbers(['731711196', '116410407', '???324321',\
     '995549301', '672734697', '158484???', '456???233'])
    [(2, 'first'), (5, 'last'), (6, 'central')]
    """
    answer_tuples = []
    for idx, column in enumerate(numbers):
        unknown_pos = column.find('???')
        if unknown_pos == -1:
            continue
        elif unknown_pos == 0:
            answer_tuples += [(idx, 'first')]
        elif unknown_pos == 3:
            answer_tuples += [(idx, 'central')]
        else:
            answer_tuples += [(idx, 'last')]
    return answer_tuples


def impute_missing_numbers(numbers: list, missing_positions: list,
                           inplace=False):
    """
    Impute missing numbers, if inplace=False, replace the found missing
    numbers in their lines and return a list of found missing numbers,
    if inplace=True, replace the found missing numbers in their lines.

    >>> impute_missing_numbers(['731711196', '116410407', '???324321', \
    '995549301', '672734697', '158484???', '456???233'] \
    , missing_positions=[(2, 'first'), (5, 'last'), (6, 'central')], \
    inplace=False)
    [(2, 'first', '525'), (5, 'last', '018'), (6, 'central', '394')]
    >>> impute_missing_numbers(['731711196', '116410407', '???324321', \
    '995549301', '672734697', '158484???', '456???233'] \
    , missing_positions=[(2, 'first'), (5, 'last'), (6, 'central')], \
    inplace=True)
    >>> impute_missing_numbers(['730365???'], missing_positions=[(0, 'last')])
    [(0, 'last', '000')]
    """
    answer_tuples = []
    for idx, position in missing_positions:
        column = numbers[idx]
        first_num = column[:3]
        central_num = column[3:-3]
        last_num = column[-3:][::-1]
        if position == 'first':
            first_num = str(int(central_num) * 2 - int(last_num))
            answer_tuples += [(idx, position, first_num)]
        elif position == 'central':
            central_num = str((int(last_num) + int(first_num)) // 2)
            answer_tuples += [(idx, position, central_num)]
        else:
            last_num = f'{int(central_num) * 2 - int(first_num):{0}3}'
            answer_tuples += [(idx, position, last_num[::-1])]
        if inplace:
            numbers[idx] = first_num + central_num + last_num[::-1]
    if not inplace:
        return answer_tuples


def check_central_numbers(numbers: list) -> bool:
    """Check the peculiarity of the numbers.
    Check compliance with the rules.

    >>> check_central_numbers(['731711196', '116410407', \
    '525324321', '995549301', '672734697', '158484018', '456394233'])
    True
    >>> check_central_numbers(['731711194', '116410407', \
    '525324321', '995549301', '672734697', '158484018', '456394233'])
    False
    """
    for column in numbers:
        first = column[:3]
        central = column[3:-3]
        last = column[-3:][::-1]
        if (int(first) + int(last)) // 2 != int(central):
            return False
    return True


def write_imputed(imputed_numbers: list):
    """
    Write the imputed and checked results
    to the "peculiar_numbers_imputed.txt" file.
    """
    rows = [''] * 9
    for col in imputed_numbers:
        for idx, digit in enumerate(col):
            rows[idx] += digit

    with open("peculiar_numbers_imputed.txt", 'w', encoding='utf-8') as output:
        output.write('\n'.join(rows))
        output.write('\n')


if __name__ == '__main__':
    import doctest
    data = read_numbers('digits.txt')
    missing = find_missing_numbers(data)
    impute_missing_numbers(data, missing, True)
    print(check_central_numbers(data))
    write_imputed(data)
    print(doctest.testmod())
