import math
from unittest import TestCase

from disc import Center, Disc

PRECISION = 2


class Tests(TestCase):
    def test_disc_class(self):
        # Disc have two main properties:
        # center of disc and the radius of disc.
        # A Disc objects convert to a printable string as:
        self.assertEqual(str(Disc(Center(1, 1), 3)),
                         "(x-1.00)**2 + (y-1.00)**2 = 9.00")
        self.assertEqual(str(Disc(Center(5, 5), 4)),
                         "(x-5.00)**2 + (y-5.00)**2 = 16.00")
        self.assertEqual(str(Disc(Center(0, 3), 1)),
                         "(x)**2 + (y-3.00)**2 = 1.00")
        self.assertEqual(str(Disc(Center(0, 0), 2)), "(x)**2 + (y)**2 = 4.00")
        self.assertEqual(str(Disc(Center(0, 1), 1)),
                         "(x)**2 + (y-1.00)**2 = 1.00")
        self.assertEqual(str(Disc(Center(1, 4), 1)),
                         "(x-1.00)**2 + (y-4.00)**2 = 1.00")
        # A Disc objects convert to a printable string as:
        self.assertEqual(str(Center(1, 4)), "Center is x=1, y=4")

        disc1 = Disc(Center(1, 1), 3)
        self.assertEqual(str(disc1), "(x-1.00)**2 + (y-1.00)**2 = 9.00")
        self.assertEqual(disc1.radius, 3)
        self.assertEqual(isinstance(disc1.radius, int), True)
        self.assertEqual(disc1.center, (1, 1))

        disc2 = Disc(Center(5, 5), 4)
        self.assertEqual(str(disc2), "(x-5.00)**2 + (y-5.00)**2 = 16.00")
        self.assertEqual(disc2.radius, 4)
        self.assertEqual(disc2.center, (5, 5))

        # Whether the discs are touching
        self.assertEqual(
            Disc(Center(0, 1), 1).is_touching(Disc(Center(0, 0), 2),
                                              precision=PRECISION), True)
        self.assertEqual(disc1.is_touching(disc2, precision=PRECISION), False)

        # inscribe_discs returns the two disks of the same radius
        # that inscribed in the given disc, are touching and
        # one coordinate coincides
        (disc5, disc6) = disc2.inscribe_discs()
        self.assertEqual(str(disc5), "(x-3.00)**2 + (y-5.00)**2 = 4.00")
        self.assertEqual(str(disc6), "(x-7.00)**2 + (y-5.00)**2 = 4.00")
        self.assertEqual(disc5.is_touching(disc6, precision=PRECISION), True)

        # We can transform disc
        disc2.transform_disc(2)
        self.assertEqual(str(disc2), "(x-5.00)**2 + (y-5.00)**2 = 36.00")
        disc2.transform_disc(-2)
        self.assertEqual(str(disc2), "(x-5.00)**2 + (y-5.00)**2 = 16.00")
        # Transformed disc is a new object
        disc = disc2.transformed_disc(2)
        self.assertEqual(isinstance(disc, Disc), True)
        self.assertEqual(str(disc2), "(x-5.00)**2 + (y-5.00)**2 = 16.00")
        self.assertEqual(str(disc), "(x-5.00)**2 + (y-5.00)**2 = 36.00")

        # We should be able to test disc for basic functionality
        self.assertEqual(Disc(Center(5, 5), 5), Disc(Center(5, 5), 5))
        self.assertNotEqual(Disc(Center(4, 4), 5), Disc(Center(1, 3), 3))
        self.assertNotEqual(Disc(Center(4, 4), 5), "don't crash here!")

        disc_set = set()
        self.assertNotIn(Disc(Center(1, 2), 3), disc_set)
        disc_set.add(Disc(Center(1, 2), 3))
        self.assertIn(Disc(Center(1, 2), 3), disc_set)
        disc_set.remove(Disc(Center(1, 2), 3))
        self.assertNotIn(Disc(Center(1, 2), 3), disc_set)

        discx = Disc.fromstring('2 3 5')
        self.assertEqual(str(discx), "(x-2.00)**2 + (y-3.00)**2 = 25.00")

        # If two discs are superimposed, the lens forms and 
        # can be calculated its parameters - four point:
        # two disc centers and two disk intersection points
        ((x4, y4), (x3, y3), (x2, y2), (x1, y1)) = disc1.lens_creation(disc2,
                                                                       precision=PRECISION)
        # (1, 1) (5, 5) (1.13, 4.00) (4.00, 1.13)
        self.assertEqual(math.isclose(x4, disc1.center[0]), True)
        self.assertEqual(math.isclose(y4, disc1.center[1]), True)
        self.assertEqual(math.isclose(x3, disc2.center[0]), True)
        self.assertTrue(math.isclose(y3, disc2.center[0]))
        self.assertTrue(math.isclose(x1, 4.00) and math.isclose(y1, 1.13))
        self.assertTrue(math.isclose(x2, 1.13) and math.isclose(y2, 4.00))

        disc3 = Disc(Center(0, 3), 1)
        disc4 = Disc(Center(0, 0), 2)
        (x, y) = disc3.lens_creation(disc4, precision=PRECISION)  # (0, 2)
        self.assertTrue(math.isclose(x, 0) and math.isclose(y, 2))
        (x, y) = disc5.lens_creation(disc6, precision=PRECISION)  # (5, 5))
        self.assertTrue(math.isclose(x, 5) and math.isclose(y, 5))

        # If the disks are coincident then the lens is not formed -
        # there are an infinite number of common points

        self.assertEqual(
            Disc(Center(2, 2), 3).lens_creation(Disc(Center(2, 2), 3),
                                                precision=PRECISION), math.inf)

        # The discs are separate and the lens is not formed
        self.assertIsNone(
            Disc(Center(1, 4), 1).lens_creation(Disc(Center(2, -1), 2),
                                                precision=PRECISION))
