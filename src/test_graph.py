import pytest
from Graph import Graph, VertexNotFoundError, EdgeToSameVertex, EdgeExistsError, VertexExistsError, GraphEmptyError

@pytest.fixture
def empty_graph():
    return Graph()

@pytest.fixture
def sample_graph():
    g = Graph()
    g.add_vertex('A', 1)
    g.add_vertex('B', 2)
    g.add_vertex('C', 3)
    g.add_edge('A', 'B', 1.0)
    g.add_edge('B', 'C', 2.0)
    return g

def test_add_vertex(empty_graph):
    empty_graph.add_vertex('A', 1)
    assert empty_graph.has_vertex('A')
    assert empty_graph.get_vertex_count() == 1

def test_add_duplicate_vertex(empty_graph):
    empty_graph.add_vertex('A', 1)
    with pytest.raises(VertexExistsError):
        empty_graph.add_vertex('A', 2)

def test_delete_vertex(sample_graph):
    sample_graph.delete_vertex('B')
    assert not sample_graph.has_vertex('B')
    assert sample_graph.get_vertex_count() == 2

def test_delete_nonexistent_vertex(sample_graph):
    with pytest.raises(VertexNotFoundError):
        sample_graph.delete_vertex('D')

def test_add_edge(sample_graph):
    sample_graph.add_edge('A', 'C', 3.0)
    assert sample_graph.is_adjacent('A', 'C')

def test_add_duplicate_edge(sample_graph):
    with pytest.raises(EdgeExistsError):
        sample_graph.add_edge('A', 'B', 2.0)

def test_add_edge_to_same_vertex(sample_graph):
    with pytest.raises(EdgeToSameVertex):
        sample_graph.add_edge('A', 'A', 1.0)

def test_delete_edge(sample_graph):
    sample_graph.delete_edge('A', 'B')
    assert not sample_graph.is_adjacent('A', 'B')

def test_delete_nonexistent_edge(sample_graph):
    with pytest.raises(EdgeExistsError):
        sample_graph.delete_edge('A', 'C')

def test_get_adjacent_nonexistent_vertex(sample_graph):
    with pytest.raises(VertexNotFoundError):
        sample_graph.get_adjacent('D')

def test_is_adjacent(sample_graph):
    assert sample_graph.is_adjacent('A', 'B')
    assert not sample_graph.is_adjacent('A', 'C')

def test_dijkstra(sample_graph):
    weight, path = sample_graph.dijkstra('A', 'C')
    assert weight == 3.0
    for vertice in path:
        assert vertice.get_label() in ['A', 'B', 'C']

def test_display_as_list(sample_graph, capsys):
    sample_graph.display_as_list()
    captured = capsys.readouterr()
    assert "A: 1 -> B: 2" in captured.out
    assert "B: 2 -> A: 1 -> C: 3" in captured.out
    assert "C: 3 -> B: 2" in captured.out

def test_display_as_matrix(sample_graph, capsys):
    sample_graph.display_as_matrix()
    captured = capsys.readouterr()
    expected_output = """
	A	B	C	
A	0	1	0	
B	1	0	1	
C	0	1	0	
"""
    assert expected_output.strip() in captured.out.strip()

if __name__ == '__main__':
    pytest.main()
