"""olympics_process.py"""
import pandas as pd


def read_data():
    """Reads data from file"""
    df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)
    for col in df.columns:
        if col[:2] == '01':
            df.rename(columns={col: 'Gold' + col[4:]}, inplace=True)
        elif col[:2] == '02':
            df.rename(columns={col: 'Silver' + col[4:]}, inplace=True)
        elif col[:2] == '03':
            df.rename(columns={col: 'Bronze' + col[4:]}, inplace=True)
        elif col[:1] == '№':
            df.rename(columns={col: '#' + col[1:]}, inplace=True)

    names_ids = df.index.str.split('\\s\\(')  # split the index by '('

    # the [0] element is the country name (new index)
    df.index = names_ids.str[0]
    # the [1] element is the abbreviation or ID
    # (take first 3 characters from that)
    df['ID'] = names_ids.str[1].str[:3]

    df = df.drop('Totals')
    # print(df)

    return df


def first_country(df):
    """
    Returns a series object of first country
    :param df: a frame of data
    :return: a series object of first country
    >>> a = pd.DataFrame([[1, 2, 3], [5, 6, 7]], \
                         columns=['Gold', 'Silver', 'Bronze'])
    >>> first_country(a)
    Gold      1
    Silver    2
    Bronze    3
    Name: 0, dtype: int64
    """
    return df.iloc[0]


def summer_biggest(df):
    """
    Returns the name of country with the biggest amount of gold medals
    in summer
    :param df: a frame of data
    :return: string - the name of country
    >>> a = pd.DataFrame([[1, 2, 3], [5, 6, 7]], \
                         columns=['Gold', 'Silver', 'Bronze'])
    >>> summer_biggest(a)
    1
    """
    return df['Gold'].idxmax()


def difference_biggest(df):
    """
    Returns the name of country with the biggest difference between
    amount of gold medals in winter and summer
    :param df: a frame of data
    :return: a name of country
    >>> a = pd.DataFrame([[1, 2, 3], [6, 6, 7]], \
                         columns=['Gold', 'Gold.1', 'Gold.2'])
    >>> difference_biggest(a)
    0
    """
    return df['Gold'].multiply(-1).add(df['Gold.1']).abs().idxmax()


def difference_biggest_relative(df):
    """
    Returns the name of country with the biggest difference between
    amount of gold medals in winter and summer relatively to the
    overall amount of gold medals
    :param df: a frame of data
    :return: a name of country
    >>> a = pd.DataFrame([[1, 2, 3], [1, 6, 7]], \
                         columns=['Gold', 'Gold.1', 'Gold.2'])
    >>> difference_biggest_relative(a)
    1
    """
    matching_df = df[df['Gold'] != 0][df['Gold.1'] != 0]
    series = ((matching_df['Gold'] - matching_df['Gold.1'])
              / matching_df['Gold.2']).abs()
    return series.idxmax()


def get_points(df):
    """
    Returns a series of points calculated for each country as
    3 * gold + 2 * silver + bronze
    :param df: a frame of data
    :return: a series object
    >>> a = pd.DataFrame([[1, 2, 3], [1, 6, 7]], \
                         columns=['Gold.2', 'Silver.2', 'Bronze.2'])
    >>> get_points(a)
    0    10
    1    22
    Name: Points, dtype: int64
    """
    points = df['Gold.2']*3 + df['Silver.2']*2 + df['Bronze.2']
    points.name = 'Points'
    df.join(points)
    return points
