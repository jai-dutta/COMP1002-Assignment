
from Queue import Queue
from Stack import Stack
from LinkedList import LinkedList


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
        adjacent_vertices = [vertex.get_value() for vertex in self.links]
        return adjacent_vertices

    def set_adjacent(self, vertex: "GraphVertex"):
        inserted = False
        for i in range(len(self.links)):
            if vertex.get_label() < self.links[i].get_value().get_label():
                self.links.insert_before(vertex, i)
                inserted = True
                break

        if not inserted:
            self.links.insert_last(vertex)  # If not inserted, add to the end



    def remove_adjacent(self, vertex: "GraphVertex"):
        for i in range(len(self.links)):
            if self.links[i].get_value() is vertex:
                self.links.remove_at(i)

    def set_visited(self):
        self.visited = True

    def clear_visited(self):
        self.visited = False

    def get_visited(self):
        return self.visited


class Graph:
    """
    A class to represent an undirected simple graph.

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
        print(f"Adding vertex: {label}")
        if self._find_vertex(label):
            raise VertexExistsError("Duplicate vertex found")

        new_vertex = GraphVertex(label, value)

        if self.vertices.is_empty():
            self.vertices.insert_last(new_vertex)
        else:
            inserted = False
            for i in range(len(self.vertices)):
                print(f"Comparing with: {self.vertices[i].get_value().get_label()}")
                if label < self.vertices[i].get_value().get_label():
                    self.vertices.insert_before(new_vertex, i)
                    print(f"Inserted {label} before {self.vertices[i].get_value().get_label()}")
                    inserted = True
                    break

            if not inserted:
                print(f"Inserted {label} at the end.")
                self.vertices.insert_last(new_vertex)  # If not inserted, add to the end

        self.count += 1

    def delete_vertex(self, label):
        index = self._find_vertex_index(label)
        if index is None:
            raise VertexNotFoundError("Vertex to delete not found!")
        self.vertices.remove_at(index)
        self.count -= 1


    def add_edge(self, label1, label2) -> None:
        """
        Adds an edge between two vertices.
        :param label1: label of the first vertex
        :param label2: label of the second vertex
        """
        if self.is_adjacent(label1, label2):
            raise EdgeExistsError("Edge exists. Cannot add multiple edges in a simple graph.")

        vertex1 = self._find_vertex(label1)
        vertex2 = self._find_vertex(label2)
        if vertex1 and vertex2:
            if vertex1 != vertex2:
                vertex1.set_adjacent(vertex2)
                vertex2.set_adjacent(vertex1)
            else:
                raise EdgeToSameVertex("Cannot add edge from vertex to itself.")

    def delete_edge(self, label1, label2):
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
            return vertex2 in vertex1.get_adjacent()
        raise VertexNotFoundError("Vertex not found.")

    def display_as_list(self) -> None:
        """
        Displays the graph as an adjacency list.
        """
        for vertex in self.vertices:
            print(f"{vertex.get_value()} {'->' if vertex.get_value().get_adjacent() else ''} ", end="")
            if vertex.get_value().get_adjacent():
                for count, adjacent_vertex in enumerate(vertex.get_value().get_adjacent()):
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
        for i in range(len(self.vertices)):
            if self.vertices[i].get_value().get_label() == label:
                return i

    def bfs(self):
        """
        Performs a bread-first search of the graph and prints the results.
        """
        if self.count == 0:
            raise GraphEmptyError("Cannot perform BFS on empty graph.")
        q = Queue()  # The main queue for BFS
        t = Queue()

        # Clear the visited status of all vertices
        for vertex in self.vertices:
            vertex.get_value().clear_visited()

        v = self.vertices[0].get_value()  # Start from the first vertex
        v.set_visited()  # Mark it as visited
        q.enqueue(v)  # Enqueue the start vertex

        while not q.is_empty():
            v = q.dequeue()

            for w in v.get_adjacent():
                if not w.get_visited():  # Only consider unvisited adjacent vertices
                    w.set_visited()  # Mark as visited before enqueueing
                    q.enqueue(w) 
                    t.enqueue(v)
                    t.enqueue(w)
            print(v)

    def dfs(self):
        """
        Performs a depth-first search of the graph and prints the results.
        """
        if self.count == 0:
            raise GraphEmptyError("Cannot perform DFS on empty graph.")
        s = Stack()  # Stack.py to hold vertices for DFS
        for vertex in self.vertices:
            vertex.get_value().clear_visited()  # Clear visited flag for all vertices

        v = self.vertices[0].get_value()  # Start from the first vertex
        v.set_visited()  # Mark the first vertex as visited
        s.push(v)  # Push the first vertex onto the stack
        print(v)
        while not s.is_empty():
            v = s.top()  # Get the top vertex without popping it
            w = v.get_adjacent()  # Get all adjacent vertices

            # Flag to track if we have an unvisited neighbor
            found_unvisited = False

            for neighbour in w:
                if not neighbour.get_visited():  # If the neighbor is not visited
                    neighbour.set_visited()  # Mark it as visited
                    s.push(neighbour)  # Push the neighbor onto the stack
                    print(neighbour) # Print the node as it is visited
                    found_unvisited = True  # Indicate that we found an unvisited neighbor
                    break  # Break to process the next neighbor

            if not found_unvisited:
                s.pop()  # Pop the vertex if no unvisited neighbors were found


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