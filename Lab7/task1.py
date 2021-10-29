"""
Complete all of the following functions. Currently they all just
'pass' rather than explicitly return value, which means that they
implicitly return None.
"""


def get_graph_from_file(file_name):
    """
    (str) -> (list)

    Read graph from file and return a list of edges.

    >>> get_graph_from_file("data1.txt")
    [[1, 2], [3, 4], [1, 5]]
    """
    with open(file_name) as input_file:
        ans = []
        for edge in input_file:
            from_node, to_edge = edge.split(',')
            ans += [[int(from_node), int(to_edge)]]
    return ans


def to_edge_dict(edge_list):
    """
    (list) -> (dict)

    Convert a graph from list of edges to dictionary of vertices.

    >>> to_edge_dict([[1, 2], [3, 4], [1, 5], [2, 4]])
    {1: [2, 5], 2: [1, 4], 3: [4], 4: [3, 2], 5: [1]}
    """
    ans = {}
    for edge in edge_list:
        add_edge(ans, edge)
    return ans


def is_edge_in_graph(graph, edge):
    """
    (dict, tuple) -> bool

    Return True if graph contains a given edge and False otherwise.

    >>> is_edge_in_graph({1: [2, 5], 2: [1, 4], 3: [4], 4: [2, 3], 5: [1]}, \
    (3, 1))
    False
    """
    return graph.get(edge[0], []).__contains__(edge[1])


def add_edge(graph, edge):
    """
    (dict, tuple) -> dict

    Add a new edge to the graph and return new graph.

    >>> add_edge({1: [2, 5], 2: [1, 4], 3: [4], 4: [2, 3], 5: [1]}, (1, 3))
    {1: [2, 5, 3], 2: [1, 4], 3: [4, 1], 4: [2, 3], 5: [1]}
    """
    graph[edge[0]] = graph.get(edge[0], []) + [edge[1]]
    graph[edge[1]] = graph.get(edge[1], []) + [edge[0]]
    return graph


def del_edge(graph, edge):
    """
    (dict, tuple) -> (dict)

    Delete an edge from the graph and return a new graph.

    >>> del_edge({1: [2, 5], 2: [1, 4], 3: [4], 4: [2, 3], 5: [1]}, (2, 4))
    {1: [2, 5], 2: [1], 3: [4], 4: [3], 5: [1]}
    """
    if graph.__contains__(edge[0]) and \
            graph[edge[0]].__contains__(edge[1]):
        graph[edge[0]].remove(edge[1])
    if graph.__contains__(edge[1]) and \
            graph[edge[1]].__contains__(edge[0]):
        graph[edge[1]].remove(edge[0])
    return graph


def add_node(graph, node):
    """
    (dict, int) -> (dict)

    Add a new node to the graph and return a new graph.

    >>> add_node({1: [2], 2: [1]}, 3)
    {1: [2], 2: [1], 3: []}
    """
    if not graph.__contains__(node):
        graph[node] = []
    return graph


def del_node(graph, node):
    """
    (dict, int) -> (dict)

    Delete a node and all incident edges from the graph.

    >>> del_node({1: [2, 5], 2: [1, 4], 3: [4], 4: [2, 3], 5: [1]}, 4)
    {1: [2, 5], 2: [1], 3: [], 5: [1]}
    """
    for destinations in graph.values():
        while destinations.__contains__(node):
            destinations.remove(node)
    if graph.__contains__(node):
        graph.pop(node)
    return graph


# def convert_to_dot(graph):
#     """
#     (dict) -> (None)
#
#     Save the graph to a file in a DOT format.
#     """
#     pass
