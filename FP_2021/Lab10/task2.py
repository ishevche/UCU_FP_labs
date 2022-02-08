"""counties_process.py"""
import pandas as pd


def read_data(path_to_file):
    """
    Reads data from file
    :param path_to_file: file from where to read
    :return: a DataFrame object
    """
    return pd.read_csv(path_to_file)


def max_counties(df):
    """
    Finds state with maximal amount of counties
    :param df: a frame of data
    :return: string - name of state
    >>> a = pd.DataFrame({'SUMLEV': [40, 50, 50, 50], \
    'STNAME': ['Alabama', 'Alabama', 'Alabama', 'Arizona']})
    >>> max_counties(a)
    'Alabama'
    """
    return df[df.SUMLEV == 50].groupby(['STNAME']).size().idxmax()


def max_difference(df):
    """
    Returns a name of county with max difference in amonunt of
    inhabitants in 2010-2015 years
    :param df: a frame of data
    :return: string - a name of county
    >>> a = pd.DataFrame({'SUMLEV': [40, 50, 50, 50, 50], \
    'STNAME': ['Alabama', 'Alabama', 'Alabama', 'Alabama', 'Arizona'], \
    'POPESTIMATE2010': [1, 2, 3, 2, 1], \
    'POPESTIMATE2011': [2, 2, 3, 2, 1], \
    'POPESTIMATE2012': [3, 2, 3, 5, 1], \
    'POPESTIMATE2013': [2, 2, 4, 2, 1], \
    'POPESTIMATE2014': [1, 2, 3, 2, 1], \
    'POPESTIMATE2015': [1, 2, 3, 2, 1], \
    'CTYNAME': ['a', 'b', 'c', 'd', 'e']})
    >>> max_difference(a)
    'd'
    """
    df = df[df.SUMLEV == 50]
    max_value = df[['POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012',
                    'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015']] \
        .max(axis=1)
    min_value = df[['POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012',
                    'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015']] \
        .min(axis=1)
    diff = max_value - min_value
    diff.name = 'diff'
    idxmax = diff.idxmax()
    return df['CTYNAME'][idxmax]


def conditional_counties(df):
    """
    Finds counties with special requirements
    :param df: a frame of data
    :return: a frame of data
    >>> a = pd.DataFrame({'SUMLEV': [40, 50, 50, 50, 50], \
    'STNAME': ['Alabama', 'Alabama', 'Alabama', 'Alabama', 'Arizona'], \
    'REGION': [1, 1, 1, 1, 1], \
    'POPESTIMATE2010': [1, 2, 3, 2, 1], \
    'POPESTIMATE2011': [2, 2, 3, 2, 1], \
    'POPESTIMATE2012': [3, 2, 3, 5, 1], \
    'POPESTIMATE2013': [2, 2, 4, 2, 1], \
    'POPESTIMATE2014': [1, 2, 3, 2, 1], \
    'POPESTIMATE2015': [1, 2, 5, 4, 1], \
    'CTYNAME': ['a', 'b', 'Washington', 'd', 'e']})
    >>> conditional_counties(a)
        STNAME     CTYNAME
    2  Alabama  Washington
    """
    county = df[df.SUMLEV == 50]
    region12 = county[county.REGION > 0][county.REGION < 3]
    population = region12[region12.POPESTIMATE2015 > region12.POPESTIMATE2014]
    washington = population[population['CTYNAME'].str.contains('Washington')]
    return washington[['STNAME', 'CTYNAME']]
