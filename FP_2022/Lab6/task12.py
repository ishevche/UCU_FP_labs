import unittest

from square_preceding import square_preceding


class TestSquare(unittest.TestCase):
    def test_square_preceding(self):
        lst = [1, 2, 3]
        square_preceding(lst)
        self.assertEqual(lst, [0, 1, 4])

        lst = []
        square_preceding(lst)
        self.assertEqual(lst, [])


if __name__ == '__main__':
    unittest.main()
