"""Calendar"""

import re
import calendar as calendar_lib


def weekday_name(number: int) -> str:
    """
    Return a string representing a weekday
    (one of "mon", "tue", "wed", "thu", "fri", "sat", "sun")
    number : an integer in range [0, 6]

    >>> weekday_name(3)
    'thu'
    """
    return ("mon", "tue", "wed", "thu", "fri", "sat", "sun")[number]


def weekday(date: str) -> int:
    """
    Return an integer representing a weekday
    (0 represents monday and so on)
    Read about algorithm as Zeller's Congruence
    date : a string of form "day.month.year
    if the date is invalid raises AssertionError
    with corresponding message

    >>> weekday("12.08.2015")
    2
    >>> weekday("28.02.2016")
    6
    """
    date_lst = re.findall(r"^(\d\d)\.(\d\d)\.(\d\d\d\d)$", date)[0]
    if date_lst:
        # print(date_lst)
        return calendar_lib.weekday(int(date_lst[2]),
                                    int(date_lst[1]),
                                    int(date_lst[0]))
    else:
        raise AssertionError


def calendar(month: int, year: int) -> str:
    """Return a string representing a\
    horizontal calendar for the given month and year.

    month : an integer in range [1 , 12]
    year : an integer (strictly speaking the algorithm in weekday
           works correctly only for Gregorian calendar, so year must
           be greater than 1583)
    when arguments are invalid raises AssertionError with corresponding
    message

    >>> print(calendar(8 , 2015))
    mon tue wed thu fri sat sun
                          1   2
      3   4   5   6   7   8   9
     10  11  12  13  14  15  16
     17  18  19  20  21  22  23
     24  25  26  27  28  29  30
     31
    """
    ans = "mon tue wed thu fri sat sun"
    day_iter = calendar_lib.Calendar(calendar_lib.MONDAY)\
        .itermonthdays2(year, month)
    for day_num, weekday_num in day_iter:
        if day_num == 0 and len(ans) > 100:
            break
        if weekday_num != 0:
            ans += ' '
        else:
            ans += '\n'
        if day_num == 0:
            ans += '   '
        else:
            ans += f'{day_num: 3}'
    return ans


def transform_calendar(cal: str) -> str:
    """Return a modified horizontal -> vertical calendar.

    calendar is a string of a calendar, returned by the calendar()
    function.
    >>> print(transform_calendar(calendar(5, 2002)))
    mon   6 13 20 27
    tue   7 14 21 28
    wed 1 8 15 22 29
    thu 2 9 16 23 30
    fri 3 10 17 24 31
    sat 4 11 18 25
    sun 5 12 19 26
    >>> print(transform_calendar(calendar(8 , 2015)))
    mon   3 10 17 24 31
    tue   4 11 18 25
    wed   5 12 19 26
    thu   6 13 20 27
    fri   7 14 21 28
    sat 1 8 15 22 29
    sun 2 9 16 23 30
    """
    cal_weeks = [x.split() for x in cal.split('\n')[1:]]
    first_week = cal_weeks[0]
    cal_weeks = cal_weeks[1:]
    ans = ''
    for row in range(7):
        ans += weekday_name(row)
        if row + len(first_week) == 7:
            ans += f' {first_week[0]}'
            first_week.pop(0)
        else:
            ans += '  '
        for week in cal_weeks:
            if len(week) > row:
                ans += f' {week[row]}'
        ans += '\n'
    return ans[:-1]


if __name__ == '__main__':
    try:
        print("Type month")
        input_month = input()
        input_month = int(input_month)
        print("Type year")
        input_year = input()
        input_year = int(input_year)
        print("\n\nThe calendar is: ")
        print(calendar(input_month, input_year))
    except ValueError as err:
        print(err)
