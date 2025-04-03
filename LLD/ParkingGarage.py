from typing import List, Dict
from datetime import datetime, timezone
from uuid import uuid4
from enum import Enum
from time import sleep

class Status(Enum):
    OCCUPIED = 1
    AVAILABLE = 0
    MAINTENANCE = -1

class Spot:
    def __init__(self, id: str, type: str):
        self.id = id
        self.type = type
        self.status = Status.AVAILABLE

class Reservation:
    def __init__(self, vehicle_registration: str, spot: Spot, start_time: datetime):
        self.id = str(uuid4())
        self.vehicle_registration = vehicle_registration
        self.spot = spot
        self.start_time = start_time
        self.end_time = None
        self.paid = False
        self.parking_charge = float(0)

    def make_payment(self, end_time: datetime, parking_charge: float):
        self.end_time = end_time
        self.parking_charge = parking_charge
        self.paid = True

class SpotManager:
    def __init__(self, spots: List[Spot]):
        self.spots = spots

    def find_available_spot(self, type: str) -> Spot:
        for spot in self.spots:
            if spot.status == Status.AVAILABLE and spot.type == type:
                spot.status = Status.OCCUPIED
                return spot
        raise ValueError(f"No available spots for type {type}")

    def release_spot(self, spot: Spot):
        spot.status = Status.AVAILABLE

class PaymentCalculator:
    def __init__(self, rate: Dict[str, float]):
        self.rate = rate

    def calculate_charge(self, spot_type: str, start_time: datetime, end_time: datetime) -> float:
        duration_hours = (end_time - start_time).total_seconds() / 3600
        return round(self.rate[spot_type] * duration_hours, 2)

class Garage:
    def __init__(self, id: int, rate: dict, zipcode: str, spots: List[Spot]):
        self.id = id
        self.zipcode = zipcode
        self.spot_manager = SpotManager(spots)
        self.payment_calculator = PaymentCalculator(rate)

    def allot_spot(self, type: str, vehicle_registration: str) -> Reservation:
        spot = self.spot_manager.find_available_spot(type)
        reservation = Reservation(vehicle_registration, spot, datetime.now(timezone.utc))
        print(f"Reservation {reservation.id} has been created for {vehicle_registration}. Spot assigned is {spot.id}.")
        return reservation

    def checkout(self, reservation: Reservation):
        end_time = datetime.now(timezone.utc)
        charges = self.payment_calculator.calculate_charge(
            reservation.spot.type, reservation.start_time, end_time
        )
        print(f"Your parking charge is {str(charges)}.")
        reservation.make_payment(end_time, charges)
        self.spot_manager.release_spot(reservation.spot)
        print("Thank you. Visit again.")

prices = {
    "Compact": 36000,
    "Regular": 72000,
    "Large": 108000
}

spots = []
com_spots, reg_spots, lar_spots = 3, 5, 2
for i in range(com_spots):
    spot = Spot("C" + str(i), 'Compact')
    spots.append(spot)
for i in range(reg_spots):
    spot = Spot("R" + str(i), 'Regular')
    spots.append(spot)
for i in range(lar_spots):
    spot = Spot("L" + str(i), 'Large')
    spots.append(spot)
garage = Garage(1, prices, "641035", spots)
reservation_01 = garage.allot_spot("Regular", "TN 37 BOSS")
reservation_02 = garage.allot_spot("Compact", "TN 66 MASS")
reservation_03 = garage.allot_spot("Large", "TN 07 THALA")
sleep(1)
garage.checkout(reservation_02)
garage.checkout(reservation_03)
garage.checkout(reservation_01)
