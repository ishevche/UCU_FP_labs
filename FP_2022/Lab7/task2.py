"""
validator.py
"""

import re


class Validator:
    """
    Validates register info
    """

    def __init__(self):
        self.name_surname_regex = \
            re.compile(r'^[A-Z][a-z]{1,29} [A-Z][a-z]{1,29}$')
        self.age_regex = \
            re.compile(r'^(1[6-9])|([2-9]\d)$')
        self.country_regex = \
            re.compile(r'^[A-Z][A-Za-z]{1,9}$')
        self.region_regex = \
            re.compile(r'^[A-Z]\w{1,9}$')
        self.living_place_regex = \
            re.compile(r'^[A-Z][A-Za-z]{2,19}\s((st)|(av)|(prosp)|(rd))\.\s\d'
                       r'[\da-z]$')
        self.index_regex = \
            re.compile(r'^\d{5}$')
        self.phone_regex = \
            re.compile(r'^\+((\d{9,12})|'
                       r'(\d{1,2}\s\(\d{3}\)\s\d{3}(-\d{2}){2}))$')
        self.email_regex = \
            re.compile(r'^(?!.*\.{2}.*@)(?!\.)'
                       r'[\w!#$%&\'*+\-/=?^`{|}~.]{1,64}(?<!\.)@'
                       r'[a-z.]{1,255}'
                       r'\.((com)|(org)|(edu)|(gov)|(net)|(ua))$')
        self.id_regex = \
            re.compile(r'^(?=.*0)(?!.*0.*0)\d{6}$')

    def validate_name_surname(self, name_surname: str):
        """
        Validates name and surname string
        """
        return bool(self.name_surname_regex.match(name_surname))

    def validate_age(self, age: str):
        """
        Validates age string
        """
        return bool(self.age_regex.match(age))

    def validate_country(self, country: str):
        """
        Validates country string
        """
        return bool(self.country_regex.match(country))

    def validate_region(self, region: str):
        """
        Validates region string
        """
        return bool(self.region_regex.match(region))

    def validate_living_place(self, living_place: str):
        """
        Validates living place string
        """
        return bool(self.living_place_regex.match(living_place))

    def validate_index(self, index: str):
        """
        Validates index string
        """
        return bool(self.index_regex.match(index))

    def validate_phone(self, phone: str):
        """
        Validates phone string
        """
        return bool(self.phone_regex.match(phone))

    def validate_email(self, email: str):
        """
        Validates email string
        """
        return bool(self.email_regex.match(email))

    def validate_id(self, idx: str):
        """
        Validates id string
        """
        return bool(self.id_regex.match(idx))

    def validate(self, data: str):
        """
        Validates data string
        """
        separator = ',' if ',' in data else ';'
        separator += ' ' if separator + ' ' in data else ''
        data_list = data.split(separator)
        return (self.validate_name_surname(data_list[0]) and
                self.validate_age(data_list[1]) and
                self.validate_country(data_list[2]) and
                self.validate_region(data_list[3]) and
                self.validate_living_place(data_list[4]) and
                self.validate_index(data_list[5]) and
                self.validate_phone(data_list[6]) and
                self.validate_email(data_list[7]) and
                self.validate_id(data_list[8]))
