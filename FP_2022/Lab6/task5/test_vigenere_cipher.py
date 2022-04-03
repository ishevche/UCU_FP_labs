import unittest

from vigenere_cipher import VigenereCipher
from vigenere_cipher import combine_character
from vigenere_cipher import separate_character


class TestVigenereCipher(unittest.TestCase):
    def test_encode(self):
        cipher = VigenereCipher("TRAIN")
        encoded = cipher.encode("ENCODEDINPYTHON")
        self.assertEqual(encoded, "XECWQXUIVCRKHWA")

    def test_encode_character(self):
        cipher = VigenereCipher("TRAIN")
        encoded = cipher.encode("E")
        self.assertEqual(encoded, "X")

    def test_encode_spaces(self):
        cipher = VigenereCipher("TRAIN")
        encoded = cipher.encode("ENCODED IN PYTHON")
        self.assertEqual(encoded, "XECWQXUIVCRKHWA")

    def test_encode_lowercase(self):
        cipher = VigenereCipher("TRain")
        encoded = cipher.encode("encoded in Python")
        self.assertEqual(encoded, "XECWQXUIVCRKHWA")

    def test_combine_character(self):
        self.assertEqual(combine_character("E", "T"), "X")
        self.assertEqual(combine_character("N", "R"), "E")

    def test_extend_keyword(self):
        cipher = VigenereCipher("TRAIN")
        extended = cipher.extend_keyword(16)
        self.assertEqual(extended, "TRAINTRAINTRAINT")

    def test_extend_keyword_even(self):
        cipher = VigenereCipher("TRAIN")
        extended = cipher.extend_keyword(15)
        self.assertEqual(extended, "TRAINTRAINTRAIN")

    def test_separate_character(self):
        self.assertEqual(separate_character("X", "T"), "E")
        self.assertEqual(separate_character("E", "R"), "N")

    def test_decode(self):
        cipher = VigenereCipher("TRAIN")
        decoded = cipher.decode("XECWQXUIVCRKHWA")
        self.assertEqual(decoded, "ENCODEDINPYTHON")
