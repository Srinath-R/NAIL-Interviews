"""
Dispatcher Algorithms:
1. First Come First Serve -> High Costs
2. Shortest Seek Time First -> Starvation
3. SCAN / Elevator Algorithm -> OK but cost and wait time can be improved
4. LOOK(or Look-Ahead SCAN) -> Good
5. Destination Dispatch -> Ideal for huge no. of elevators and floors
"""
from abc import ABC, abstractmethod
from enum import Enum
from collections import defaultdict
from threading import Thread, Lock
import time

class ElevatorState(Enum):
    MOVING_UP = "MOVING UP"
    MOVING_DOWN = "MOVING DOWN"
    IDLE = "IDLE"
    MAINTENANCE = "MAINTENANCE"

class Request:
    def __init__(self, floor: int):
        self.floor = floor

class Dispatcher(ABC):
    @abstractmethod
    def dispatch_elevator(self, elevator):
        pass

class Elevator(Thread):
    def __init__(self, id: int, system):
        super().__init__()
        self.id = id
        self.system = system
        self.current_floor = 0
        self.state = ElevatorState.IDLE
        self.internal_requests = set()
        self.external_requests = defaultdict(list)
        self.lock = Lock()
        self.running = True
    
    def request_elevator(self, floor: int):
        if self.state == ElevatorState.IDLE and self.current_floor == floor:
            return
        with self.lock:
            self.external_requests[floor].append(Request(floor))
    
    def select_floor(self, floor: int):
        with self.lock:
            self.internal_requests.add(floor)
    
    def move(self):
        with self.lock:
            if self.state == ElevatorState.MAINTENANCE:
                print(f"The Elevator #{self.id} is in Maintenance!")
                return
            
            if not self.internal_requests and not self.external_requests:
                self.state = ElevatorState.IDLE
                return
            
            next_floor = self.system.dispatcher.dispatch_elevator(self)

            if next_floor is not None:
                # Simulate travel time
                time.sleep(abs(self.current_floor - next_floor))
                self.current_floor = next_floor
                
                if next_floor in self.internal_requests:
                    self.internal_requests.remove(next_floor)
                    print(f"Elevator #{self.id} has reached floor #{next_floor}. Please get down...")
                
                if next_floor in self.external_requests:
                    del self.external_requests[next_floor]
                    print(f"Ching!!! Elevator #{self.id} has come to floor #{next_floor}. Please enter...")
            else:
                self.state = ElevatorState.IDLE
    
    def run(self):
        while self.running or self.internal_requests or self.external_requests:
            self.move()
            # time.sleep(1)

    def stop(self):
        self.running = False

class ElevatorSystem:
    def __init__(self, num_elevators: int, total_floors: int, dispatcher: Dispatcher):
        self.num_elevators = num_elevators
        self.total_floors = total_floors
        self.dispatcher = dispatcher
        self.elevators = [Elevator(i, self) for i in range(num_elevators)]
        for elevator in self.elevators:
            elevator.start()

    def request_elevator(self, floor: int):
        """For calling an elevator from the lobby"""

        # Find all idle elevators
        idle_elevators = [e for e in self.elevators if e.state == ElevatorState.IDLE]
        
        if idle_elevators:
            # Assign the closest idle elevator to the request
            best_elevator = min(idle_elevators, key=lambda e: abs(e.current_floor - floor))
        else:
            # If no idle elevators, assign the closest elevator that is not in maintenance
            busy_elevators = [e for e in self.elevators if e.state != ElevatorState.MAINTENANCE]
            best_elevator = min(busy_elevators, key=lambda e: abs(e.current_floor - floor))
        
        best_elevator.request_elevator(floor)
    
    def select_floor(self, elevator_id: int, floor: int):
        """For selecting floor from inside the elevator"""
        elevator = self.elevators[elevator_id]
        elevator.select_floor(floor)
    
    def stop_system(self):
        for elevator in self.elevators:
            elevator.stop()
            elevator.join()

class LOOK(Dispatcher):
    def dispatch_elevator(self, elevator) -> int:
        target_floors = sorted(elevator.internal_requests | set(elevator.external_requests.keys()))

        if not target_floors:
            return None
        
        if elevator.state == ElevatorState.IDLE:
            if target_floors[0] > elevator.current_floor:
                elevator.state = ElevatorState.MOVING_UP
            elif target_floors[-1] < elevator.current_floor:
                elevator.state = ElevatorState.MOVING_DOWN
        
        if elevator.state == ElevatorState.MOVING_UP:
            next_floor = [f for f in target_floors if f >= elevator.current_floor]
        else:
            next_floor = [f for f in reversed(target_floors) if f <= elevator.current_floor]
        
        return next_floor[0] if next_floor else None

system = ElevatorSystem(2, 10, LOOK())
system.request_elevator(1)
system.request_elevator(3)
system.select_floor(0, 7)
system.select_floor(1, 5)
system.stop_system()