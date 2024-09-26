from django.db import models


# Define your models here.


class GraphModel:
    # ------------------------- Nested Class Vertex -------------------------
    class Node:
        """ A structure representing a node in the graph. """

        def __init__(self, identifier, label=None, properties=None, connections=None):
            self._identifier = identifier
            self._label = label
            self._properties = {} if properties is None else properties
            self._connections = [] if connections is None else connections

        @property
        def identifier(self):
            return self._identifier

        @property
        def label(self):
            return self._label

        @property
        def properties(self):
            return self._properties

        @property
        def connections(self):
            return self._connections

        @connections.setter
        def connections(self, value):
            self._connections = [] if value is None else value

        def __hash__(self):
            return hash(id(self))

        def __str__(self):
            return str(self._identifier)

        def add_property(self, key, value):
            self._properties[key] = value

        def add_connection(self, node):
            self._connections.append(node)

    # ------------------------- Nested Class Edge -------------------------
    class Link:
        """ A structure representing an edge in the graph. """
        __slots__ = '_start', '_end', '_data'

        def __init__(self, start, end, data):
            self._start = start
            self._end = end
            self._data = data

        def endpoints(self):
            """ Returns a tuple (u,v) for nodes u and v. """
            return (self._start, self._end)

        def opposite(self, node):
            """ Returns the node on the opposite side of node in this edge. """
            if not isinstance(node, GraphModel.Node):
                raise TypeError('Node must be an instance of Node class')
            if self._end == node:
                return self._start
            elif self._start == node:
                return self._end
            raise ValueError('Node is not part of the edge')

        @property
        def data(self):
            """ Returns the data associated with the edge. """
            return self._data

        def __hash__(self):
            return hash((self._start, self._end))

        def __str__(self):
            return '({0},{1},{2})'.format(self._start, self._end, self._data)

    # ------------------------- GraphModel Methods -------------------------
    def __init__(self, is_directed=False):
        """ Creates an empty graph (default is undirected). """
        self._outgoing_links = {}
        self._incoming_links = {} if is_directed else self._outgoing_links
        self._root_node = None

    @property
    def root_node(self):
        return self._root_node

    def _validate_node(self, node):
        """ Validates if node is part of this graph. """
        if not isinstance(node, self.Node):
            raise TypeError('Expected an instance of Node')
        if node not in self._outgoing_links:
            raise ValueError('Node does not belong to this graph.')

    def is_directed_graph(self):
        """ Returns True if the graph is directed; False if undirected. """
        return self._incoming_links is not self._outgoing_links

    def node_count(self):
        """ Returns the number of nodes in the graph. """
        return len(self._outgoing_links)

    def nodes(self):
        """ Returns an iterator over all nodes in the graph. """
        return self._outgoing_links.keys()

    def link_count(self):
        """ Returns the number of edges in the graph. """
        total_links = sum(len(self._outgoing_links[n]) for n in self._outgoing_links)
        return total_links if self.is_directed_graph() else total_links // 2

    def links(self):
        """ Returns a set of all edges in the graph. """
        result = set()
        for secondary_map in self._outgoing_links.values():
            result.update(secondary_map.values())
        return result

    def find_link(self, u, v):
        """ Returns the edge between nodes u and v or None if they are not adjacent. """
        self._validate_node(u)
        self._validate_node(v)
        return self._outgoing_links[u].get(v)

    def degree_of_node(self, node, outgoing=True):
        """ Returns the degree of a node - number of (outgoing) edges from node in the graph. """
        self._validate_node(node)
        adjacency_map = self._outgoing_links if outgoing else self._incoming_links
        return len(adjacency_map[node])

    def incident_links(self, node, outgoing=True):
        """ Returns all (outgoing) edges from node in the graph. """
        self._validate_node(node)
        adjacency_map = self._outgoing_links if outgoing else self._incoming_links
        for edge in adjacency_map[node].values():
            yield edge

    def incident_nodes(self, node, outgoing=True):
        """ Returns all outgoing nodes from node in the graph. """
        self._validate_node(node)
        adjacency_map = self._outgoing_links if outgoing else self._incoming_links
        for edge in adjacency_map[node].values():
            yield edge.opposite(node)

    def get_connected_nodes(self, node, outgoing=True):
        result = {}
        self._validate_node(node)
        adjacency_map = self._outgoing_links if outgoing else self._incoming_links
        for edge in adjacency_map[node].values():
            neighbor = edge.opposite(node)
            result[neighbor.identifier] = neighbor
        return result

    def get_node_by_identifier(self, identifier):
        """ Returns node with the given identifier if exists, otherwise None. """
        for node in self.nodes():
            if node.identifier == identifier:
                return node
        return None

    def add_new_node(self, identifier, label=None, properties=None):
        """ Inserts and returns a new node (Node). """
        if self.get_node_by_identifier(identifier) is not None:
            raise ValueError('Node with this identifier already exists.')
        new_node = self.Node(identifier, label, properties)
        self._outgoing_links[new_node] = {}
        if self.is_directed_graph():
            self._incoming_links[new_node] = {}
        return new_node

    def add_existing_node(self, node):
        """ Inserts and returns a node (Node). """
        if self.get_node_by_identifier(node.identifier) is not None:
            raise ValueError('Node with this identifier already exists.')
        self._outgoing_links[node] = {}
        if self.is_directed_graph():
            self._incoming_links[node] = {}
        return node

    def add_edge(self, u, v, data=None):
        """ Inserts and returns a new edge (Link) from u to v with auxiliary data. """
        if self.find_link(u, v) is not None:
            raise ValueError('u and v are already adjacent')
        new_edge = self.Link(u, v, data)
        self._outgoing_links[u][v] = new_edge
        self._incoming_links[v][u] = new_edge
        if not self.is_directed_graph():
            self.get_node_by_identifier(u.identifier).add_connection(v)
            self.get_node_by_identifier(v.identifier).add_connection(u)
        else:
            self.get_node_by_identifier(u.identifier).add_connection(v)

    def is_tree_structure(self):
        """ Checks if the graph is a tree (undirected and acyclic graph). """
        if self.is_directed_graph() or self.__contains_cycle_in_undirected_graph():
            return False
        return True

    def has_cycle(self):
        return self.__contains_cycle_in_undirected_graph()

    def __dfs_cycle_check(self, current_node, parent_node, visited_nodes):
        """ Auxiliary method to check if the graph contains a cycle. """
        visited_nodes[current_node] = True
        for adjacent_node in self.incident_nodes(current_node):
            if not visited_nodes[adjacent_node]:
                if self.__dfs_cycle_check(adjacent_node, current_node, visited_nodes):
                    return True
            elif parent_node is not None and adjacent_node.identifier != parent_node.identifier:
                return True
        return False

    def __contains_cycle_in_undirected_graph(self):
        """ Method checks if the graph is cyclic. """
        visited_nodes = {node: False for node in self.nodes()}
        for node in self.nodes():
            if not visited_nodes[node]:
                if self.__dfs_cycle_check(node, None, visited_nodes):
                    return True
        return False

    def display_graph(self):
        print("OUTGOING LINKS")
        for key, value in self._outgoing_links.items():
            print('--------')
            print(key)
            for i, j in value.items():
                print('{} : {}'.format(i, j))
            print('--------')

        print("INCOMING LINKS")
        for key, value in self._incoming_links.items():
            print('--------')
            print(key)
            for i, j in value.items():
                print('{} : {}'.format(i, j))
            print('--------')

    def collect_root_nodes(self):
        root_nodes = []
        if self._root_node is not None:
            root_nodes.append(self._root_node)
        else:
            visited = []
            for node in self.nodes():
                if node not in visited:
                    visited.append(node)
                    root_nodes.append(node)
                    for child in node.connections:
                        visited.append(child)
        return root_nodes
