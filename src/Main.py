import os
from Graph import Graph, VertexExistsError, EdgeExistsError
from Vehicle import Vehicle
from MinHeap import MinHeap
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
    9: "Display map",
    10: "Check path existance",
    11: "Exit"
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

def main():
    vehicle_hash_table = VehicleHashTable(10)
    graph = Graph()


    running = True

    while running:
        clear_screen()

        print_menu(menu_options)
        choice = get_choice(menu_options)
        match choice:
            case 1:
                vehicle_id = input("Enter vehicle ID: ")
                vehicle = Vehicle(vehicle_id)
                vehicle_hash_table.put(vehicle_id, vehicle)
                print(f"{green}{bold}Vehicle added successfully{end}")
                input("Press Enter to continue...")
            case 2:
                vehicle_id = input("Enter vehicle ID: ")
                try:
                    vehicle_hash_table.remove(vehicle_id)
                    print(f"{green}{bold}Vehicle removed successfully{end}")
                except VehicleNotFoundError as e:
                    print(f"{red}{bold}Error: {e}{end}")
                input("Press Enter to continue...")
            case 3:
                vehicle_id = input("Enter vehicle ID: ")

                try:
                    vehicle = vehicle_hash_table.get(vehicle_id)
                    print(f"{green}{bold}Vehicle found successfully{end}")
                except VehicleNotFoundError as e:
                    print(f"{red}{bold}Error: {e}{end}")

                location_id = input("Enter location ID: ")
                if(graph.has_vertex(location_id)):
                    print(f"{green}{bold}Location found{end}")
                else:
                    print(f"{red}{bold}Error: Location not found{end}")

                destination_id = input("Enter destination ID: ")
                if(graph.has_vertex(destination_id)):
                    print(f"{green}{bold}Destination found{end}")
                else:
                    print(f"{red}{bold}Error: Destination not found{end}")

                vehicle.set_destination(destination_id)
                vehicle.set_location(location_id)
                print(f"{green}{bold}Vehicle updated successfully{end}")
                input("Press Enter to continue...")
            case 4:
                print(vehicle_hash_table)
                input("Press Enter to continue...")
            case 5:
                heap
            case 6:
                pass
            case 7:
                try:
                    location_id = input("Enter location ID: ")
                    graph.add_vertex(location_id)
                    print(f"{green}{bold}Location added successfully{end}")
                except VertexExistsError as e:
                    print(f"{red}{bold}Error: {e}{end}")
                input("Press Enter to continue...")
            case 8:
                try:
                    vertex1_id = input("Enter first location ID: ")
                    vertex2_id = input("Enter second location ID: ")
                    weight = int(input("Enter length of the road: "))
                    graph.add_edge(vertex1_id, vertex2_id, weight)
                    print(f"{green}{bold}Road added successfully{end}")
                except EdgeExistsError or ValueError as e:
                    print(f"{red}{bold}Error: {e}{end}")
                input("Press Enter to continue...")
            case 9:
                graph.display_as_list()
                input("Press Enter to continue...")
            case 10:
                pass
            case 11:
                print("Thank you for using the Autonomous Vehicle Management System. Goodbye!")
                running = False
           
if __name__ == "__main__":
    main()