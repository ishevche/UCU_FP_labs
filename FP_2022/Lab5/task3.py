"""
vehicle.py
"""


class Vehicle:
    """
    Represents vehicle
    """

    def __init__(self, brand, model, vehicle_type, volume, consumption):
        self.brand = brand
        self.model = model
        self.type = vehicle_type
        self.volume = volume
        self.consumption = consumption
        self.fuel_level = 0

    def fuel_up(self, amount: float):
        """
        Fuels up a gas tank
        """
        self.fuel_level = min(self.fuel_level + amount, self.volume)
        return "Gas tank is filled."

    def get_fuel_level(self):
        """
        Returns fuel level
        """
        return self.fuel_level

    def drive(self, amount: float):
        """
        Drives amount kilometers
        """
        consumption = amount / 100 * self.consumption
        if consumption > self.fuel_level:
            return "Not enough fuel level in a gas tank."
        else:
            self.fuel_level -= consumption
            return f"The {self.brand} {self.model} is now driving."

    def __str__(self):
        return f"Vehicle {self.brand} {self.model} is a {self.type}. " \
               f"It has a gas tank size of {self.volume}."


class Battery:
    """
    Represents a battery of electric vehicle
    """

    def __init__(self):
        self.charge_level = 0

    def charge(self):
        """
        Charges a battery
        """
        self.charge_level = 100

    def drive(self):
        """
        Consumption of charge
        """
        self.charge_level = 0

    def __str__(self):
        return f"Battery has size of 85, " \
               f"it is charged up to {self.charge_level}%"


class ElectricVehicle(Vehicle):
    """
    Represents an electric vehicle
    """

    def __init__(self, brand, model, vehicle_type):
        super().__init__(brand, model, vehicle_type, 0, 0)
        self.battery = Battery()

    def charge(self):
        """
        Charges an vehicle
        """
        self.battery.charge()
        return "The vehicle is fully charged."

    def get_charge_level(self):
        """
        Returns current fuel level
        """
        return self.battery.charge_level

    def drive(self):
        """
        Drives electric vehicle
        """
        self.battery.drive()
        return f"The {self.brand} {self.model} is now driving."

    def get_battery_info(self):
        """
        Returns info about battery
        """
        return str(self.battery)

    def __str__(self):
        return f"Vehicle {self.brand} {self.model} is a {self.type}."


def test_vehicle():
    """
    Test function
    """
    print("Testing Vehicle classes...")
    # A basic Vehicle has a brand, model, type, volume of gas_tank_size
    # fuel_level that by default equals 0 and fuel_consumption
    # that by default equals 6. It can drive and be fueled up
    vehicle = Vehicle("Subaru", "Forester", "Crossover", 16, 7)
    assert (type(vehicle) == Vehicle)
    assert (isinstance(vehicle, Vehicle))
    assert (str(vehicle) ==
            "Vehicle Subaru Forester is a Crossover. "
            "It has a gas tank size of 16.")

    # change some attributes
    assert (vehicle.fuel_up(12) == "Gas tank is filled.")
    assert (vehicle.get_fuel_level() == 12)
    # When vehicle drives, it uses the fuel level
    # Vehicle uses fuel in amount of
    # fuel_consumption * distance to drive / 100
    assert (vehicle.drive(100) == "The Subaru Forester is now driving.")
    # the vehicle travelled 100 km and the fuel level reduced
    # from 12 to 5
    assert (vehicle.get_fuel_level() == 5)
    assert (vehicle.drive(100) == "Not enough fuel level in a gas tank.")

    # ElectricVehicle is a Vehicle that doesn't need a gas_tank_size
    # and doesn't have a fuel_consumption.
    # You can charge and drive it.
    electric_vehicle = ElectricVehicle('Tesla', 'Model 3', 'Sedan')
    assert (type(electric_vehicle) == ElectricVehicle)
    assert (isinstance(electric_vehicle, ElectricVehicle))
    assert (isinstance(electric_vehicle, Vehicle))
    assert (str(electric_vehicle) == "Vehicle Tesla Model 3 is a Sedan.")

    assert (electric_vehicle.get_fuel_level() == 0)
    assert (electric_vehicle.charge() == "The vehicle is fully charged.")
    assert (electric_vehicle.get_charge_level() == 100)
    assert (electric_vehicle.drive() == "The Tesla Model 3 is now driving.")
    assert (electric_vehicle.get_charge_level() == 0)

    # the attribute battery has to belong to Battery class
    # the Battery has a size, that by default equals 85
    # and charge level that by default equals 0
    assert (type(electric_vehicle.battery) == Battery)
    assert (isinstance(electric_vehicle.battery, Battery))
    assert (electric_vehicle.get_battery_info() ==
            "Battery has size of 85, it is charged up to 0%")

    print("Done!")


if __name__ == '__main__':
    test_vehicle()
