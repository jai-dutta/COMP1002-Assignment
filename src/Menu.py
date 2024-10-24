"""Menu.py

This file contains the menu for the simulation.

DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
"""

import os

import numpy
from Graph import PathNotFound, VertexExistsError, EdgeExistsError, VertexNotFoundError, EdgeToSameVertex, Graph
from Sorting import *
from Vehicle import *
from VehicleHashTable import *

# Define ANSI escape codes for colors and formatting
red = "\033[0;31m"
green = "\033[0;32m"
bold = "\033[1m"
negative = "\033[7m"
end = "\033[0m"


def print_menu():
    """Prints the menu.

    Returns:
        None

    Note:
        ASCII Art generated from https://patorjk.com/software/taag + https://ozh.github.io/ascii-tables/ 
    """

    header = """
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
            ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝"""
    menu_options = f"""
╔════════════════════════════════╦══════════════════════════╗
║            Vehicle             ║        Locations         ║
╠════════════════════════════════╬══════════════════════════╣
║ [{green}1{end}] Add a vehicle              ║ [{green}7{end}] Add a location       ║
║ [{green}2{end}] Remove a vehicle           ║ [{green}8{end}] Add a road           ║
║ [{green}3{end}] Update a vehicle           ║ [{green}9{end}] Check road existence ║
║ [{green}4{end}] Display all vehicles       ║                          ║
║ [{green}5{end}] Find nearest vehicle       ║                          ║
║ [{green}6{end}] Find highest battery level ║                          ║
╠════════════════════════════════╩══════════════════════════╣
║ [{red}10{end}] Exit                                                 ║
╚═══════════════════════════════════════════════════════════╝"""

    print(header)
    print(menu_options)


def get_choice():
    """Grabs and validates the user's choice from the menu options.

    Returns:
        int: The user's choice.
    """
    while True:
        try:
            choice = int(input("Please enter option: "))
            if choice not in range(1, 11):
                print(f"{red}{bold}Invalid input. Please enter a number between 1 and 10.{end}")
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
        # Export vehicles from hash table to array each time the loop runs (for printing and sorting)
        vehicles = vehicle_hash_table.export_to_array()
        sort_heap = VehicleSortHeap(len(vehicles))

        clear_screen()

        print_menu()

        # Print locations
        print("Locations: ")
        print()
        display_graph(graph)
        print("═" * 50)

        # Print vehicles
        print("\nVehicles: ")
        print()
        _print_vehicle_from_arr(vehicles, False)
        print("═" * 50)

        # Get user choice
        choice = get_choice()

        # Match user choice to menu option
        match choice:
            # Add vehicle
            case 1:
                add_vehicle(vehicle_hash_table)

            # Remove vehicle    
            case 2:
                remove_vehicle(vehicle_hash_table)

            # Update vehicle
            case 3:
                update_vehicle(graph, vehicle_hash_table)

            # Display vehicles
            case 4:
                display_sorted_vehicles(vehicles, sort_heap)

            # Find nearest vehicle
            case 5:
                try:
                    sort_heap.find_nearest_vehicle(vehicles)
                except VehiclesEmptyException as e:
                    handle_error(e)

            # Find the highest battery level
            case 6:
                try:
                    find_highest_battery_level(vehicles)
                except VehiclesEmptyException as e:
                    handle_error(e)

            # Add location
            case 7:
                add_location(graph)

            # Add road
            case 8:
                add_road(graph)

            # Check path
            case 9:
                check_path(graph)

            # Exit
            case 10:
                print("Thank you for using the Autonomous Vehicle Management System. Goodbye!")
                running = False


def add_vehicle(vehicle_hash_table: VehicleHashTable):
    """Adds a vehicle to the hash table.

    Args:
        vehicle_hash_table: Hash table of the vehicles in the simulation.
    """

    vehicle_id = input("Enter vehicle ID: ")

    try:
        battery_level = int(input("Enter battery level (0-100): "))
    except ValueError:
        return handle_error(f"{red}{bold}Please enter a valid input.{end}")

    try:
        vehicle = Vehicle(vehicle_id, battery_level)
    except InvalidBatteryException as e:
        return handle_error(e)

    try:
        vehicle_hash_table.put(vehicle)
    except DuplicateVehicleFound as e:
        return handle_error(e)

    print(f"{green}{bold}Vehicle added successfully{end}")
    input("Press Enter to continue...")


def remove_vehicle(vehicle_hash_table: VehicleHashTable):
    """Removes a vehicle from the hash table.

    Args:
        vehicle_hash_table: Hash table of the vehicles in the simulation.
    """
    vehicle_id = input("Enter vehicle ID: ")

    try:
        vehicle_hash_table.remove(vehicle_id)
        print(f"{green}{bold}Vehicle removed successfully{end}")

    except VehicleNotFoundError as e:
        return handle_error(e)

    input("Press Enter to continue...")


def update_vehicle(graph: Graph, vehicle_hash_table: VehicleHashTable):
    """Updates a vehicle in the hash table.

    Args:
        graph: Graph of the simulation.
        vehicle_hash_table: Hash table of the vehicles in the simulation.
    """

    # Get vehicle ID and validate it to make sure the vehicle exists.
    vehicle_id = input("Enter vehicle ID: ")
    try:
        vehicle = vehicle_hash_table.get(vehicle_id)
        print(f"{green}{bold}Vehicle found successfully{end}")
    except VehicleNotFoundError as e:
        return handle_error(e)

    # Get the location of the vehicle and validate it to make sure the location exists.
    location_id = input("Enter current location ID: ")
    location_node = graph.find_vertex(location_id)
    if location_node:
        print(f"{green}{bold}Location found{end}")
        vehicle.set_location(location_node)
    else:
        return handle_error(f"{red}{bold}Location not found{end}")

    # Get the destination of the vehicle and validate it to make sure the location exists.
    destination_id = input("Enter destination ID: ")
    destination_node = graph.find_vertex(destination_id)
    if destination_node:

        # Make sure user hasn't set a path from a location to itself
        if destination_node == location_node:
            return handle_error(f"{red}{bold}Destination cannot be the same as the current location{end}")

    else:
        return handle_error(f"{red}{bold}Destination not found{end}")

    # Check for path and calculate distance between location
    try:
        distance_to_dest, _ = graph.dijkstra(location_id, destination_id)
        print(f"{green}{bold}Path from {location_node.get_label()} to {destination_node.get_label()} found with a "
              f"distance of {distance_to_dest}{end}")
    except PathNotFound as e:
        return handle_error(e)

    # Get new battery level for the vehicle.
    try:
        new_battery_lvl = int(input("Enter battery level (0-100): "))
    except ValueError:
        return handle_error(f"{red}{bold}Please enter a valid input.{end}")

    try:
        vehicle.set_battery_level(new_battery_lvl)
        vehicle.set_location(location_node)
        vehicle.set_destination(destination_node)
        vehicle.set_distance_to_destination(distance_to_dest)
    except InvalidBatteryException as e:
        return handle_error(e)

    print(f"{green}{bold}Vehicle updated successfully{end}")
    input("Press Enter to continue...")


def handle_error(e):
    print(f"{red}{bold}Error: {e}{end}")
    input("Press Enter to continue...")
    return


def display_sorted_vehicles(vehicles: numpy.ndarray, sort_heap: VehicleSortHeap):
    """Displays all vehicles in the hash table.

    Args:
        vehicles: Array of vehicles to sort.
        sort_heap: Heap to sort the vehicles.
    """
    try:
        choice = int(input("Display by:"
                           "\n[1]. Battery Level [Desc]"
                           "\n[2]. Distance to destination [Asc]"
                           "\nInput: "))
    except ValueError:
        return handle_error(f"{red}{bold}Please enter a valid input.{end}")

    if choice == 1:
        sorted_vehicles = sort_by_battery(vehicles)

    elif choice == 2:
        sorted_vehicles = sort_by_distance(vehicles, sort_heap)

    else:
        return handle_error(f"{red}{bold}Please enter a valid input.{end}")

    if len(sorted_vehicles) > 0:
        _print_vehicle_from_arr(sorted_vehicles, True)
        input("Press Enter to continue...")
    else:
        return handle_error(f"{red}{bold}No vehicles are in the AVMS.{end}")


def sort_by_distance(vehicles: numpy.ndarray, vehicle_sort_heap: VehicleSortHeap) -> numpy.ndarray:
    """Sorts vehicles by distance to destination.

    Args:
        vehicles: numpy.ndarray of vehicles to sort.
        vehicle_sort_heap: VehicleSortHeap object to store Vehicles for heapsort.

    Returns:
        numpy.ndarray: Sorted array of vehicles.
        Returns empty array if input is empty.

    Note:
        Sorting is done based on vehicle's distance to destination.
    """
    if not len(vehicles):
        return numpy.array([])

    return vehicle_sort_heap.heapsort_vehicles(vehicles)


def sort_by_battery(vehicles: numpy.ndarray):
    """Sorts vehicles by battery level.

    Args:
        vehicles: List of vehicles to sort.

    Returns:
        list: Sorted list of vehicles.
    """
    if not len(vehicles):
        return numpy.array([])
    sorted_vehicles = quick_sort(vehicles)
    return sorted_vehicles


def add_location(graph: Graph):
    """Adds a location to the graph.

    Args:
        graph: Graph of the simulation.
    """
    try:
        location_id = input("Enter location ID: ")
        graph.add_vertex(location_id)
        print(f"{green}{bold}Location added successfully{end}")
    except VertexExistsError as e:
        return handle_error(e)
    input("Press Enter to continue...")


def add_road(graph: Graph):
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
        return handle_error(e)
    except ValueError:
        return handle_error(f"{red}{bold}Please enter a valid input.{end}")


def check_path(graph: Graph):
    """Checks if a path exists between two locations.

    Args:
        graph: Graph of the simulation.
    """
    try:
        vertex1_id = input("Enter first location ID: ")
        vertex2_id = input("Enter second location ID: ")
        distance, _ = graph.dijkstra(vertex1_id, vertex2_id)
        print(f"{green}A path exists between {vertex1_id} and {vertex2_id}, with a distance of {distance}.{end}")
    except (VertexNotFoundError, PathNotFound) as e:
        return handle_error(e)


def display_graph(graph: Graph):
    """Displays the graph.

    Args:
        graph: Graph of the simulation.
    """
    graph.display_as_list()


def _print_vehicle_from_arr(vehicle_arr: numpy.ndarray, full_info: bool):
    """Prints vehicles from an array.

    Args:
        vehicle_arr: Array of vehicles to print.
        full_info: Boolean indicating whether to print full info or not.
    """
    for vehicle in vehicle_arr:
        if full_info:
            print(f"{bold}{vehicle} | Battery Level: {vehicle.get_battery_level()}"
                  f" | Location: {vehicle.get_location()}"
                  f" | Destination: {vehicle.get_destination()}"
                  f" | Distance to Destination: {vehicle.get_distance_to_destination()}")
        else:
            print(f"{vehicle}")
