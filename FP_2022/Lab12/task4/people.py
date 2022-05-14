"""Support classes for simulation"""


class Passenger:
    """Used to store and manage information related to an airline passenger."""

    def __init__(self, id_num, arrival_time):
        """Creates a passenger object."""
        self._id_num = id_num
        self._arrival_time = arrival_time

    def id_num(self):
        """Gets the passenger's id number."""
        return self._id_num

    def time_arrived(self):
        """Gets the passenger's arrival time."""
        return self._arrival_time


class TicketAgent:
    """
    Used to store and manage information related to an airline ticket agent.
    """

    def __init__(self, id_num):
        """Creates a ticket agent object."""
        self._id_num = id_num
        self._passenger = None
        self._stop_time = -1

    def id_num(self):
        """Gets the ticket agent's id number."""
        return self._id_num

    def is_free(self):
        """Determines if the ticket agent is free to assist a passenger."""
        return self._passenger is None

    def is_finished(self, cur_time):
        """Determines if the ticket agent has finished helping the passenger."""
        return self._passenger is not None and self._stop_time == cur_time

    def start_service(self, passenger, stop_time):
        """Indicates the ticket agent has begun assisting a passenger."""
        self._passenger = passenger
        self._stop_time = stop_time

    def stop_service(self):
        """Indicates the ticket agent has finished helping the passenger."""
        the_passenger = self._passenger
        self._passenger = None
        return the_passenger
