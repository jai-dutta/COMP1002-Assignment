"""
test_vehiclehashtable.py

This file contains the tests for the VehicleHashTable class.

DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
"""

import pytest

from VehicleHashTable import *

@pytest.fixture
def vehicle_hashtable():
    vht = VehicleHashTable(15)
    vht.put(Vehicle("A", 100))
    vht.put(Vehicle("B", 100))
    vht.put(Vehicle("C", 100))

    return vht

def test_put(vehicle_hashtable):
    d_veh = Vehicle("D", 100)
    assert vehicle_hashtable.get_count() == 3
    vehicle_hashtable.put(d_veh)
    assert vehicle_hashtable.get_count() == 4
    assert vehicle_hashtable.get("D") == d_veh

def test_put_duplicate(vehicle_hashtable):
    with pytest.raises(DuplicateVehicleFound):
        vehicle_hashtable.put(Vehicle("A", 100))

def test_get(vehicle_hashtable):
    assert vehicle_hashtable.get("A").get_ID() == "A"
    assert vehicle_hashtable.get("B").get_ID() == "B"
    assert vehicle_hashtable.get("C").get_ID() == "C"

    with pytest.raises(VehicleNotFoundError):
        vehicle_hashtable.get("D")

def test_remove(vehicle_hashtable):
    assert vehicle_hashtable.get_count() == 3
    vehicle_hashtable.remove("A")
    assert vehicle_hashtable.get_count() == 2
    with pytest.raises(VehicleNotFoundError):
        vehicle_hashtable.get("A")

def test_get_lf(vehicle_hashtable):
    # Although table size is set to 15, the next prime will be 17.
    # The load factor should be 3/17 = 0.176, rounded to 0.18 (two decimas)
    assert vehicle_hashtable.get_lf() == 0.18

def test_has_key(vehicle_hashtable):
    assert vehicle_hashtable.has_key("A") == True
    assert vehicle_hashtable.has_key("D") == False

def test_export_to_array(vehicle_hashtable):
    arr = vehicle_hashtable.export_to_array()
    assert len(arr) == 3
    assert arr[0].get_ID() == "A"
    assert arr[1].get_ID() == "B"
    assert arr[2].get_ID() == "C"


