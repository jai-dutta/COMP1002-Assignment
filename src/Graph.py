from operator import index
from Queue import Queue
from Stack import Stack
from LinkedList import LinkedList
from Heap import *


class GraphVertex:
    def __init__(self, label, value):
        self.label = label
        self.value = value
        self.visited = False
        self.links = LinkedList()

    def __str__(self):
        return f"{self.label}: {self.value}"

    def get_label(self):
        return self.label

    def get_value(self):
        return self.value

    def get_adjacent(self):
        adjacent_vertices = [(node.get_value()[0], node.get_value()[1]) for node in self.links]
        return adjacent_vertices

    def set_adjacent(self, vertex: "GraphVertex", weight: float):
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
        for i in range(len(self.links)):
            if self.links[i].get_value()[0] == vertex:
                self.links.remove_at(i)
                break

    def set_visited(self):
        self.visited = True

    def clear_visited(self):
        self.visited = False

    def get_visited(self):
        return self.visited


class Graph:
    """
    A class to represent an undirected, weighted simple graph.

    Attributes:
        vertices : A LinkedList, containing each vertex of the graph.
        count : a count of vertices in the graph.
    """

    def __init__(self):
        # Initialise linked list to contain vertices
        self.vertices = LinkedList()
        self.count = 0

    def add_vertex(self, label, value) -> None:
        """
        Adds a vertex to the graph. Maintains sorted order.
        :param label: Label of the vertex
        :param value: Value of the vertex
        """
        if self._find_vertex(label):
            raise VertexExistsError("Duplicate vertex found")

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
        """
        Deletes a vertex from the graph.
        :param label: label of the vertex to delete
        """
        index = self._find_vertex_index(label)
        if index is None:
            raise VertexNotFoundError("Vertex to delete not found!")
        self.vertices.remove_at(index)
        self.count -= 1

    def add_edge(self, label1, label2, weight: float) -> None:
        """
        Adds an edge between two vertices.
        :param label1: label of the first vertex
        :param label2: label of the second vertex
        :param weight: weight of the edge
        """
        if self.is_adjacent(label1, label2):
            raise EdgeExistsError("Edge exists. Cannot add multiple edges in a simple graph.")

        vertex1 = self._find_vertex(label1)
        vertex2 = self._find_vertex(label2)
        if vertex1 and vertex2:
            if vertex1 != vertex2:
                vertex1.set_adjacent(vertex2, weight)
                vertex2.set_adjacent(vertex1, weight)
            else:
                raise EdgeToSameVertex("Cannot add edge from vertex to itself.")

    def delete_edge(self, label1, label2) -> None:
        """
        Deletes an edge between two vertices.
        :param label1: label of the first vertex
        :param label2: label of the second vertex
        """
        if not self.is_adjacent(label1, label2):
            raise EdgeExistsError("Edge to delete does not exist.")

        vertex1 = self._find_vertex(label1)
        vertex2 = self._find_vertex(label2)
        if vertex1 and vertex2:
            if vertex1 != vertex2:
                vertex1.remove_adjacent(vertex2)
                vertex2.remove_adjacent(vertex1)
            else:
                raise EdgeToSameVertex("Cannot remove edge from vertex to itself.")

    def has_vertex(self, label) -> bool:
        """
        Checks if a vertex exists.
        :param label: Label of vertex to check.
        """
        return True if self._find_vertex(label) else False

    def get_vertex_count(self) -> int:
        """
        Returns vertex count
        """
        return self.count

    def get_adjacent(self, label) -> GraphVertex | None:
        """
        Returns adjacent vertices to specified vertex.
        :param label: label for the vertex whose adjacent vertices are to be retrieved.
        """
        vertex = self._find_vertex(label)
        if vertex:
            return vertex.get_adjacent()
        else:
            raise VertexNotFoundError("Vertex not found.")

    def is_adjacent(self, label1, label2) -> bool:
        """
        Checks two vertices and returns if they are adjacent.
        :param label1: label of the first vertex to check
        :param label2: label of the second vertex to check.
        """
        vertex1 = self._find_vertex(label1)
        vertex2 = self._find_vertex(label2)
        if vertex1 and vertex2:
            for vertex, _ in vertex1.get_adjacent():
                if vertex2 == vertex:
                    return True
        return False

    def display_as_list(self) -> None:
        """
        Displays the graph as an adjacency list.
        """
        for vertex in self.vertices:
            print(f"{vertex.get_value()} {'->' if vertex.get_value().get_adjacent() else ''} ", end="")
            if vertex.get_value().get_adjacent():
                for count, (adjacent_vertex, weight) in enumerate(vertex.get_value().get_adjacent()):
                    print(f"{adjacent_vertex} {'->' if count + 1 < len(vertex.get_value().get_adjacent()) else ''} ",
                          end="")
            print()

    def display_as_matrix(self):
        """
        Displays the graph as an adjacency matrix.
        """
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
        """
        Helper function to find vertex given a label within the graph.
        :param label:
        """
        for vertex in self.vertices:
            if vertex.get_value().get_label() == label:
                return vertex.get_value()
        return None

    def _find_vertex_index(self, label):
        """
        Helper function to find the index of a vertex using its label.
        Used in delete_vertex
        :param label: label of the vertex to find
        :return: index of the vertex
        """
        for i in range(len(self.vertices)):
            if self.vertices[i].get_value().get_label() == label:
                return i

    def dijkstra(self, start_label: str, end_label: str) -> tuple[float, list]:
        """
        Finds the shortest path between two vertices using dijkstra's algorithm.
        :param start_label: label of the start vertex
        :param end_label: label of the end vertex
        :return: tuple containing the distance and the path between the two vertices
        """
        if self.count == 0:
            raise GraphEmptyError("Cannot perform dijkstra's algorithm on empty graph.")
        if not self.has_vertex(start_label) or not self.has_vertex(end_label):
            raise VertexNotFoundError("Cannot find one or both vertices to perform dijkstra's algorithm")

        start = self._find_vertex(start_label)
        end = self._find_vertex(end_label)

        # convert the linked list of vertices to a python list/arr to use indexing
        vertices_list = [node.get_value() for node in self.vertices]

        pq = Heap(self.count)

        prev = [None] * self.count
        distances = [float("inf")] * self.count
        distances[vertices_list.index(start)] = 0

        pq.add(0, start)

        found = False

        while pq.get_count() > 0 and not found:
            vertex = pq.remove().get_value()

            for neighbour, weight in vertex.get_adjacent():
                if neighbour == end:
                    found = True
                alt = distances[vertices_list.index(vertex)] + weight

                if alt < distances[vertices_list.index(neighbour)]:
                    prev[vertices_list.index(neighbour)] = vertex
                    distances[vertices_list.index(neighbour)] = alt
                    pq.add(alt, neighbour)

        if found:
            final_distance = distances[vertices_list.index(end)]
            return final_distance, self._reconstruct_path(prev, start, end, vertices_list)
        else:
            raise PathNotFoundError("Path not found between provided vertices.")

    def _reconstruct_path(self, prev, start, end, vertices_list):
        """
        Reconstructs the path from the start to the end vertex.
        Helper function for dijkstra's algorithm.
        """
        path = []
        current = end
        while current:
            path.append(current)
            current = prev[vertices_list.index(current)]
        path.reverse()
        return path

    def is_path(self, start_label, end_label) -> bool:
        """
        Checks if there is a path between two vertices using dijkstra's algorithm.

        Note: I know we were instructed to use BFS or DFS for this, but I have implemented Dijkstra's algorithm
        to find the shortest path between two vertices, so I thought it would be more efficient to use it here.

        :param start_label: label of the start vertex
        :param end_label: label of the end vertex
        :return: True if there is a path, False otherwise
        """
        if not self.has_vertex(start_label) or not self.has_vertex(end_label):
            raise VertexNotFoundError("Cannot find one or both vertices to check for path.")
        start = self._find_vertex(start_label)
        end = self._find_vertex(end_label)

        return self.dijkstra(start_label, end_label)[0] is not None


class VertexNotFoundError(Exception):
    pass


class EdgeToSameVertex(Exception):
    pass


class EdgeExistsError(Exception):
    pass

class VertexExistsError(Exception):
    pass

class GraphEmptyError(Exception):
    pass

class PathNotFoundError(Exception):
    pass

