import os
from Graph import VertexExistsError, EdgeExistsError, VertexNotFoundError, EdgeToSameVertex
from Sorting import *
from VehicleHashTable import *

red = "\033[0;31m"
green = "\033[0;32m"
bold = "\033[1m"
end = "\033[0m"

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

def print_menu(menu_options: dict):
    print("-" * 50)
    print(f"{red}{bold}Welcome to the Autonomous Vehicle Management System{end}")
    print("-" * 50)
    for key, value in menu_options.items():
        print(f"\t{key}. {value}")
    print("-" * 50)

def get_choice(menu_options: dict):
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
    os.system("cls" if os.name == "nt" else "clear")

def main_menu(graph, vehicle_hash_table):
    running = True

    while running:
        clear_screen()

        print_menu(menu_options)
        print("Map: ")
        display_graph(graph)
        print("-" * 50)
        print("\nVehicles: ")
        print("-" * 50)
        _print_vehicle_from_arr(vehicle_hash_table.export_to_array(), False)
        choice = get_choice(menu_options)
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
                pass
            case 6:
                pass
            case 7:
                add_location(graph)
            case 8:
                add_road(graph)
            case 9:
                check_path(graph)
            case 10:
                print("Thank you for using the Autonomous Vehicle Management System. Goodbye!")
                running = False

def check_path(graph):
    try:
        vertex1_id = input("Enter first location ID: ")
        vertex2_id = input("Enter second location ID: ")
        distance = graph.is_path(vertex1_id, vertex2_id)
        if distance:
            print(f"{green}A path exists between {vertex1_id} and {vertex2_id}, with a distance of {distance}.{end}")
        else:
            print(f"{red}No path exists between {vertex1_id} and {vertex2_id}{end}")
    except VertexNotFoundError as e:
        print(f"{red}{bold}Error: {e}{end}")
    input("Press Enter to continue...")

def display_graph(graph):
    graph.display_as_list()


def add_road(graph):
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


def add_location(graph):
    try:
        location_id = input("Enter location ID: ")
        graph.add_vertex(location_id)
        print(f"{green}{bold}Location added successfully{end}")
    except VertexExistsError as e:
        print(f"{red}{bold}Error: {e}{end}")

    input("Press Enter to continue...")

def _print_vehicle_from_arr(vehicle_arr, full_info: bool):
    for vehicle in vehicle_arr:
        if full_info:
            print(f"{vehicle} | Battery Level: {vehicle.get_battery_level()} | Location: {vehicle.get_location()} | Destination: {vehicle.get_destination()} | Distance to Destination: {vehicle.get_distance_to_destination()}")
        else:
            print(f"{vehicle}")

def display_vehicles(vehicle_hash_table):
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
        sorted_vehicles = quick_sort(vehicles)
        _print_vehicle_from_arr(sorted_vehicles, True)

    elif choice == 2:
        sort_heap = VehicleSortHeap(len(vehicles))
        sorted_vehicles = sort_heap.heapsort_vehicles(vehicles)
        _print_vehicle_from_arr(sorted_vehicles, True)
        input("Press Enter to continue...")

    else:
        print(f"{red}{bold}Please enter a valid input.{end}")
        input("Press Enter to continue...")


def update_vehicle(graph, vehicle_hash_table):
    vehicle_id = input("Enter vehicle ID: ")
    try:
        vehicle = vehicle_hash_table.get(vehicle_id)
        print(f"{green}{bold}Vehicle found successfully{end}")
    except VehicleNotFoundError as e:
        print(f"{red}{bold}Error: {e}{end}")
        input("Press Enter to continue...")
        return

    location_id = input("Enter location ID: ")
    if graph.has_vertex(location_id):
        print(f"{green}{bold}Location found{end}")
        vehicle.set_location(location_id)
    else:
        print(f"{red}{bold}Error: Location not found{end}")
        input("Press Enter to continue...")
        return

    destination_id = input("Enter destination ID: ")
    if graph.has_vertex(destination_id):
        print(f"{green}{bold}Destination found{end}")

        distance_to_dest = graph.is_path(location_id, destination_id)
        if distance_to_dest:
            print(f"{green}{bold}Path from {location_id} to {destination_id} found with a distance of {distance_to_dest}{end}")
            print(graph.dijkstra(location_id, destination_id))
            vehicle.set_destination(destination_id)
            vehicle.set_distance_to_destination(distance_to_dest)
        else:
            print(f"{red}{bold}No path from {location_id} to {destination_id} was found.{end}")
            input("Press Enter to continue...")
            return
    else:
        print(f"{red}{bold}Error: Destination not found{end}")
        input("Press Enter to continue...")
        return

    vehicle.set_destination(destination_id)
    vehicle.set_location(location_id)
    print(f"{green}{bold}Vehicle updated successfully{end}")
    input("Press Enter to continue...")


def remove_vehicle(vehicle_hash_table):
    vehicle_id = input("Enter vehicle ID: ")

    try:
        vehicle_hash_table.remove(vehicle_id)
        print(f"{green}{bold}Vehicle removed successfully{end}")

    except VehicleNotFoundError as e:
        print(f"{red}{bold}Error: {e}{end}")
        input("Press Enter to continue...")
        return

    input("Press Enter to continue...")


def add_vehicle(vehicle_hash_table):
    vehicle_id = input("Enter vehicle ID: ")
    vehicle = Vehicle(vehicle_id)

    try:
        vehicle_hash_table.put(vehicle_id, vehicle)

    except DuplicateVehicleFound as e:
        print(f"{red}{bold}Error: {e}{end}")
        input("Press Enter to continue...")
        return

    print(f"{green}{bold}Vehicle added successfully{end}")
    input("Press Enter to continue...")