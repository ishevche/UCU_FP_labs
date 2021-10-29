"""history_analysis.py"""


def sites_on_date(visits: list, date: str) -> set:
    """
    Returns set of all urls that have been visited
    on current date
    :param visits: all visits in browser history
    :param date: date in format "yyyy-mm-dd"
    :return: set of url visited on date
    >>> sites_on_date([("https://www.youtube.com/", "YouTube", "2021-10-29", \
    "14:21:16.105392", 44394201)], "2021-10-29")
    {'https://www.youtube.com/'}
    """
    filtered = filter(lambda x: x[2] == date, visits)
    ans = set()
    for element in filtered:
        ans.add(element[0])
    return ans


def most_frequent_sites(visits: list, number: int) -> set:
    """
    Returns set of most frequent sites visited in total
    Return only 'number' of most frequent sites visited
    :param visits: all visits in browser history
    :param number: number of most frequent sites to return
    :return: set of most frequent sites
    >>> most_frequent_sites([("https://www.youtube.com/", "YouTube", "2021-10-29", \
    "14:21:16.105392", 44394201)], 1)
    {'https://www.youtube.com/'}
    """
    dic = {}
    for site in visits:
        if dic.__contains__(site[0]):
            dic[site[0]] += 1
        else:
            dic[site[0]] = 1
    visit_amount = list(dic.items())
    visit_amount.sort(key=lambda x: x[1])
    ans = set()
    for site in visit_amount[-1:- number - 1: -1]:
        ans.add(site[0])
    return ans


def get_url_info(visits: list, url: str) -> tuple:
    """
    Returns tuple with info about site, which title is passed
    Function should return:
    title - title of site with this url
    last_visit_date - date of the last visit of this site, in format
        "yyyy-mm-dd"
    last_visit_time - time of the last visit of this site, in format
        "hh:mm:ss.ms"
    num_of_visits - how much time was this site visited
    average_time - average time, spend on this site
    :param visits: all visits in browser history
    :param url: url of site to search
    :return: (title, last_visit_date, last_visit_time,
        num_of_visits, average_time)
    >>> get_url_info([("https://www.youtube.com/", "YouTube", "2021-10-29", \
    "14:21:16.105392", 44394201)], "https://www.youtube.com/")
    ('YouTube', '2021-10-29', '14:21:16.105392', 1, 44394201.0)
    """
    title = ""
    last_visit_date = ""
    last_visit_time = ""
    num_of_visits = 0
    sum_time = 0
    for site in visits:
        if site[0] != url:
            continue
        if site[2] > last_visit_date or \
                (site[2] == last_visit_date and
                 site[3] > last_visit_time):
            last_visit_time = site[3]
            last_visit_date = site[2]
        num_of_visits += 1
        sum_time += int(site[4])
        title = site[1]
    if num_of_visits != 0:
        return (title, last_visit_date, last_visit_time,
                num_of_visits, sum_time / num_of_visits)
    else:
        return (title, last_visit_date, last_visit_time,
                num_of_visits, 0)


# with open("history.txt", 'r') as file:
#     ans = []
#     for line in file:
#         ans += re.findall(r"^\(\'(.+?)\', \'(.+?)\', "
#                           r"\'(.+?)\', \'(.+?)\', (.+?)\)$", line)
#     print(len(ans))
#     for el in get_url_info(ans, "https://www.youtube.com/"):
#         print(el)
