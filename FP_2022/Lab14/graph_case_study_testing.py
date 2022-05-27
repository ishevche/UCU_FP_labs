import re

from Graph_case_study.graph import LinkedDirectedGraph, LinkedEdge, LinkedVertex
from Graph_case_study.algorithms import dfs, topoSort
from Graph_case_study.linkedstack import LinkedStack


def read_file(path):
    """
    Reads from file and makes a graph
    """
    graph = LinkedDirectedGraph()
    regex = re.compile(r"^(\w+)\s+\((.+)\)$")
    with open(path, "r") as input_file:
        for line in input_file.readlines()[1:]:
            line = line.replace("\n", "")
            origin, destinations = regex.findall(line)[0]
            destinations = destinations.split(", ")
            if not graph.containsVertex(origin):
                graph.add(origin)

            for destination in destinations:
                if destination == "none":
                    continue
                if not graph.containsVertex(destination):
                    graph.add(destination)
                graph.addEdge(origin, destination, None)

    return graph


def test_dfs(graph, vertex, result):
    """
    Tests bfs snd dfs, passed via func parameter
    """
    graph.clearVertexMarks()
    stack = LinkedStack()
    dfs(graph, graph.getVertex(vertex), stack)
    assert list(map(str, stack)) == result, list(map(str, stack))


def test_topological_sort(graph):
    """
    Tests topological sort
    """
    sorted_list = list(iter(topoSort(graph)))
    for edge in graph.edges():
        destination = edge.getToVertex()
        origin = edge.getOtherVertex(destination)
        assert sorted_list.index(origin) > sorted_list.index(destination)


def main():
    """
    Main function
    """
    oriented_graph = read_file("stanford_cs.txt")
    test_topological_sort(oriented_graph)
    dfs_tests = {"MATH51": ["MATH19", "MATH20", "MATH21", "MATH51"],
                 "CS140": ["CS106A", "CS106B", "CS107", "CS110", "CS140"],
                 "ENGR40M": ["PHYS21", "PHYS23", "ENGR40M"],
                 "CS109": ["CS106A", "CS106B", "CS103", "CS109"]}
    for test_vertex, result in dfs_tests.items():
        test_dfs(oriented_graph, test_vertex, result)


if __name__ == "__main__":
    main()
