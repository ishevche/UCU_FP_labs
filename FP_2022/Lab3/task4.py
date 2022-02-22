"""
buildings.py
"""
import task3 as classroom


class AcademicBuilding:
    """
    Class represents academic building
    """

    def __init__(self, address, classrooms):
        """
        Initializes class attributes
        """
        self.address = address
        self.classrooms = classrooms

    def total_equipment(self):
        """
        Returns the total equipment in the building
        >>> classroom_016 = classroom.Classroom('016', 80, ['PC', 'projector', \
        'mic'])
        >>> classroom_007 = classroom.Classroom('007', 12, ['TV'])
        >>> classroom_008 = classroom.Classroom('008', 25, ['PC', 'projector'])
        >>> classrooms = [classroom_016, classroom_007, classroom_008]
        >>> building = AcademicBuilding('Kozelnytska st. 2a', classrooms)
        >>> building.total_equipment()
        [('PC', 2), ('projector', 2), ('mic', 1), ('TV', 1)]
        """
        equipment = {}
        for classroom_object in self.classrooms:
            classroom_object: classroom.Classroom
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
