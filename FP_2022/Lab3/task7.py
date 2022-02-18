import random


class Item:
    """
    Represents a good that can be bought
    """

    def __init__(self, name, price):
        """
        Initializes class attributes
        """
        self.name: str = name
        self.price: float = price

    def __str__(self):
        """
        Pretty representation
        """
        return f"An item of {self.name} for {self.price} UAH"


class Vehicle:
    """
    Represents vehicle in the logistic system
    """

    def __init__(self, vehicle_num):
        """
        Initializes class attributes
        """
        self.vehicleNo: int = vehicle_num
        self.isAvailable: bool = True


class Location:
    """
    Represents a location like a final destination
    """

    def __init__(self, city, post_office):
        """
        Initializes class attributes
        """
        self.city: str = city
        self.postoffice: int = post_office


class Order:
    """
    Represents info about order and user
    """

    def __init__(self, user_name, city, postoffice, items):
        """
        Initializes class attributes
        """
        self.orderId: int = random.randint(1, 1000000000)
        self.user_name: str = user_name
        self.location: Location = Location(city, postoffice)
        self.items: list = items
        self.vehicle: Vehicle = None
        print(f'Your order number is {self.orderId}.')

    def calculateAmount(self):
        total_price = 0.0
        for item in self.items:
            total_price += item.price
        return total_price

    def __str__(self):
        """
        Pretty representation
        """
        return f"Your order #{self.orderId} is sent to {self.location.city}. " \
               f"Total price: {self.calculateAmount()} UAH."

    def assignVehicle(self, vehicle: Vehicle):
        """
        Assigns vehicle for delivering the order
        """
        self.vehicle = vehicle
        vehicle.isAvailable = False


class LogisticSystem:
    """
    Represents logistic system
    """

    def __init__(self, vehicles: list):
        """
        Initializes class attributes
        """
        self.orders = []
        self.vehicles = vehicles

    def placeOrder(self, order: Order):
        """
        Places order for execution
        """
        for vehicle in self.vehicles:
            if vehicle.isAvailable:
                order.assignVehicle(vehicle)
                self.orders.append(order)
                return
        print('There is no available vehicle to deliver an order.')

    def trackOrder(self, orderId: int):
        """
        Displays info about order
        """
        for order in self.orders:
            if order.orderId == orderId:
                print(order)
                return
        print('No such order.')

