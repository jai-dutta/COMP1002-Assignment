"""
test_vehicle.py

This file contains the tests for the Vehicle class.

DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
"""

import pytest

from Vehicle import *
from Graph import GraphVertex

@pytest.fixture
def vehicle():
    v = Vehicle("A", 70)
    v.set_location(GraphVertex("A"))
    v.set_destination(GraphVertex("B"))
    v.set_distance_to_destination(100)
    return v


def test_get_location(vehicle):
    assert vehicle.get_location().get_label() == "A"

def test_get_destination(vehicle):
    assert vehicle.get_destination().get_label() == "B"

def test_get_distance_to_destination(vehicle):
    assert vehicle.get_distance_to_destination() == 100

def test_get_battery_level(vehicle):
    assert vehicle.get_battery_level() == 70



