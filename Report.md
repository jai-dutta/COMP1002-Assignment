# COMP1002 Data Structures and Algorithms Assignment Report

**Author:** Jai Dutta  
**Student ID:** 22073372

## Introduction

This report details my process of developing the DSA Assignment, an autonomous vehicle management system designed to use a multitude of data structures and algorithms that have been taught throughout the semester.

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


### Sorting.py

### Vehicle.py

### VehicleHashTable.py

### Menu.py

### Main.py

## Test Cases

(List of test cases with inputs and expected outputs to be added here)

## Challenges and Solutions

(Description of encountered challenges and implemented solutions to be added here)

## Efficiency Analysis and Potential Improvements

(Analysis of time and space complexity, along with suggestions for improvements to be added here)

## Conclusion

(Summary of key outcomes and learnings from the assignment to be added here)
