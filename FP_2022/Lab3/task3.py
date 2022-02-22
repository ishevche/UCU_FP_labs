"""
classroom.py
"""


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
