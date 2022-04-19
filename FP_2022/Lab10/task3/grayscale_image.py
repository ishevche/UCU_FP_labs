"""
grayscale_image.py
"""

from arrays import Array2D


class GrayscaleImage:
    """
    Represents a black - white image
    """

    def __init__(self, rows, cols):
        self.image = Array2D(rows, cols)
        self.clear(0)

    def width(self):
        """
        Returns width of the image
        """
        return self.image.num_cols()

    def height(self):
        """
        Returns height of the image
        """
        return self.image.num_rows()

    def clear(self, value):
        """
        Sets every pixel to a value
        """
        if 0 <= value <= 255:
            self.image.clear(value)
        else:
            raise ValueError("Value must be between 0 and 255")

    def getitem(self, row, col):
        """
        Returns value of pixel at given coordinates
        """
        if 0 <= row < self.height() and 0 <= col < self.width():
            return self.image[row, col]
        else:
            raise IndexError("Row number must be in range from "
                             f"0 to {self.height() - 1} and "
                             f"col number must be in range from "
                             f"0 to {self.width() - 1} and ")

    def setitem(self, row, col, value):
        """
        Sets value at given coordinates
        """
        if 0 <= value <= 255:
            if 0 <= row < self.height() and 0 <= col < self.width():
                self.image[row, col] = value
            else:
                raise IndexError("Row number must be in range from "
                                 f"0 to {self.height() - 1} and "
                                 f"col number must be in range from "
                                 f"0 to {self.width() - 1} and ")
        else:
            raise ValueError("Value must be between 0 and 255")

    def show(self):
        """
        Shows an image on a screen
        """
        import numpy as np
        from PIL import Image
        array = np.array([[self.image[i, j]
                           for j in range(self.image.num_cols())]
                          for i in range(self.image.num_rows())]) \
            .astype(np.uint8)
        print(array)
        image = Image.fromarray(array)
        image.show()

    def lzw_compression(self):
        """
        Compressing an image using lzw
        """
        dict_size = 257
        dictionary = dict(((i,), i) for i in range(dict_size))

        prefix = []
        result = []
        for i in range(self.height()):
            for j in range(self.width()):
                element = self.image[i, j]
                string = prefix + [element]
                if tuple(string) in dictionary:
                    prefix = string
                else:
                    result += [dictionary[tuple(prefix)]]

                    dictionary[tuple(string)] = dict_size
                    dict_size += 1
                    prefix = [element]
            string = prefix + [256]
            if tuple(string) in dictionary:
                prefix = string
            else:
                result += [dictionary[tuple(prefix)]]

                dictionary[tuple(string)] = dict_size
                dict_size += 1
                prefix = [256]
        if prefix:
            result += [dictionary[tuple(prefix)]]
        return result

    @classmethod
    def from_file(cls, path):
        """
        Makes an class instance from a file
        """
        from PIL import Image, ImageOps
        image_grayscale = ImageOps.grayscale(Image.open(path))
        pixels = image_grayscale.load()
        width, height = image_grayscale.size
        result = cls(height, width)
        for i in range(height):
            for j in range(width):
                result.setitem(i, j, pixels[j, i])
        return result

    @classmethod
    def from_list(cls, lst):
        """
        Builds an image from 2D list with values 0-255
        """
        if not isinstance(lst[0], list):
            raise ValueError("The argument must be a list of lists")
        answer = cls(len(lst), len(lst[0]))
        for i in range(len(lst)):
            if not isinstance(lst[i], list):
                raise ValueError("The argument must be a list of lists")
            if len(lst[i] != len(lst[0])):
                raise ValueError("The argument must be a list of lists with "
                                 "equal length")
            for j in range(len(lst[0])):
                answer.setitem(i, j, lst[i][j])
        return answer

    @classmethod
    def lzw_decompression(cls, lst: list):
        """
        Decompresses an image using lzw
        """
        dict_size = 257
        dictionary = dict((i, [i]) for i in range(dict_size))

        answer = []
        prefix = [lst.pop(0)]
        answer += prefix
        for element in lst:
            if element in dictionary:
                string = dictionary[element]
            elif element == dict_size:
                string = prefix + [prefix[0]]
            else:
                raise ValueError('Bad compressed')
            answer += string

            dictionary[dict_size] = prefix + [string[0]]
            dict_size += 1

            prefix = string
        result = [[]]
        for element in answer:
            if element == 256:
                result += [[]]
            else:
                result[-1] += [element]
        return cls.from_list(result[:-1])
