"""
angle_adt.py
"""


class AngleADT:
    """
    Abstract data type used to encode message in a list of angles
    """

    @staticmethod
    def hex_digit_to_angle(digit: str) -> float:
        """
        Converts hex digit (0-f) to an angel
        """
        num = int(digit) if digit.isdigit() \
            else ord(digit) - ord('a') + 10
        return num * 360 / 16

    @staticmethod
    def char_to_hex_digits(char: str) -> str:
        """
        Converts char to a hex representation
        """
        return hex(ord(char))[2:]

    @staticmethod
    def encode_message(message: str) -> list[float]:
        """
        Encodes a message to a list of turns
        """
        angles_list = []
        for char in message:
            angles_list += list(map(AngleADT.hex_digit_to_angle,
                                    AngleADT.char_to_hex_digits(char)))
        angles_list = [angles_list[0]] + [angles_list[i] - angles_list[i - 1]
                                          for i in range(1, len(angles_list))]
        return [a if a != 0 else 360. for a in angles_list]
