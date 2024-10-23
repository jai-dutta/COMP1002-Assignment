"""Menu.py

This file contains the menu for the simulation.

DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
"""

import os

from Graph import PathNotFound, VertexExistsError, EdgeExistsError, VertexNotFoundError, EdgeToSameVertex
from Sorting import *
from Vehicle import *
from VehicleHashTable import *

# Define ANSI escape codes for colors and formatting
red = "\033[0;31m"
green = "\033[0;32m"
bold = "\033[1m"
negative = "\033[7m"
end = "\033[0m"

"""
Dictionary of menu options for the simulation.
Key: Integer input
Value: String of the menu option
"""
menu_options = {
    1: "Add a new vehicle",
    2: "Remove a vehicle",
    3: "Update a vehicle",
    4: "Display all vehicles",
    5: "Find nearest vehicle",
    6: "Find highest battery level",
    7: "Add a location",
    8: "Add a road",
    9: "Check path existence",
    10: "Exit"
}


def print_menu(options: dict):
    """Prints the menu.

    Args:
        options: Dictionary containing menu options.
                 Keys: Integer representing the option number.
                 Values: String describing the menu option.

    Returns:
        None

    Note:
        ASCII Art generated from https://patorjk.com/software/taag :)
    """
    print("-" * 50)
    print(f"""
     █████╗ ██╗   ██╗███╗   ███╗███████╗    
    ██╔══██╗██║   ██║████╗ ████║██╔════╝    
    ███████║██║   ██║██╔████╔██║███████╗    
    ██╔══██║╚██╗ ██╔╝██║╚██╔╝██║╚════██║    
    ██║  ██║ ╚████╔╝ ██║ ╚═╝ ██║███████║    
    ╚═╝  ╚═╝  ╚═══╝  ╚═╝     ╚═╝╚══════╝    
    ███╗   ███╗███████╗███╗   ██╗██╗   ██╗  
    ████╗ ████║██╔════╝████╗  ██║██║   ██║  
    ██╔████╔██║█████╗  ██╔██╗ ██║██║   ██║  
    ██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║   ██║  
    ██║ ╚═╝ ██║███████╗██║ ╚████║╚██████╔╝  
    ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝""")
    print("-" * 50)
    for key, value in menu_options.items():
        print(f"\t{key}. {value}")
    print("-" * 50)


def get_choice(options: dict):
    """Grabs and validates the user's choice from the menu options.

    Args:
        options: Dictionary containing menu options.

    Returns:
        int: The user's choice.
    """
    while True:
        try:
            choice = int(input("Please enter option: "))
            if choice not in menu_options:
                print(f"{red}{bold}Invalid input. Please enter a number between 1 and {len(menu_options)}.{end}")
            else:
                return choice
        except ValueError:
            print(f"{red}{bold}Invalid input. Please enter a number.{end}")


def clear_screen():
    """Clears the screen."""
    os.system("cls" if os.name == "nt" else "clear")


def main_menu(graph, vehicle_hash_table):
    """Main menu for the simulation.

    Args:
        graph: Graph of the simulation.
        vehicle_hash_table: Hash table of the vehicles in the simulation.
    """
    # Initialize running varible
    running = True

    # Main menu loop
    while running:
        # Export vehciles from hash table to array each time the loop runs (for printing and sorting)
        vehicles = vehicle_hash_table.export_to_array()

        clear_screen()

        print_menu(menu_options)

        # Print locations
        print("Locations: ")
        print()
        display_graph(graph)
        print("-" * 50)

        # Print vehicles
        print("\nVehicles: ")
        print()
        _print_vehicle_from_arr(vehicles, False)
        print("-" * 50)

        # Get user choice
        choice = get_choice(menu_options)

        # Match user choice to menu option
        match choice:
            case 1:
                add_vehicle(vehicle_hash_table)

            case 2:
                remove_vehicle(vehicle_hash_table)

            case 3:
                update_vehicle(graph, vehicle_hash_table)

            case 4:
                display_vehicles(vehicle_hash_table)

            case 5:
                sorted_vehicles = sort_by_distance(vehicles)
                if len(vehicles) > 0:
                    vehicle = sorted_vehicles[0]
                    print(
                        f"{vehicle} | Battery Level: {vehicle.get_battery_level()} | Location: {vehicle.get_location()} | Destination: {vehicle.get_destination()} | Distance to Destination: {vehicle.get_distance_to_destination()}")
                    input("Press Enter to continue...")

            case 6:
                sorted_vehicles = sort_by_battery(vehicles)
                if len(vehicles) > 0:
                    vehicle = sorted_vehicles[0]
                    print(f"{vehicle} | Battery Level: {vehicle.get_battery_level()} | Location: {vehicle.get_location()} | Destination: {vehicle.get_destination()} | Distance to Destination: {vehicle.get_distance_to_destination()}")
                    input("Press Enter to continue...")

            case 7:
                add_location(graph)

            case 8:
                add_road(graph)

            case 9:
                check_path(graph)

            case 10:
                print("Thank you for using the Autonomous Vehicle Management System. Goodbye!")
                running = False

def add_vehicle(vehicle_hash_table):
    """Adds a vehicle to the hash table.

    Args:
        vehicle_hash_table: Hash table of the vehicles in the simulation.
    """
    vehicle_id = input("Enter vehicle ID: ")
    try:
        battery_level = int(input("Enter battery level (0-100): "))
    except ValueError:
        print(f"{red}{bold}Please enter a valid input.{end}")
        input("Press Enter to continue...")
        return

    try:
        vehicle = Vehicle(vehicle_id, battery_level)

    except InvalidBatteryException as e:
        print(f"{red}{bold}Error: {e}{end}")
        input("Press Enter to continue...")
        return

    try:
        vehicle_hash_table.put(vehicle_id, vehicle)

    except DuplicateVehicleFound as e:
        print(f"{red}{bold}Error: {e}{end}")
        input("Press Enter to continue...")
        return

    print(f"{green}{bold}Vehicle added successfully{end}")
    input("Press Enter to continue...")

def remove_vehicle(vehicle_hash_table):
    """Removes a vehicle from the hash table.

    Args:
        vehicle_hash_table: Hash table of the vehicles in the simulation.
    """
    vehicle_id = input("Enter vehicle ID: ")

    try:
        vehicle_hash_table.remove(vehicle_id)
        print(f"{green}{bold}Vehicle removed successfully{end}")

    except VehicleNotFoundError as e:
        print(f"{red}{bold}Error: {e}{end}")
        input("Press Enter to continue...")
        return

    input("Press Enter to continue...")

def update_vehicle(graph, vehicle_hash_table):
    """Updates a vehicle in the hash table.

    Args:
        graph: Graph of the simulation.
        vehicle_hash_table: Hash table of the vehicles in the simulation.
    """
    vehicle_id = input("Enter vehicle ID: ")
    try:
        vehicle = vehicle_hash_table.get(vehicle_id)
        print(f"{green}{bold}Vehicle found successfully{end}")
    except VehicleNotFoundError as e:
        print(f"{red}{bold}Error: {e}{end}")
        input("Press Enter to continue...")
        return

    location_id = input("Enter current location ID: ")
    if graph.has_vertex(location_id):
        print(f"{green}{bold}Location found{end}")
        vehicle.set_location(location_id)
    else:
        print(f"{red}{bold}Error: Location not found{end}")
        input("Press Enter to continue...")
        return

    destination_id = input("Enter destination ID: ")
    if graph.has_vertex(destination_id):
        try:
            distance_to_dest, path = graph.dijkstra(location_id, destination_id)
            print(
                f"{green}{bold}Path from {location_id} to {destination_id} found with a distance of {distance_to_dest}{end}")
            vehicle.set_destination(destination_id)
            vehicle.set_distance_to_destination(distance_to_dest)
        except PathNotFound as e:
            print(f"{red}{bold}Error: {e}{end}")
            input("Press Enter to continue...")
            return
    else:
        print(f"{red}{bold}Error: Destination not found{end}")
        input("Press Enter to continue...")
        return

    try:
        new_battery_lvl = int(input("Enter battery level (0-100): "))
    except ValueError:
        print(f"{red}{bold}Please enter a valid input.{end}")
        input("Press Enter to continue...")
        return
    try:
        vehicle.set_battery_level(new_battery_lvl)
        vehicle.set_destination(destination_id)
        vehicle.set_location(location_id)
    except InvalidBatteryException as e:
        print(f"{red}{bold}Error: {e}{end}")
        input("Press Enter to continue...")
        return
    print(f"{green}{bold}Vehicle updated successfully{end}")
    input("Press Enter to continue...")

def display_vehicles(vehicle_hash_table):
    """Displays all vehicles in the hash table.

    Args:
        vehicle_hash_table: Hash table of the vehicles in the simulation.
    """
    vehicles = vehicle_hash_table.export_to_array()
    try:
        choice = int(input("Display by:"
                           "\n[1]. Battery Level [Desc]"
                           "\n[2]. Distance to destination [Asc]"
                           "\nInput: "))
    except ValueError:
        print(f"{red}{bold}Please enter a valid input.{end}")
        input("Press Enter to continue...")
        return

    if choice == 1:
        sorted_vehicles = sort_by_battery(vehicles)
        if len(vehicles) > 0:
            _print_vehicle_from_arr(sorted_vehicles, True)
            input("Press Enter to continue...")

    elif choice == 2:
        sorted_vehicles = sort_by_distance(vehicles)
        if len(vehicles) > 0:
            _print_vehicle_from_arr(sorted_vehicles, True)
            input("Press Enter to continue...")

    else:
        print(f"{red}{bold}Please enter a valid input.{end}")
        input("Press Enter to continue...")

def sort_by_distance(vehicles):
    """Sorts vehicles by distance to destination.

    Args:
        vehicles: List of vehicles to sort.

    Returns:
        list: Sorted list of vehicles.
    """
    if len(vehicles) > 0:
        sort_heap = VehicleSortHeap(len(vehicles))
        sorted_vehicles = sort_heap.heapsort_vehicles(vehicles)
        return sorted_vehicles
    else:
        print(f"{red}{bold}No vehicles in the system.{end}")
        input("Press Enter to continue...")

def sort_by_battery(vehicles):
    """Sorts vehicles by battery level.

    Args:
        vehicles: List of vehicles to sort.

    Returns:
        list: Sorted list of vehicles.
    """
    if len(vehicles) > 0:
        sorted_vehicles = quick_sort(vehicles)
        return sorted_vehicles
    else:
        print(f"{red}{bold}No vehicles in the system.{end}")
        input("Press Enter to continue...")

def add_location(graph):
    """Adds a location to the graph.

    Args:
        graph: Graph of the simulation.
    """
    try:
        location_id = input("Enter location ID: ")
        graph.add_vertex(location_id)
        print(f"{green}{bold}Location added successfully{end}")
    except VertexExistsError as e:
        print(f"{red}{bold}Error: {e}{end}")
    input("Press Enter to continue...")

def add_road(graph):
    """Adds a road to the graph.

    Args:
        graph: Graph of the simulation.
    """
    try:
        vertex1_id = input("Enter first location ID: ")
        vertex2_id = input("Enter second location ID: ")
        weight = int(input("Enter length of the road: "))
        graph.add_edge(vertex1_id, vertex2_id, weight)
        print(f"{green}{bold}Road added successfully{end}")
    except (EdgeExistsError, EdgeToSameVertex, VertexNotFoundError) as e:
        print(f"{red}{bold}Error: {e}{end}")
    except ValueError:
        print(f"{red}{bold}Please enter a valid input.{end}")
    input("Press Enter to continue...")


def check_path(graph):
    """Checks if a path exists between two locations.

    Args:
        graph: Graph of the simulation.
    """
    try:
        vertex1_id = input("Enter first location ID: ")
        vertex2_id = input("Enter second location ID: ")
        distance, _ = graph.dijkstra(vertex1_id, vertex2_id)
        print(f"{green}A path exists between {vertex1_id} and {vertex2_id}, with a distance of {distance}.{end}")
    except PathNotFound as e:
        print(f"{red}{bold}Error: {e}{end}")
    except VertexNotFoundError as e:
        print(f"{red}{bold}Error: {e}{end}")
    input("Press Enter to continue...")


def display_graph(graph):
    """Displays the graph.

    Args:
        graph: Graph of the simulation.
    """
    graph.display_as_list()

def _print_vehicle_from_arr(vehicle_arr, full_info: bool):
    """Prints vehicles from an array.

    Args:
        vehicle_arr: Array of vehicles to print.
        full_info: Boolean indicating whether to print full info or not.
    """
    for vehicle in vehicle_arr:
        if full_info:
            print(f"{bold}{vehicle} | Battery Level: {vehicle.get_battery_level()} | Location: {vehicle.get_location()} | Destination: {vehicle.get_destination()} | Distance to Destination: {vehicle.get_distance_to_destination()}")
        else:
            print(f"{vehicle}")
