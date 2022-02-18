"""
kved_parser.py
"""
import json


def parse_kved(code: str):
    """
    Reads kved.json file and writes data about asked class in kved_result.json
    :param code: code of class to get info about
    :return: None
    """
    with open('kved.json', 'r') as file:
        kved_data = json.load(file)

    answer_data = get_requested_class_data(code, kved_data)

    with open('kved_results.json', 'w') as output:
        json.dump(answer_data, output, ensure_ascii=False, indent=4)


def get_requested_class_data(code, kved_data):
    """
    Gets data about class from kved_data
    Returns data object
    >>> get_requested_class_data('0', {'sections':[[{'sectionName':'s',\
    'divisions':[{'divisionName':'d','groups':[{'groupName':'g', 'classes':[{\
    "classCode":"0",'className':'c'}]}]}]}]]}) == \
    {'name':'c','type':'class','parent':{'name':'g','type':'group','num_children':1,\
'parent':{'name':'d','type':'division','num_children':1,\
'parent':{'name':'s','type':'section','num_children':1}}}}
    True
    """
    found_class = False
    answer_data = {}
    sections = kved_data['sections'][0]
    for section in sections:
        divisions = section['divisions']
        for division in divisions:
            groups = division['groups']
            for group in groups:
                classes = group['classes']
                for class_ in classes:
                    if class_['classCode'] == code:
                        answer_data['name'] = class_['className']
                        answer_data['type'] = 'class'
                        answer_data['parent'] = {}
                        found_class = True
                        break
                if found_class:
                    answer_data['parent']['name'] = group['groupName']
                    answer_data['parent']['type'] = 'group'
                    answer_data['parent']['num_children'] = len(classes)
                    answer_data['parent']['parent'] = {}
                    break
            if found_class:
                answer_data['parent']['parent']['name'] = \
                    division['divisionName']
                answer_data['parent']['parent']['type'] = 'division'
                answer_data['parent']['parent']['num_children'] = len(groups)
                answer_data['parent']['parent']['parent'] = {}
                break
        if found_class:
            answer_data['parent']['parent']['parent']['name'] = \
                section['sectionName']
            answer_data['parent']['parent']['parent']['type'] = 'section'
            answer_data['parent']['parent']['parent']['num_children'] = \
                len(divisions)
            break
    return answer_data


if __name__ == '__main__':
    parse_kved(input())
