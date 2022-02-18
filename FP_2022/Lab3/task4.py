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
        """
        equipment = {}
        for classroom in self.classrooms:
            for equipment_peace in classroom.equipment:
                if equipment_peace in equipment:
                    equipment[equipment_peace] += 1
                else:
                    equipment[equipment_peace] = 1
        return equipment.items()

    def __str__(self):
        """
        Pretty representation
        """
        answer_str = f'{self.address}\n'
        for classroom in self.classrooms:
            answer_str += f'{str(classroom)}\n'
        return answer_str[:-1]
