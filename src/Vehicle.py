"""
Vehicle.py

This file contains the Vehicle class, which is used to represent a vehicle in the simulation.

DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
"""

from Graph import GraphVertex

class Vehicle:
    """
    Class used to represent a vehicle in the simulation.
    Attributes:
        ID: The ID of the vehicle.
        battery_level: The battery level of the vehicle.
        location: The location of the vehicle.
        destination: The destination of the vehicle.
        distance_to_destination: The distance to the destination of the vehicle.
    """
    def __init__(self, ID: str, battery_level: int):
        self.ID = ID
        self.location = None
        self.destination = None
        self.distance_to_destination = 0

        if battery_level > 100 or battery_level < 0:
            raise InvalidBatteryException("Invalid battery percentage, must be between 0-100.")
        self.battery_level = battery_level

    def __str__(self) -> str:
        return f"ID: {self.ID}"

    def get_location(self) -> GraphVertex:
        return self.location

    def get_destination(self):
        return self.destination

    def get_distance_to_destination(self):
        return self.distance_to_destination

    def get_battery_level(self):
        return self.battery_level

    def set_location(self, location: GraphVertex):
        if not isinstance(location, GraphVertex):
            raise ValueError("Location must be a GraphVertex")

        self.location = location

    def set_destination(self, destination: GraphVertex):
        if not isinstance(destination, GraphVertex):
            raise ValueError("Destination must be a GraphVertex")
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
    """
    Exception raised for invalid battery levels.
    """
    pass
