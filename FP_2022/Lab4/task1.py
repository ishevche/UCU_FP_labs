"""
building.py
"""


class Building:
    """
    Represents a constructed building
    """

    def __init__(self, address):
        """
        Initializes classes references
        """
        self.address = address


class House(Building):
    """
    Represents a constructed house with flats
    """

    def __init__(self, address, flats):
        """
        Initializes classes references
        """
        self.flats = flats
        super().__init__(address)


class AcademicBuilding(Building):
    """
    Class represents academic building
    """

    def __init__(self, address, classrooms):
        """
        Initializes class attributes
        """
        super().__init__(address)
        self.classrooms = classrooms

    def total_equipment(self):
        """
        Returns the total equipment in the building
        >>> classroom_016 = Classroom('016', 80, ['PC', 'projector', \
        'mic'])
        >>> classroom_007 = Classroom('007', 12, ['TV'])
        >>> classroom_008 = Classroom('008', 25, ['PC', 'projector'])
        >>> classrooms = [classroom_016, classroom_007, classroom_008]
        >>> building = AcademicBuilding('Kozelnytska st. 2a', classrooms)
        >>> building.total_equipment()
        [('PC', 2), ('projector', 2), ('mic', 1), ('TV', 1)]
        """
        equipment = {}
        for classroom_object in self.classrooms:
            for equipment_peace in classroom_object.equipment:
                if equipment_peace in equipment:
                    equipment[equipment_peace] += 1
                else:
                    equipment[equipment_peace] = 1
        return list(equipment.items())

    def __str__(self):
        """
        Pretty representation
        """
        answer_str = f'{self.address}\n'
        for classroom_object in self.classrooms:
            answer_str += f'{str(classroom_object)}\n'
        return answer_str[:-1]


class Classroom:
    """
    Class represents Classroom
    """

    def __init__(self, number, capacity, equipment):
        """
        Initializes class attributes
        """
        self.number = number
        self.capacity = capacity
        self.equipment = equipment

    def __str__(self):
        """
        Pretty representation
        >>> classroom_016 = Classroom('016', 80, ['PC', 'projector', 'mic'])
        >>> print(classroom_016)
        Classroom 016 has a capacity of 80 persons and has the following \
equipment: PC, projector, mic.
        """
        return f"Classroom {self.number} has a capacity of {self.capacity} " \
               f"persons and has the following equipment: " \
               f"{', '.join(self.equipment)}."

    def is_larger(self, other):
        """
        Compares capacity of classrooms
        """
        return self.capacity > other.capacity

    def equipment_differences(self, other):
        """
        Returns equipment present in self and no t present in other
        """
        answer_list = []
        for staff in self.equipment:
            if staff not in other.equipment:
                answer_list += [staff]
        return answer_list

    def __repr__(self):
        """
        Pretty representation
        """
        return f"Classroom({repr(self.number)}, " \
               f'{repr(self.capacity)}, ' \
               f'{repr(self.equipment)})'
