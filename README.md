# COMP1002 Data Structures and Algorithms Assignment Report

**Author:** Jai Dutta  

## Introduction

This report details my process of developing the DSA Assignment, an autonomous vehicle management system designed to use a multitude of data structures and algorithms that have been taught throughout the semester.

I have implemented a program which consists of the following major parts:
- Location and Road network using a Graph
- Vehicles (stored in a Hash Table) positioned at one location of a user's choosing, with destination also set by the user. The distance to destination is automatically calculated using Dijkstra's algorithm and displayed to the user.
- Sorting algorithms for displaying the vehicles by either distance to destination or battery level.
- An interactive menu for user interaction.
- Extensive error handling and custom exceptions.

I've implemented the code in a way that follows the principles of OOP (encapsulation, inheritance and abstraction are used, polymorphism wasn't needed.) and modular software design philosophy. 
The code is extensible, and concerns are clearly separated.

## Usage:

To run the AVMS simulation: from src directory run `python Main.py`
to run the tests: from root directory run `pytest`

## Class and Method Descriptions

### Graph.py

**Purpose:** Represents the road network for vehicle navigation. The graph is weighted and undirected.  
Implemented using an adjacency linked list.  

**Key Methods:**

- `add_vertex`: Adds a vertex to the graph.
- `add_edge`: Adds an edge between two vertices.
- `find_vertex`: Retrieves vertex object by its label
- `get_adjacent`: Returns the adjacent vertices and their edge weights.
- `dijkstra`: Implements Dijkstra's algorithm to find the shortest path between two vertices.
- `is_path`: Performs a breadth-first search to check if there is a path between two vertices.

**Implementation Details:**  
The graph is implemented using an linked list, where each vertex has a linked list of its adjacent vertices and the edge weights.
The graph itself contains a linked list of all its vertices.


### LinkedList.py

**Purpose:** Represents a double ended, doubly linked list.

**Key Methods:**

- `insert_first`: Inserts a new node at the beginning of the linked list.
- `insert_before`: Inserts a new node before a node at a given index.
- `insert_last`: Inserts a new node at the end of the linked list.
- `remove_first`: Removes/returns first node from the linked list.
- `remove_last`: Removes/returns last node from linked list.
- `remove_at`: Removes the node in the linked list at a given index.

**Implementation Details:**  

The linked list is doubly ended and doubly linked. Each ListNode has a pointer to the previous and the next node, and LinkedList
has a pointer to the first and last node. This allows for efficient insertion and removal of nodes from both ends, which is important for the queue and stack implementations.

### Queue.py

**Purpose:** Represents a queue data structure.

**Key Methods:**
- `enqueue`: Enqueues a value to the end of the queue.
- `dequeue`: Dequeues and returns the value from the start of the queue.
- `peek`: Returns the first value in the queue

**Implementation Details:**

The queue is implemented using a Linked List, which eliminates the need for circular or shuffling queue design, as the linked list can always accommodate extra values.

### MinHeap.py

**Purpose:** Represents a MinHeap.

**Key Methods:**
- `add`: Adds a value to the MinHeap
- `trickel_up`: Moves new value up the heap by comparing with parent nodes until it's in the correct spot to maintain the MinHeap property
- `trickle_down`: Compares a node with its children and swaps with the smaller child, continues down until Min Heap property is restored (used after removal) 
- `remove`: Removes and returns the root node.

**Implementation Details:**

The MinHeap is implemented for use as a parent to the VehicleSortHeap (specialised MinHeap) and for a Priority Queue in dijkstra's algorithm.

### Sorting.py

**Purpose:** Represents a Vehicle Sort MinHeap and contains the Quicksort implementation. The VehicleSortHeap is a specialised MinHeap that stores a Vehicle on each node, and the priority is the vehicles DistanceToDestination.

**Key Methods:**
- `add`: Adds a vehicle to the heap.
- `heapsort_vehicles`: Sorts an array of vehicles based on Distance to Destination in ascending order. Takes in an array of vehicles and returns the sorted array.
- `find_nearest_vehicle`: Sorts an array of vehicles using heap sort and returns the first vehicle (lowest distance to destination.)
- `quick_sort`: Sorts an array of vehicles based on Battery Level in descending order.
- `do_partitioning`: Partitioning for quicksort, compares battery level of each vehicle rather than value. e.g. if arr[i].get_battery_level() > pivot_val.get_battery_level():
- `find_highest_battery_level`: Sorts an array of vehicles using quick sort and returns the first vehicle (Highest battery.)

**Implementation Details:**

The VehicleSortHeap inherits from MinHeap. The changes/additions are listed below:
- add: Adds a vehicle entry to the heap.
- heapsort_vehicles: Sorts the vehicles in the heap.
- find_nearest_vehicle: Finds the nearest vehicle to the destination.

Quick sort uses middle element as pivot. This provides good average performance (average o(n log n) ) for random/unsorted data (as is contained within the VehicleHashTable)


### Vehicle.py

**Purpose:** Represents a Vehicle.

**Key Methods:**
- `get_ID`: Returns ID
- `get_location`: Returns location (GraphVertex)
- `get_destination`: Returns destination (GraphVertex)
- `get_distance_to_destination`: Returns distance to destination (automatically calculated using dijkstra's algorithm.)
- And associated setters.

**Implementation Details:**

The vehicle class is a basic class representing a vehicle, and follows OOP principles of encapsulation and abstraction.

### VehicleHashTable.py

**Purpose:** Represents a Hash Table containing the vehicles within the simulation.

**Key Methods:**
- `put`: Inserts a new vehicle into the hash table.
- `get`: Gets a vehicle from the hash table from provided ID.
- `remove`: Removes a vehicle from the hash table with provided ID.
- `export_to_array`: Creates an array of all vehicles within the hash table.
- `_hash`: Creates a hash from provided key (in this implementation the key is the vehicle ID.)

**Implementation Details:**

Collision resolution: Linear Probing
Hashing Algorithm: Uses ASCII values of the provided ID to create a hopefully unique hash. The hash is reduced by applying modulo to the hash with the size of the hash table so it fits within the array.
Resizing: If the load factor falls below 0.2 or rises above 0.75, the hash table will double in size. A new array is created, and the existing entries are put in the new table. **Note**: On the size down checks, I've implemented a check to ensure the hash table contains over 100 values before the hash table can reduce in size. This prevents unnecessary resizing when the hash table contains few values.

### Menu.py

**Purpose:** Provides an interactive menu for the user.

### Main.py
**Purpose:** Creates necessary objects and calls the Menu, main run file.

## Test Cases

The test cases can be found in the /tests directory.  
To run the tests, run pytest from the root directory.

## Challenges and Solutions

### Displaying all vehicles from the hash table  
As I wanted all vehicles in the system to be displayed on the main menu, I had to add a function to export all hash table entries to an array and print it.

### Dijkstra's Algorithm
I implemented Dijkstra's Algorithm for shortest path checks, as I wanted the distance to destination to be calculated automatically when a location and destination were set for a vehicle.  
BFS would not be suitable for this application, as it is a weighted graph.  

### Non-use of built in ADTS such as Lists
I have used numpy arrays in all cases where I would normally use a Python list, which presented a bit of a learning curve.

## Efficiency Analysis and Potential Improvements

- Hash Table:
  - Getting/removing vehicle: O(1) in the average/best case, O(N) in the worst case. May need linear probing which entails iterating through the array.
  - Insertion: O(1) in the average/best case, O(N) worst case if a hash collision occurs and extensive iteration to find an empty spot is needed.
  - Resizing: O(N) in all cases. Must iterate through array, rehash and copy each element to a new array.
  - Export to Array: O(N) in all cases, must iterate through array while checking for state == 1.
  - Improvement: Implement double hashing instead of linear probing, could improve worst case performance.
- Sorting:
  - Heap Sort: The vehicles must be added to a new Heap each sort, but algorithm still runs faster than Quicksort from testing with 25000 vehicles. The algorithm runs in O(n log n) time in all cases.
  - Quick Sort: Runs in O(N^2) in the worst case, but averages O(n log n).
- Graph:
  - Dijkstra's Algorithm: Runs in O(E log V) where E is the number of edges, V is the number of vertices. Uses a MinHeap priority queue.
  - BFS: Runs in O(V + E)
  - Add vertex: Runs in O(N) where N is the number of vertices, must iterate through Linked List of vertices to ensure duplicate vertex is not present.
  - Add edge: Runs in O(N) where N is the number of vertices, must iterate twice through Linked List of vertices to ensure both Vertices are present to add an edge between them. Simplified to O(N).
    Could be improved by doing one pass to find both vertices, or using a hash table for O(1) lookup.
  - Improvement: Implement a hash table to store vertices, could change O(N) existence checks to O(1).
- GraphVertex:
  - Adjacency check: Runs in O(N). Each GraphVertex has it's own Linked List of adjacencies which must be traversed completely for an adjacency check.
  - Set adjacent: Runs in O(1), the new adjacent vertex is inserted at the end of the linked list.
  - Remove adjacent: Runs in O(N), linked list must be traversed to find the vertex to remove.
- Linked List:
  - Insert front: Runs in O(1) as uses head pointer.
  - Insert rear: Runs in O(1) as uses tail pointer.
  - Insert at: Runs in O(N) in the worst case, as must iterate through the linked list to find the specified index to insert the new node at.
  - Remove front: Runs in O(1) as uses head/next pointers.
  - Remove rear: Runs in O(1) as uses tail/prev pointers.
  - Remove At: Runs in O(N) in the worst case, as must iterate through the linked list to find the specified index to remove the node.
- Queue:
  - Enqueue: Runs in O(1), as it calls the Linked List insert rear method.
  - Dequeue: Runs in O(1), as it calls the Linked List remove front method.

## Conclusion

This assignment has been very helpful for me in piecing together and implementing data structures to seamlessly work with one another.  
Although challenging in some aspects, I felt like the assignment specification was straightforward.  
The logical next step for this code is to implement movement of vehicles between locations, with dynamically updating battery levels.