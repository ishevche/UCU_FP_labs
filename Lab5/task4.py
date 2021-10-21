def plus(first, second):
    """Adds arguments"""
    return first + second


def minus(first, second):
    """Subtracts arguments"""
    return first - second


def multiply(first, second):
    """Multiplies arguments"""
    return first * second


def divide(first, second):
    """Divides arguments"""
    return first / second


def calculate_expression(expression):
    """
    Calculates expression
    :param expression: expression to calculate
    :return: a number - the answer on expression
        or a string 'Неправильний вираз!' if something wrong

    >>> calculate_expression("Скільки буде 8 відняти 3?")
    5
    >>> calculate_expression("Скільки буде 7 додати 3 помножити на 5?")
    50
    >>> calculate_expression("Скільки буде 10 поділити на 0 додати 11 мінус -3?")
    9
    >>> calculate_expression("Скільки буде 3 в кубі?")
    'Неправильний вираз!'
    """
    try:
        list_of_words = expression.split(' ')
        if list_of_words[0] != "Скільки" or \
                list_of_words[1] != "буде":
            raise ValueError()
        list_of_words = list_of_words[2:]
        list_of_words[-1] = list_of_words[-1][:-1]
        ans = 0
        operation = plus
        cur_pos = 0
        while cur_pos < len(list_of_words):
            number = int(list_of_words[cur_pos])
            ans = operation(ans, number)
            if cur_pos == len(list_of_words) - 1:
                break
            if list_of_words[cur_pos + 1] == "додати" or \
                    list_of_words[cur_pos + 1] == "плюс":
                operation = plus
                cur_pos += 2
            elif list_of_words[cur_pos + 1] == "відняти" or \
                    list_of_words[cur_pos + 1] == "мінус":
                operation = minus
                cur_pos += 2
            elif list_of_words[cur_pos + 1] == "помножити" and \
                    list_of_words[cur_pos + 2] == "на":
                operation = multiply
                cur_pos += 3
            elif list_of_words[cur_pos + 1] == "поділити" and \
                    list_of_words[cur_pos + 2] == "на":
                operation = divide
                cur_pos += 3
            else:
                raise ValueError()
        return int(ans)
    except ValueError:
        return 'Неправильний вираз!'
    except IndexError:
        return 'Неправильний вираз!'
    except ZeroDivisionError:
        return 'Неправильний вираз!'
