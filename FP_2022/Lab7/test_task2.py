"""
test_validator.py
"""

from unittest import TestCase

from task2 import Validator


class TestValidator(TestCase):
    def test_all_together(self):
        """
        data - string in format "name_surname,age,country,region,living_place,
        index,phone,email,id" can also be whitespaces between sections and
        allowed separator is ";" all previous criteria are valid
        """
        valid = Validator()
        self.assertEqual(valid.validate("Elvis Presley,20,Ukraine,Lviv,"
                                        "Koselnytska st. 2a,79000,"
                                        "+380951234567,"
                                        "username@domain.com,123450"), True)
        self.assertEqual(valid.validate("Elvis Presley;20;Ukraine;Lviv;"
                                        "Koselnytska st. 2a;79000;"
                                        "+380951234567;"
                                        "username@domain.com;123450"), True)
        self.assertEqual(valid.validate("Elvis Presley; 20; Ukraine; Lviv; "
                                        "Koselnytska st. 2a; 79000; "
                                        "+380951234567; "
                                        "username@domain.com; 123450"), True)
        self.assertEqual(valid.validate("Elvis Presley, 20, Ukraine, "
                                        "Lviv, Koselnytska st. 2a, 79000, "
                                        "+380951234567, "
                                        "username@domain.com, 123450"), True)

    def test_id(self):
        """
        valid id - exactly 6 digits, but should contain 
        exactly one zero - at any position
        """
        valid = Validator()
        self.assertEqual(valid.validate_id("123450"), True)
        self.assertEqual(valid.validate_id("011111"), True)
        self.assertEqual(valid.validate_id("123456"), False)
        self.assertEqual(valid.validate_id("123006"), False)
        self.assertEqual(valid.validate_id("1230916"), False)
        self.assertEqual(valid.validate_id("12306"), False)

    def test_email(self):
        """
        valid email should be in format "username@domain.type" username - 
        any letters, digits, any of "!#$%&'*+-/=?^_`{|}~", dots (provided 
        that it its not the first or last character and provided also that it 
        does not appear consecutively), at least 1, at most 64
        domain - only lowercase letters, at least 1, at most 255, but
        be careful - can be also "." - for example @ucu.edu.ua
        type : "com", "org", "edu", "gov", "net", "ua",...."""
        valid = Validator()
        self.assertEqual(valid.validate_email("username@domain.com"), True)
        self.assertEqual(valid.validate_email(
            "username+usersurname@domain.com"),
            True
        )
        self.assertEqual(valid.validate_email("username@ucu.edu.ua"), True)
        self.assertEqual(valid.validate_email("usernamedomain.com"), False)
        self.assertEqual(valid.validate_email("username@domaincom"), False)
        self.assertEqual(valid.validate_email("username@domain.aaa"), False)
        self.assertEqual(valid.validate_email("username@aaa"), False)
        self.assertEqual(valid.validate_email("@domain.com"), False)

    def test_phone(self):
        """
        valid phone - in format "+380951234567" or "+38 (095) 123-45-67"
        starts wit "+" and has from 9 to 12 numbers
        """
        valid = Validator()
        self.assertEqual(valid.validate_phone("+380951234567"), True)
        self.assertEqual(valid.validate_phone("+38 (095) 123-45-67"), True)
        self.assertEqual(valid.validate_phone("38 (095) 123-45-67"), False)
        self.assertEqual(valid.validate_phone("380951234567"), False)
        self.assertEqual(valid.validate_phone("-380951234567"), False)
        self.assertEqual(valid.validate_phone("+3810951234567"), False)
        self.assertEqual(valid.validate_phone("+20951234567"), True)

    def test_index(self):
        """
        valid index - exactly 5 digits
        """
        valid = Validator()
        self.assertEqual(valid.validate_index("79000"), True)
        self.assertEqual(valid.validate_index("7900"), False)
        self.assertEqual(valid.validate_index("790000"), False)
        self.assertEqual(valid.validate_index("7900q"), False)
        self.assertEqual(valid.validate_index("790 00"), False)

    def test_living_place(self):
        """
        living place - should be in format: "Koselnytska st. 2a"
        name of street - between 3 and 20 chars, first character uppercase,
        no digits in it
        type of street - should be "st.", "av.", "prosp." or "rd."
        number of building - exactly 2 symbols, first should be number,
        second can be number or small letter
        """
        valid = Validator()
        self.assertEqual(valid.validate_living_place("Koselnytska st. 2a"),
                         True)
        self.assertEqual(valid.validate_living_place("koselnytska st. 2a"),
                         False)
        self.assertEqual(valid.validate_living_place("Koselnytska provulok 2a"),
                         False)
        self.assertEqual(valid.validate_living_place("Koselnytska st. 2"),
                         False)
        self.assertEqual(valid.validate_living_place("Koselnytska st. a2"),
                         False)
        self.assertEqual(valid.validate_living_place("Koselnytska st. 22"),
                         True)

    def test_region(self):
        """
        valid region - the same as country, but can contain numbers
        """
        valid = Validator()
        self.assertEqual(valid.validate_region("Lviv"), True)
        self.assertEqual(valid.validate_region("Lviv1"), True)
        self.assertEqual(valid.validate_region("L"), False)
        self.assertEqual(valid.validate_region("lviv"), False)

    def test_country(self):
        """
        valid country - between 2 and 10 chars, first letter should be
        uppercase, can`t contain numbers
        """
        valid = Validator()
        self.assertEqual(valid.validate_country("Ukraine"), True)
        self.assertEqual(valid.validate_country("U"), False)
        self.assertEqual(valid.validate_country("UUUUUUUUUUUUUUUUUUUUUUU"),
                         False)
        self.assertEqual(valid.validate_country("Ukraine1"), False)
        self.assertEqual(valid.validate_country("ukraine"), False)
        self.assertEqual(valid.validate_country("USA"), True)

    def test_age(self):
        """
        valid age id digit between 16 and 99
        """
        valid = Validator()
        self.assertEqual(valid.validate_age("20"), True)
        self.assertEqual(valid.validate_age("7"), False)
        self.assertEqual(valid.validate_age("100"), False)
        self.assertEqual(valid.validate_age("20."), False)
        self.assertEqual(valid.validate_age("20a"), False)

    def test_name_surname(self):
        """
        two words, should be only first uppercase letter in name and surname,
        size of both name and surname should be between 2 and 30,
        no digits or punctuation in name or surname
        """
        valid = Validator()
        self.assertEqual(valid.validate_name_surname("Elvis Presley"), True)
        self.assertEqual(valid.validate_name_surname("ElvisPresley"), False)
        self.assertEqual(valid.validate_name_surname("Elvis Presley forever"),
                         False)
        self.assertEqual(valid.validate_name_surname("elvis Presley"), False)
        self.assertEqual(valid.validate_name_surname("Elvis presley"), False)
        self.assertEqual(valid.validate_name_surname("Elvis PResley"), False)
        self.assertEqual(valid.validate_name_surname(
            "Elvis Presleyqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"), False)
        self.assertEqual(valid.validate_name_surname("Elvis P"), False)
        self.assertEqual(valid.validate_name_surname("Elvis P,resley"), False)
        self.assertEqual(valid.validate_name_surname("El1vis Presley"), False)
