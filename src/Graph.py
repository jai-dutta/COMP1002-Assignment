"""
Graph.py

This file contains the Graph class, which represents a weighted, undirected graph.

DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
"""
import numpy as np
from LinkedList import LinkedList
from MinHeap import *
from Queue import Queue


class GraphVertex:
    """A class to represent a vertex in the graph.

    Attributes:
        label: A string representing the label of the vertex.
        value: The value associated with the vertex. (not necessary for the assignment - left over from Practical)
        visited: A boolean indicating if the vertex has been visited.
        links: A LinkedList of adjacent vertices and their edge weights.
    """

    def __init__(self, label: str, value: any = None):
        """Initialize a GraphVertex object.

        Args:
            label: A string representing the label of the vertex.
            value: The value associated with the vertex.
        """
        self.label = label
        self.value = value
        self.visited = False
        self.links = LinkedList()

    def __str__(self) -> str:
        """Return a string representation of the vertex.

        Returns:
            A string representation of the vertex.
        """
        return f"{self.label}: {self.value}" if self.value else f"{self.label}"

    def get_label(self) -> str:
        """Get the label of the vertex.

        Returns:
            The label of the vertex.
        """
        return self.label

    def get_value(self) -> any:
        """Get the value of the vertex.

        Returns:
            The value of the vertex.
        """
        return self.value

    def get_adjacent(self) -> np.ndarray:
        """Get the adjacent vertices and their edge weights.

        Returns:
            An array of tuples, each containing an adjacent vertex and its edge weight.
        """
        # Create an array to store the adjacent vertices and their weights
        adjacent_vertices = np.empty(len(self.links), dtype=object)
        # Iterate through the linked list and add the adjacent vertices and their weights to the new array
        for i in range(len(self.links)):
            adjacent_vertices[i] = self.links[i].get_value()
        # Return the new array
        return adjacent_vertices

    def set_adjacent(self, vertex: "GraphVertex", weight: float) -> None:
        """Set an adjacent vertex with its edge weight.

        Args:
            vertex: The adjacent GraphVertex object.
            weight: The weight of the edge connecting to the adjacent vertex.
        """
        # Create a flag to check if the vertex was inserted
        inserted = False
        # Iterate through the linked list and insert the adjacent vertex and its weight in the correct position (alphabetically (this is a remnant from the Practical, not needed for the assignment as using weighted edges with Dijkstra's, instead of BFS/DFS))
        for i in range(len(self.links)):
            current_vertex, current_weight = self.links[i].get_value()
            if vertex.get_label() < current_vertex.get_label():
                self.links.insert_before((vertex, weight), i)
                inserted = True
                break
        # If not inserted, add to the end
        if not inserted:
            self.links.insert_last((vertex, weight))

    def remove_adjacent(self, vertex: "GraphVertex") -> None:
        """Remove an adjacent vertex.

        Args:
            vertex: The GraphVertex object to be removed from adjacency list.
        """
        # Iterate through linked list of adjacent vertices and remove the specified adjacent vertex from the list.
        for i in range(len(self.links)):
            if self.links[i].get_value()[0] == vertex:
                self.links.remove_at(i)
                break

    def set_visited(self) -> None:
        """Mark the vertex as visited."""
        self.visited = True

    def clear_visited(self) -> None:
        """Clear the visited status of the vertex."""
        self.visited = False

    def get_visited(self) -> bool:
        """Get the visited status of the vertex.

        Returns:
            A boolean indicating whether the vertex has been visited.
        """
        return self.visited


class Graph:
    """A class to represent an undirected, weighted simple graph.

    Attributes:
        vertices: A LinkedList containing each vertex of the graph.
        count: An integer count of vertices in the graph.
    """

    def __init__(self):
        """Initialize a Graph object."""
        self.vertices = LinkedList()
        self.count = 0

    def add_vertex(self, label: str, value: any = None) -> None:
        """Add a vertex to the graph. Maintains sorted order.

        Args:
            label: Label of the vertex.
            value: Value of the vertex. Defaults to 0.

        Raises:
            VertexExistsError: If a vertex with the given label already exists.
        """
        # If existing vertex with the same label, throw a VertexExistsError
        if self.find_vertex(label):
            raise VertexExistsError("Duplicate location found.")

        # Create new vertex object with the given label and value
        new_vertex = GraphVertex(label, value)

        # If the graph is empty, insert the new vertex at the end (as it's the only vertex)
        if self.vertices.is_empty():
            self.vertices.insert_last(new_vertex)
        # Otherwise, insert the new vertex in the correct position (alphabetically (again, remnant from the Practical, not needed for the assignment as using weighted edges with Dijkstra's, instead of BFS/DFS))
        else:
            inserted = False
            for i in range(len(self.vertices)):
                if label < self.vertices[i].get_value().get_label():
                    self.vertices.insert_before(new_vertex, i)
                    inserted = True
                    break

            if not inserted:
                self.vertices.insert_last(new_vertex)

        self.count += 1

    def delete_vertex(self, label: str) -> None:
        """Delete a vertex from the graph.

        Args:
            label: Label of the vertex to delete.

        Raises:
            VertexNotFoundError: If the vertex to delete is not found.
        """
        # Find the index of the vertex to delete
        index = self._find_vertex_index(label)
        # If the vertex is not found, raise a VertexNotFoundError
        if index is None:
            raise VertexNotFoundError("Vertex to delete not found!")
        # Remove the vertex from the linked list
        self.vertices.remove_at(index)
        self.count -= 1

    def add_edge(self, label1: str, label2: str, weight: float) -> None:
        """Add an edge between two vertices.

        Args:
            label1: Label of the first vertex.
            label2: Label of the second vertex.
            weight: Weight of the edge.

        Raises:
            EdgeExistsError: If the edge already exists.
            VertexNotFoundError: If one or both vertices are not found.
            EdgeToSameVertex: If attempting to add an edge from a vertex to itself.
        """
        # If edge already exists, raise an EdgeExistsError
        if self.is_adjacent(label1, label2):
            raise EdgeExistsError("Road exists. Cannot add multiple roads in a simple graph.")

        # Find the two given vertices from label
        vertex1 = self.find_vertex(label1)
        vertex2 = self.find_vertex(label2)

        # If both vertices have been found, add the edge (but check if they are the same vertex first)
        if vertex1 and vertex2:
            if vertex1 != vertex2:
                vertex1.set_adjacent(vertex2, weight)
                vertex2.set_adjacent(vertex1, weight)
            else:
                raise EdgeToSameVertex("Cannot add road from location to itself.")
        else:
            raise VertexNotFoundError("Cannot find one or both locations to add road.")

    def delete_edge(self, label1: str, label2: str) -> None:
        """Delete an edge between two vertices.
        
        Args:
            label1: Label of the first vertex.
            label2: Label of the second vertex.

        Raises:
            EdgeExistsError: If the edge to delete does not exist.
            EdgeToSameVertex: If attempting to remove an edge from a vertex to itself.
        """
        # If the edge does not exist, raise an EdgeExistsError
        if not self.is_adjacent(label1, label2):
            raise EdgeExistsError("Road to delete does not exist.")

        # Find the two given vertices form label
        vertex1 = self.find_vertex(label1)
        vertex2 = self.find_vertex(label2)
        # If both vertices have been found, remove the edge (but check if they are the same vertex first)
        if vertex1 and vertex2:
            if vertex1 != vertex2:
                vertex1.remove_adjacent(vertex2)
                vertex2.remove_adjacent(vertex1)
            else:
                raise EdgeToSameVertex("Cannot remove road from location to itself.")

    def has_vertex(self, label: str) -> bool:
        """Check if a vertex exists.

        Args:
            label: Label of vertex to check.

        Returns:
            True if the vertex exists, False otherwise.
        """
        return True if self.find_vertex(label) else False

    def get_vertex_count(self) -> int:
        """Get the vertex count.

        Returns:
            The number of vertices in the graph.
        """
        return self.count

    def get_adjacent(self, label: str) -> GraphVertex | None:
        """Get adjacent vertices to specified vertex.

        Args:
            label: Label for the vertex whose adjacent vertices are to be retrieved.

        Returns:
            A list of adjacent vertices.

        Raises:
            VertexNotFoundError: If the specified vertex is not found.
        """
        vertex = self.find_vertex(label)
        if vertex:
            return vertex.get_adjacent()
        else:
            raise VertexNotFoundError("Location not found.")

    def is_adjacent(self, label1: str, label2: str) -> bool:
        """Check if two vertices are adjacent.

        Args:
            label1: Label of the first vertex to check.
            label2: Label of the second vertex to check.

        Returns:
            True if the vertices are adjacent, False otherwise.
        """
        vertex1 = self.find_vertex(label1)
        vertex2 = self.find_vertex(label2)
        if vertex1 and vertex2:
            for vertex, _ in vertex1.get_adjacent():
                if vertex2 == vertex:
                    return True
        return False

    def display_as_list(self) -> None:
        """Display the graph as an adjacency list."""
        for vertex in self.vertices: # Iterate through each vertex in the linked list
            print(f"{vertex.get_value()} ", end="") # Print the vertex label as the base
            if len(vertex.get_value().get_adjacent()) > 0: # If the vertex has adjacent vertices
                for count, (adjacent_vertex, weight) in enumerate(vertex.get_value().get_adjacent()): # Iterate through the adjacency linked list, using the count to determine if it's the last adjacent vertex
                    # Sorry this is very messy. The purpose of this is to stop the arrow from being printed after the last adjacent vertex.
                    # Print the arrow between vertices with weight in the middle e.g: - 4 > - Print the adjacent vertice label - If count is less than the number of adjacent vertices, print another arrow as there will be another vertex to print
                    print(f"{f'- {weight} > {adjacent_vertex} ' if count + 1 < len(vertex.get_value().get_adjacent()) else f'- {weight} > {adjacent_vertex} '} ", end="")
            print() # Print newline

    def display_as_matrix(self) -> None:
        """Display the graph as an adjacency matrix."""
        matrix = np.zeros((self.count, self.count), dtype=int) # Create a 2d array of zeros with the size of the number of vertices

        for row in range(len(matrix)):
            for col in range(len(matrix)):
                if self.is_adjacent(self.vertices[row].get_value().get_label(), # For each element in the 2d array, check if the vertices the element corresponds to are adjacent, if so, set the element to 1 to represent the edge
                                    self.vertices[col].get_value().get_label()):
                    matrix[row][col] = 1

        print()
        print("\t", end="")
        # Print the horizontal labels of the vertices
        for i in self.vertices:
            print(i.get_value().get_label(), end="\t")
        print()

        # Print the 2d array and the verticalk labels
        for row in range(len(matrix)):
            print(self.vertices[row].get_value().get_label(), end="\t") # Print the vertical label of the vertex
            for col in range(len(matrix)):
                print(matrix[row][col], end="\t") # Print the element in the 2d array
            print()

    def find_vertex(self, label: str) -> GraphVertex | None:
        """Find a vertex given a label within the graph.

        Args:
            label: The label of the vertex to find.

        Returns:
            The vertex if found, None otherwise.
        """
        for vertex in self.vertices:
            if vertex.get_value().get_label().casefold() == label.casefold():
                return vertex.get_value()
        return None

    def _find_vertex_index(self, label: str) -> int | None:
        """Find the index of a vertex using its label.

        Args:
            label: Label of the vertex to find.

        Returns:
            The index of the vertex if found, None otherwise.
        """
        for i in range(len(self.vertices)):
            if self.vertices[i].get_value().get_label() == label:
                return i

    def dijkstra(self, start_label: str, end_label: str) -> tuple[float, list]:
        """Find the shortest path between two vertices using Dijkstra's algorithm.

        Args:
            start_label: Label of the start vertex.
            end_label: Label of the end vertex.

        Returns:
            A tuple containing the distance and the path between the two vertices.

        Raises:
            VertexNotFoundError: If one or both vertices are not found.
            PathNotFound: If no path exists between the provided locations.
        """
        if not self.has_vertex(start_label) or not self.has_vertex(end_label):
            raise VertexNotFoundError("Cannot find one or both locations to perform dijkstra's algorithm")

        # Get the vertex objects from the labels
        start = self.find_vertex(start_label)
        end = self.find_vertex(end_label)

        # convert the linked list of vertices to a numpy array to use indexing
        vertices_list = np.empty(self.count, dtype=object)
        for i in range(self.count):
            vertices_list[i] = self.vertices[i].get_value()

        # Converting the numpy array to a list to use indexing - I know we're not meant to use in built ADTS, but need to use .index() from Python lists.
        # Java has .indexOf() for arrays, but numpy lacks this. The list is used the same way as an array.
        vertices_list = list(vertices_list)

        # Create a priority queue using MinHeap
        pq = MinHeap(self.count)

        # Create arrays to store the previous vertices and distances
        prev = np.empty(self.count, dtype=object)
        distances = np.empty(self.count, dtype=float)
        distances[:] = float("inf")
        distances[vertices_list.index(start)] = 0

        # Add start vertex to the priority queue with priority 0 (distance 0)
        pq.add(0, start)

        # While the priority queue is not empty
        while pq.get_count() > 0:
            # Remove the vertex with the highest priority (lowest distance)
            current_entry = pq.remove()
            # Unpack the current entry (tuple) into distance and vertex
            current_distance = current_entry.get_priority()
            vertex = current_entry.get_value()

            # If the vertex is the end vertex, break as the shortest path has been found
            if vertex == end:
                break

            # If the current distance is greater than the distance stored in the distances array, continue to the next iteration
            if current_distance > distances[vertices_list.index(vertex)]:
                continue

            # Iterate through the adjacent vertices of the current vertex
            for neighbour, weight in vertex.get_adjacent():
                alt = current_distance + weight

                if alt < distances[vertices_list.index(neighbour)]:
                    prev[vertices_list.index(neighbour)] = vertex
                    distances[vertices_list.index(neighbour)] = alt
                    pq.add(alt, neighbour)

        final_distance = distances[vertices_list.index(end)]
        if final_distance == float("inf"):
            raise PathNotFound("Path not found between provided locations.")
        return final_distance, self._reconstruct_path(prev, start, end, vertices_list)

    def _reconstruct_path(self, prev, start, end, vertices_list) -> list:
        """Reconstruct the path from the start to the end vertex.

        Args:
            prev: List of previous vertices in the path.
            start: The start vertex.
            end: The end vertex.
            vertices_list: List of all vertices in the graph.

        Returns:
            The reconstructed path from start to end.
        """
        path = []
        current = end
        while current:
            path.append(current)
            current = prev[vertices_list.index(current)]
        path.reverse()
        return path

    def is_path(self, start_label, end_label) -> bool:
        """Perform a breadth-first search of the graph and check if a path exists between two nodes.

        Args:
            start_label: Label of the start vertex.
            end_label: Label of the end vertex.

        Returns:
            True if a path exists, False otherwise.

        Raises:
            GraphEmptyError: If the graph is empty.
        """
        if self.count == 0:
            raise GraphEmptyError("Cannot perform BFS on empty graph.")
        q = Queue()  # The main queue for BFS

        # Clear the visited status of all vertices
        for vertex in self.vertices:
            vertex.get_value().clear_visited()

        v = self.find_vertex(start_label)  # Start from the first vertex
        end = self.find_vertex(end_label)
        v.set_visited()  # Mark it as visited
        q.enqueue(v)  # Enqueue the start vertex

        while not q.is_empty():
            v = q.dequeue()
            for w, _ in v.get_adjacent():
                if w == end:
                    return True
                if not w.get_visited():  # Only consider unvisited adjacent vertices
                    w.set_visited()  # Mark as visited before enqueueing
                    q.enqueue(w)
        return False


class VertexNotFoundError(Exception):
    """Exception raised when a vertex is not found in the graph."""
    pass


class EdgeToSameVertex(Exception):
    """Exception raised when attempting to add an edge from a vertex to itself."""
    pass


class EdgeExistsError(Exception):
    """Exception raised when an edge already exists or doesn't exist when expected."""
    pass


class VertexExistsError(Exception):
    """Exception raised when a vertex already exists in the graph."""
    pass


class GraphEmptyError(Exception):
    """Exception raised when attempting to perform operations on an empty graph."""
    pass


class PathNotFound(Exception):
    """Exception raised when a path between two vertices is not found."""
    pass


