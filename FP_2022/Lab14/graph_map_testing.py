import re

from Graph_map.graph import Graph
from Graph_map.bfs import BFS_complete
from Graph_map.dfs import DFS_complete
from Graph_map.topological_sort import topological_sort


def read_file(path, directed=False):
    """
    Reads from file and makes a graph
    """
    graph = Graph(directed)
    vertexes = {}
    regex = re.compile(r'^(\w+)\s+\((.+)\)$')

    with open(path, 'r') as input_file:
        for line in input_file.readlines()[1:]:
            line = line.replace('\n', '')
            origin, destinations = regex.findall(line)[0]
            destinations = destinations.split(', ')

            origin_obj = vertexes.get(origin)
            if origin_obj is None:
                origin_obj = graph.insert_vertex(origin)
                vertexes[origin] = origin_obj

            for destination in destinations:
                if destination == 'none':
                    continue

                destination_obj = vertexes.get(destination)
                if destination_obj is None:
                    destination_obj = graph.insert_vertex(destination)
                    vertexes[destination] = destination_obj

                graph.insert_edge(origin_obj, destination_obj)

    return graph


def test_fs(graph, func):
    """
    Tests bfs snd dfs, passed via func parameter
    """
    forest = func(graph)
    discovered_vertices = set()
    for vertex, edge in forest.items():
        discovered_vertices.add(vertex)
        if edge is not None:
            assert edge.endpoints()[0] in discovered_vertices


def test_topological_sort(graph):
    """
    Tests topological sort
    """
    sorted_list = topological_sort(graph)
    for edge in graph.edges():
        origin = edge.endpoints()[0]
        destination = edge.endpoints()[1]
        assert sorted_list.index(origin) < sorted_list.index(destination)


def main():
    """
    Main function
    """
    oriented_graph = read_file('stanford_cs.txt', True)
    test_fs(oriented_graph, BFS_complete)
    test_fs(oriented_graph, DFS_complete)
    test_topological_sort(oriented_graph)
    regular_graph = read_file('stanford_cs.txt', False)
    test_fs(regular_graph, BFS_complete)
    test_fs(regular_graph, DFS_complete)


if __name__ == '__main__':
    main()
