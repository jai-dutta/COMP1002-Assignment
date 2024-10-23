"""Graph.py

This file contains the Graph class, which represents a weighted, undirected graph.

DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
"""

from LinkedList import LinkedList
from MinHeap import *
from Queue import Queue


class GraphVertex:
    """A class to represent a vertex in the graph.

    Attributes:
        label: A string representing the label of the vertex.
        value: The value associated with the vertex.
        visited: A boolean indicating if the vertex has been visited.
        links: A LinkedList of adjacent vertices and their edge weights.
    """

    def __init__(self, label, value):
        """Initialize a GraphVertex object.

        Args:
            label: A string representing the label of the vertex.
            value: The value associated with the vertex.
        """
        self.label = label
        self.value = value
        self.visited = False
        self.links = LinkedList()

    def __str__(self):
        """Return a string representation of the vertex.

        Returns:
            A string representation of the vertex.
        """
        return f"{self.label}: {self.value}" if self.value else f"{self.label}"

    def get_label(self):
        """Get the label of the vertex.

        Returns:
            The label of the vertex.
        """
        return self.label

    def get_value(self):
        """Get the value of the vertex.

        Returns:
            The value of the vertex.
        """
        return self.value

    def get_adjacent(self):
        """Get the adjacent vertices and their edge weights.

        Returns:
            A list of tuples, each containing an adjacent vertex and its edge weight.
        """
        adjacent_vertices = [(node.get_value()[0], node.get_value()[1]) for node in self.links]
        return adjacent_vertices

    def set_adjacent(self, vertex: "GraphVertex", weight: float):
        """Set an adjacent vertex with its edge weight.

        Args:
            vertex: The adjacent GraphVertex object.
            weight: The weight of the edge connecting to the adjacent vertex.
        """
        inserted = False
        for i in range(len(self.links)):
            current_vertex, current_weight = self.links[i].get_value()
            if vertex.get_label() < current_vertex.get_label():
                self.links.insert_before((vertex, weight), i)
                inserted = True
                break

        if not inserted:
            self.links.insert_last((vertex, weight))  # If not inserted, add to the end

    def remove_adjacent(self, vertex: "GraphVertex"):
        """Remove an adjacent vertex.

        Args:
            vertex: The GraphVertex object to be removed from adjacency list.
        """
        for i in range(len(self.links)):
            if self.links[i].get_value()[0] == vertex:
                self.links.remove_at(i)
                break

    def set_visited(self):
        """Mark the vertex as visited."""
        self.visited = True

    def clear_visited(self):
        """Clear the visited status of the vertex."""
        self.visited = False

    def get_visited(self):
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

    def add_vertex(self, label, value=0) -> None:
        """Add a vertex to the graph. Maintains sorted order.

        Args:
            label: Label of the vertex.
            value: Value of the vertex. Defaults to 0.

        Raises:
            VertexExistsError: If a vertex with the given label already exists.
        """
        if self._find_vertex(label):
            raise VertexExistsError("Duplicate location found.")

        new_vertex = GraphVertex(label, value)

        if self.vertices.is_empty():
            self.vertices.insert_last(new_vertex)
        else:
            inserted = False
            for i in range(len(self.vertices)):
                if label < self.vertices[i].get_value().get_label():
                    self.vertices.insert_before(new_vertex, i)
                    inserted = True
                    break

            if not inserted:
                self.vertices.insert_last(new_vertex)  # If not inserted, add to the end

        self.count += 1

    def delete_vertex(self, label) -> None:
        """Delete a vertex from the graph.

        Args:
            label: Label of the vertex to delete.

        Raises:
            VertexNotFoundError: If the vertex to delete is not found.
        """
        index = self._find_vertex_index(label)
        if index is None:
            raise VertexNotFoundError("Vertex to delete not found!")
        self.vertices.remove_at(index)
        self.count -= 1

    def add_edge(self, label1, label2, weight: float) -> None:
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
        if self.is_adjacent(label1, label2):
            raise EdgeExistsError("Road exists. Cannot add multiple roads in a simple graph.")

        vertex1 = self._find_vertex(label1)
        vertex2 = self._find_vertex(label2)
        if vertex1 and vertex2:
            if vertex1 != vertex2:
                vertex1.set_adjacent(vertex2, weight)
                vertex2.set_adjacent(vertex1, weight)
            else:
                raise EdgeToSameVertex("Cannot add road from location to itself.")
        else:
            raise VertexNotFoundError("Cannot find one or both locations to add road.")

    def delete_edge(self, label1, label2) -> None:
        """Delete an edge between two vertices.

        Args:
            label1: Label of the first vertex.
            label2: Label of the second vertex.

        Raises:
            EdgeExistsError: If the edge to delete does not exist.
            EdgeToSameVertex: If attempting to remove an edge from a vertex to itself.
        """
        if not self.is_adjacent(label1, label2):
            raise EdgeExistsError("Road to delete does not exist.")

        vertex1 = self._find_vertex(label1)
        vertex2 = self._find_vertex(label2)
        if vertex1 and vertex2:
            if vertex1 != vertex2:
                vertex1.remove_adjacent(vertex2)
                vertex2.remove_adjacent(vertex1)
            else:
                raise EdgeToSameVertex("Cannot remove road from location to itself.")

    def has_vertex(self, label) -> bool:
        """Check if a vertex exists.

        Args:
            label: Label of vertex to check.

        Returns:
            True if the vertex exists, False otherwise.
        """
        return True if self._find_vertex(label) else False

    def get_vertex_count(self) -> int:
        """Get the vertex count.

        Returns:
            The number of vertices in the graph.
        """
        return self.count

    def get_adjacent(self, label) -> GraphVertex | None:
        """Get adjacent vertices to specified vertex.

        Args:
            label: Label for the vertex whose adjacent vertices are to be retrieved.

        Returns:
            A list of adjacent vertices.

        Raises:
            VertexNotFoundError: If the specified vertex is not found.
        """
        vertex = self._find_vertex(label)
        if vertex:
            return vertex.get_adjacent()
        else:
            raise VertexNotFoundError("Location not found.")

    def is_adjacent(self, label1, label2) -> bool:
        """Check if two vertices are adjacent.

        Args:
            label1: Label of the first vertex to check.
            label2: Label of the second vertex to check.

        Returns:
            True if the vertices are adjacent, False otherwise.
        """
        vertex1 = self._find_vertex(label1)
        vertex2 = self._find_vertex(label2)
        if vertex1 and vertex2:
            for vertex, _ in vertex1.get_adjacent():
                if vertex2 == vertex:
                    return True
        return False

    def display_as_list(self) -> None:
        """Display the graph as an adjacency list."""
        for vertex in self.vertices:
            print(f"{vertex.get_value()} ", end="")
            if vertex.get_value().get_adjacent():
                for count, (adjacent_vertex, weight) in enumerate(vertex.get_value().get_adjacent()):
                    print(
                        f"{f'- {weight} > {adjacent_vertex} ' if count + 1 < len(vertex.get_value().get_adjacent()) else f'- {weight} > {adjacent_vertex} '} ",
                        end="")
            print()

    def display_as_matrix(self):
        """Display the graph as an adjacency matrix."""
        matrix = [[0] * self.count for _ in range(self.count)]

        for row in range(len(matrix)):
            for col in range(len(matrix)):
                if self.is_adjacent(self.vertices[row].get_value().get_label(),
                                    self.vertices[col].get_value().get_label()):
                    matrix[row][col] = 1

        print()
        print("\t", end="")
        for i in self.vertices:
            print(i.get_value().get_label(), end="\t")
        print()

        for row in range(len(matrix)):
            print(self.vertices[row].get_value().get_label(), end="\t")
            for col in range(len(matrix)):
                print(matrix[row][col], end="\t")
            print()

    def _find_vertex(self, label):
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

    def _find_vertex_index(self, label):
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

        start = self._find_vertex(start_label)
        end = self._find_vertex(end_label)

        # convert the linked list of vertices to a python list/arr to use indexing
        vertices_list = [node.get_value() for node in self.vertices]

        pq = MinHeap(self.count)

        prev = [None] * self.count
        distances = [float("inf")] * self.count
        distances[vertices_list.index(start)] = 0

        pq.add(0, start)

        while pq.get_count() > 0:
            current_entry = pq.remove()
            current_distance = current_entry.get_priority()
            vertex = current_entry.get_value()

            if vertex == end:
                break

            if current_distance > distances[vertices_list.index(vertex)]:
                continue

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

    def _reconstruct_path(self, prev, start, end, vertices_list):
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

        v = self._find_vertex(start_label)  # Start from the first vertex
        end = self._find_vertex(end_label)
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
