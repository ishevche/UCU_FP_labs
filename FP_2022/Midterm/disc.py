import math


class Center:
    """
    Represents an center of the disc (a point on a plane)
    """

    def __init__(self, x_cord: float, y_cord: float):
        self.x_cord = x_cord
        self.y_cord = y_cord

    def __str__(self):
        return f"Center is x={round(self.x_cord)}, y={round(self.y_cord)}"


class Disc:
    """
    Represents a disc on a plane
    """

    def __init__(self, center: Center, radius: float):
        self.center = center.x_cord, center.y_cord
        self.radius = radius

    def is_touching(self, other, precision=2):
        """
        Checks if circle touches other circle
        """
        distance = math.sqrt((self.center[0] - other.center[0]) ** 2 +
                             (self.center[1] - other.center[1]) ** 2)
        distance = round(distance, precision)
        return (distance == self.radius + other.radius or
                distance == math.fabs(self.radius - other.radius))

    def inscribe_discs(self):
        """
        Inscribes two identical discs, and returns them
        """
        radius = self.radius / 2
        return (Disc(Center(self.center[0] - radius, self.center[1]), radius),
                Disc(Center(self.center[0] + radius, self.center[1]), radius))

    def transform_disc(self, value):
        """
        Transforms current disc, increasing radius by value
        """
        self.radius += value

    def transformed_disc(self, value):
        """
        Returns transformed disc
        """
        return Disc(Center(*self.center), self.radius + value)

    @staticmethod
    def fromstring(string):
        """
        Forms an object from string
        """
        x_cord, y_cord, radius = map(int, string.split(' '))
        return Disc(Center(x_cord, y_cord), radius)

    def lens_creation(self, other, precision=2):
        """
        Checks if discs superimposed and returns points
        """
        if self.__eq__(other):
            return math.inf
        if self.is_touching(other):
            x_cord = (other.radius * self.center[0] +
                      self.radius * other.center[0]) / \
                     (self.radius + other.radius)
            y_cord = (other.radius * self.center[1] +
                      self.radius * other.center[1]) / \
                     (self.radius + other.radius)
            return round(x_cord, precision), round(y_cord, precision)
        distance = math.sqrt((self.center[0] - other.center[0]) ** 2 +
                             (self.center[1] - other.center[1]) ** 2)
        if (distance > self.radius + other.radius or
                distance < math.fabs(self.radius - other.radius)):
            return
        first_leg = (self.radius ** 2 - other.radius ** 2 + distance ** 2) / \
                    (2 * distance)
        height = math.sqrt(self.radius ** 2 - first_leg ** 2)
        x_cord = (self.center[0] +
                  first_leg * (other.center[0] - self.center[0]) / distance)
        y_cord = (self.center[1] +
                  first_leg * (other.center[1] - self.center[1]) / distance)
        x1_cord = round(x_cord - height * (other.center[1] -
                                           self.center[1]) / distance,
                        precision)
        y1_cord = round(y_cord + height * (other.center[0] -
                                           self.center[0]) / distance,
                        precision)
        x2_cord = round(x_cord + height * (other.center[1] -
                                           self.center[1]) / distance,
                        precision)
        y2_cord = round(y_cord - height * (other.center[0] -
                                           self.center[0]) / distance,
                        precision)
        return (self.center, other.center,
                (x1_cord, y1_cord), (x2_cord, y2_cord))

    def __str__(self):
        first_arch = "x" + (f"-{float(self.center[0]):.2f}"
                            if self.center[0] else '')
        second_arch = "y" + (f"-{float(self.center[1]):.2f}"
                             if self.center[1] else '')
        return f'({first_arch})**2 + ' \
               f'({second_arch})**2 = ' \
               f'{float(self.radius ** 2):.2f}'

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash((self.center, self.radius))
