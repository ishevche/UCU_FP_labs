"""
Deals with document by url:
http://raw.githubusercontent.com/anrom7/Test_Olya/master/New%20folder/total.txt
"""

import urllib.request
import re


def read_input_file(url, number):
    """
    Reads a file by url
    :param url: a link to the file
    :param number: number of students to read
    :return: list of list with student data in items
    >>> read_input_file("https://raw.githubusercontent.com/anrom7/Test_Olya/"\
    "master/New%20folder/total.txt", 0)
    []
    """
    if number == 0:
        return []
    with urllib.request.urlopen(url) as input_file:
        first_row_regex = re.compile(
            r"^(\d+)\s+(.+?\..+?\.).+?(\d+\.\d+)"
        )
        attestation_regex = re.compile(
            r"Середній\s+бал\s+документа\s+про\s+освіту\s+(\d+\.\d\d)"
        )
        approved_regex = re.compile(
            r"^—\s+([+—])"
        )
        ans_data = []
        for line in input_file:
            line = line.strip().decode('utf-8')
            if first_row_regex.search(line):
                num, name, score = first_row_regex.findall(line)[0]
                ans_data += [[num, name, score]]
            elif attestation_regex.search(line):
                grade = attestation_regex.findall(line)[0]
                ans_data[-1] += [grade]
            elif approved_regex.search(line):

                approved = approved_regex.findall(line)[0]
                ans_data[-1].insert(2, approved)
                if len(ans_data) == number:
                    break
    return ans_data


def write_csv_file(url):
    """
    Writes down the students information
    :param url: a link to the file
    :return: None
    """
    with open("total.csv", 'w') as output_file:
        output_file.write("№,ПІБ,Д,Заг.бал,С.б.док.осв.\n")
        lst = read_input_file(url, -1)
        for student_data in lst:
            output_file.write(f"{','.join(student_data)}\n")
