"""Implementation of the main simulation class."""
import random

from arrays import Array
from llistqueue import Queue
from people import TicketAgent, Passenger


class TicketCounterSimulation:
    """Represents a simulation"""

    def __init__(self, num_agents, num_minutes, between_time, service_time):
        """Create a simulation object."""
        # Parameters supplied by the user.
        self._arrive_prob = 1.0 / between_time
        self._service_time = service_time
        self._num_minutes = num_minutes

        # Simulation components.
        self._passenger_queue = Queue()
        self._agents = Array(num_agents)
        for agent_idx in range(num_agents):
            self._agents[agent_idx] = TicketAgent(agent_idx + 1)

        # Computed during the simulation.
        self._total_wait_time = 0
        self._num_passengers = 0

    def run(self, verbose=False):
        """Run the simulation using the parameters supplied earlier."""
        for cur_time in range(self._num_minutes + 1):
            self._handle_arrival(cur_time, verbose=verbose)
            self._handle_begin_service(cur_time, verbose=verbose)
            self._handle_end_service(cur_time, verbose=verbose)

    def get_results(self, verbose=True):
        """Print the simulation results."""
        num_served = self._num_passengers - len(self._passenger_queue)
        avg_wait = float(self._total_wait_time) / num_served
        num_left = len(self._passenger_queue)
        if verbose:
            print("")
            print("Number of passengers served = ", num_served)
            print("Number of passengers remaining in line = %d" % num_left)
            print("The average wait time was %4.2f minutes." % avg_wait)
        return round(avg_wait, 2), num_served, num_left

    def _handle_arrival(self, cur_time, verbose=False):
        """Handles the arrival of a passenger"""
        if random.random() > self._arrive_prob:
            return
        self._num_passengers += 1
        self._passenger_queue.enqueue(
            Passenger(self._num_passengers,
                      cur_time)
        )
        if verbose:
            print(f"Time {cur_time:4}: "
                  f"Passenger {self._num_passengers} arrived.")

    def _handle_begin_service(self, cur_time, verbose=False):
        """Handles start of the service of a passenger"""
        available_agents = list(map(lambda x: x.is_free(), self._agents))
        while not self._passenger_queue.isEmpty() and any(available_agents):
            available_agent_idx = available_agents.index(True)
            available_agents[available_agent_idx] = False

            passenger = self._passenger_queue.dequeue()
            agent: TicketAgent = self._agents[available_agent_idx]
            agent.start_service(passenger, cur_time + self._service_time)

            self._total_wait_time += cur_time - passenger.time_arrived()

            if verbose:
                print(f"Time {cur_time:4}: "
                      f"Agent {agent.id_num()} started serving passenger "
                      f"{passenger.id_num()}.")

    def _handle_end_service(self, cur_time, verbose=False):
        """Handles end of the service of a passenger"""
        for agent in self._agents:
            agent: TicketAgent
            if agent.is_finished(cur_time):
                passenger = agent.stop_service()
                if verbose:
                    print(f"Time {cur_time:4}: "
                          f"Agent {agent.id_num()} stopped serving passenger "
                          f"{passenger.id_num()}.")


if __name__ == '__main__':
    sims = [(2, 100, 2, 3),
            (2, 500, 2, 3),
            (2, 1000, 2, 3),
            (2, 5000, 2, 3),
            (2, 10000, 2, 3),
            (2, 100, 2, 4),
            (2, 500, 2, 4),
            (2, 1000, 2, 4),
            (2, 5000, 2, 4),
            (2, 10000, 2, 4),
            (3, 100, 2, 4),
            (3, 500, 2, 4),
            (3, 1000, 2, 4),
            (3, 5000, 2, 4),
            (3, 10000, 2, 4)]
    results = []
    for sim_asset in sims:
        random.seed(4500)
        sim = TicketCounterSimulation(*sim_asset)
        sim.run()
        results += [sim.get_results(verbose=False)]
    print('\n'.join(map(str, results)))
