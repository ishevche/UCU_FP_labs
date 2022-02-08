"""Names"""


def common_names(female_names, male_names):
    """
    Searches for common names
    >>> common_names([], [])
    set()
    """
    male_names_set = set(male_names)
    ans = set()
    for female_name in female_names:
        if len(female_name) < 1 or female_name[0] not in "AOEUI":
            continue
        if female_name in male_names_set:
            ans.add(female_name)
    return ans


def names_read(file_name):
    """
    reads file
    :param file_name: path to a file
    :return: list of names
    >>> str(names_read("male.txt"))[:10]
    "['Aamir', "
    """
    with open(file_name, 'r') as input_file:
        return [x[:-1] for x in input_file.readlines()]
