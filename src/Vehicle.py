"""
Vehicle.py
DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
This file contains the Vehicle class, which is used to represent a vehicle in the simulation.
"""


class Vehicle:
    def __init__(self, ID: str, battery_level: int):
        self.ID = ID
        self.location = None
        self.destination = None
        self.distance_to_destination = 0

        if battery_level > 100 or battery_level < 0:
            raise InvalidBatteryException("Invalid battery percentage, must be between 0-100.")
        self.battery_level = battery_level

    def __str__(self):
        return f"ID: {self.ID}"

    def get_location(self):
        return self.location

    def get_destination(self):
        return self.destination

    def get_distance_to_destination(self):
        return self.distance_to_destination

    def get_battery_level(self):
        return self.battery_level

    def set_location(self, location):
        self.location = location

    def set_destination(self, destination):
        self.destination = destination

    def set_distance_to_destination(self, distance: int):
        if distance < 0:
            raise ValueError("Distance to destination must be positive")
        self.distance_to_destination = distance

    def set_battery_level(self, battery_level: int):
        if battery_level > 100 or battery_level < 0:
            raise InvalidBatteryException("Invalid battery percentage, must be between 0-100.")
        self.battery_level = battery_level


class InvalidBatteryException(Exception):
    pass
