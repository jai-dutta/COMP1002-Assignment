import os
from Graph import Graph
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
    3: "Display all vehicles",
    4: "Find nearest vehicle",
    5: "Find highest battery level",
    6: "Add a location",
    7: "Add a road",
    8: "Display map",
    9: "Check path existance",
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
                print(vehicle_hash_table)
                input("Press Enter to continue...")
            case 4:
                pass
                #find_nearest_vehicle()
            case 5:
                pass
                #find_highest_battery_level()
            case 6:
                pass
                #add_location()
            case 7:
                pass
                #add_road()
            case 8:
                pass
                #display_map()
            case 9:
                pass
                #check_path_existence()
            case 10:
                print("Thank you for using the Autonomous Vehicle Management System. Goodbye!")
                running = False
           
if __name__ == "__main__":
    main()