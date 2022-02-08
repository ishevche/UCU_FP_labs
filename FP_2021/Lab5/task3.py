import calendar


def semester_calendar(output_type, year, first_month, last_month):
    """

    :param output_type: html or txt
    :param year:
    :param first_month: month to start with
    :param last_month: month to end with
    :return: a sting or html string with a calendar in it

    >>> print(semester_calendar("txt", 2021, 10, 10), end="")
        October 2021
    Mo Tu We Th Fr Sa Su
                 1  2  3
     4  5  6  7  8  9 10
    11 12 13 14 15 16 17
    18 19 20 21 22 23 24
    25 26 27 28 29 30 31
    """
    txt_cal = calendar.TextCalendar(calendar.MONDAY)
    html_cal = calendar.HTMLCalendar(calendar.MONDAY)
    ans = ""
    for cur_month in range(first_month, last_month + 1):
        if output_type == "txt":
            ans += txt_cal.formatmonth(year, cur_month)
        else:
            ans += html_cal.formatmonth(year, cur_month)
    return ans
