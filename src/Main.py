"""
Main.py
DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
This file runs the simulation.
"""

from Graph import *
from MinHeap import *
from VehicleHashTable import *
from Menu import main_menu

def main():
    vehicle_hash_table = VehicleHashTable(50)
    vehicle_graph = Graph()
    main_menu(vehicle_graph, vehicle_hash_table)




if __name__ == "__main__":
    main()