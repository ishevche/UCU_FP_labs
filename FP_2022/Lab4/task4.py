"""
points.py
"""
import math


class Point:
    """
    Represents a point on coordinate plane
    """

    def __init__(self, x_coord, y_coord):
        """
        Initializes classes references
        """
        self.x = x_coord
        self.y = y_coord

    def __str__(self):
        """
        Pretty representation
        """
        return f'Point in two-dimensional space with coordinates ' \
               f'({self.x}, {self.y})'

    def __repr__(self):
        """
        Pretty representation
        """
        return f'Point(x={self.x}, y={self.y})'

    def __eq__(self, other):
        """
        Compares two point objects
        >>> Point(3, 4) != Point(2, 3)
        True
        >>> Point(5, 4) == Point3D(5, 4, 0)
        True
        >>> Point(5, 4) != Point3D(5, 4, 1)
        True
        """
        if isinstance(other, Point3D):
            return other.__eq__(self)
        elif not isinstance(other, Point):
            return False
        return (self.x == other.x and
                self.y == other.y)

    def vector_length(self):
        """
        Returns norm of the point
        >>> Point(3, 4).vector_length()
        5.0
        >>> Point(6, -12).vector_length()
        13.42
        """
        return round(math.sqrt(self.x ** 2 + self.y ** 2), 2)


class Point3D(Point):
    """
    Represents a point on coordinate plane
    """

    def __init__(self, x_coord, y_coord, z_coord=0):
        """
        Initializes classes references
        """
        super().__init__(x_coord, y_coord)
        self.z = z_coord

    def __str__(self):
        """
        Pretty representation
        """
        return f'Point in three-dimensional space with coordinates ' \
               f'({self.x}, {self.y}, {self.z})'

    def __repr__(self):
        """
        Pretty representation
        """
        return f'Point(x={self.x}, y={self.y}, z={self.z})'

    def __eq__(self, other):
        """
        Compares two point objects
        >>> Point3D(8, 7, 0) == Point3D(8, 7)
        True
        >>> Point3D(5, 4, 0) == Point(5, 4)
        True
        >>> Point3D(5, 4, 1) != Point(5, 4)
        True
        """
        if not isinstance(other, Point3D):
            if isinstance(other, Point):
                return (self.x == other.x and
                        self.y == other.y and
                        self.z == 0)
            return False
        return (self.x == other.x and
                self.y == other.y and
                self.z == other.z)

    def vector_length(self):
        """
        Returns norm of the point
        >>> Point3D(-6, -12, 0).vector_length()
        13.42
        >>> Point3D(-13, 14, -15).vector_length()
        24.29
        """
        return round(math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2), 2)
