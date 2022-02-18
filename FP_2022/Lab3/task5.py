import math


class Point:
    """
    Class represents Point
    """

    def __init__(self, x_coord, y_coord):
        """
        Initializes class attributes
        """
        self.x_coord = x_coord
        self.y_coord = y_coord

    def distance(self, other):
        """
        Calculates distance between two points
        """
        return math.sqrt((self.x_coord - other.x_coord) ** 2 +
                         (self.y_coord - other.y_coord) ** 2)


class Triangle:
    """
    Class represents triangle
    """

    def __init__(self, point1: Point, point2: Point, point3: Point):
        """
        Initializes class attributes
        """
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3

    def is_triangle(self):
        """
        Checks if points making a triangle
        """
        lengths = sorted([self.point1.distance(self.point2),
                          self.point2.distance(self.point3),
                          self.point3.distance(self.point1)])
        return lengths[0] + lengths[1] > lengths[2]

    def perimeter(self):
        """
        Calculates perimeter
        """
        return (self.point1.distance(self.point2) +
                self.point2.distance(self.point3) +
                self.point3.distance(self.point1))

    def area(self):
        """
        Calculates area of the triangle
        """
        side1 = self.point1.distance(self.point2)
        side2 = self.point2.distance(self.point3)
        side3 = self.point3.distance(self.point1)
        semi_perimeter = 0.5 * (side1 + side2 + side3)
        return math.sqrt(semi_perimeter *
                         (semi_perimeter - side1) *
                         (semi_perimeter - side2) *
                         (semi_perimeter - side3))
