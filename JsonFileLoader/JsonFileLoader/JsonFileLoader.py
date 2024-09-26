from core.models import Graph
from core.services.services import DataLoader
import json
import re
from dateutil.parser import parse
from datetime import datetime


class JsonFileLoader(DataLoader):

    def __init__(self):
        self._id_counter = 0
        self._vertices_map = {}
        self._id_matcher = re.compile(r"(id|get_identifier)[0-9]?")
        self._doc_id_to_internal_id = {}
        self._explicit_links = {}
        self._inferred_links = {}
        self._graph_structure = Graph(True)

    def _next_id(self):
        self._id_counter += 1
        return self._id_counter

    def _reset_loader(self):
        self._id_counter = 0
        self._vertices_map = {}
        self._doc_id_to_internal_id = {}
        self._explicit_links = {}
        self._inferred_links = {}
        self._graph_structure = Graph(True)

    def load_data(self, filepath) -> Graph:
        if not filepath.endswith(".json"):
            return Graph()
        try:
            with open("test_data/" + filepath) as json_file:
                self._reset_loader()
                data_content = json.load(json_file)
                self._process_element(data_content)
                self._link_nodes()
                return self._graph_structure
        except Exception:
            return Graph()

    def _link_nodes(self):
        self._link_explicit_nodes()
        self._link_inferred_nodes()

    def _link_explicit_nodes(self):
        for node_id, neighbors in self._explicit_links.items():
            for neighbor in neighbors:
                src = self._vertices_map[node_id]
                dest = self._vertices_map[neighbor]
                if self._graph_structure.get_edge(src, dest) is None:
                    self._graph_structure.insert_edge(src, dest)

    def _link_inferred_nodes(self):
        for node_id, neighbors in self._inferred_links.items():
            for neighbor in neighbors:
                src = self._vertices_map[node_id]
                if neighbor in self._doc_id_to_internal_id:
                    dest = self._vertices_map[self._doc_id_to_internal_id[neighbor]]
                else:
                    dest_id = self._next_id()
                    dest = self._create_vertex(dest_id)
                    self._add_property_to_vertex(dest, "value", neighbor)
                if self._graph_structure.get_edge(src, dest) is None:
                    self._graph_structure.insert_edge(src, dest)

    def _process_element(self, element, parent=None, element_id=None):
        if isinstance(element, dict):
            self._process_dict_element(element, parent, element_id)
        elif isinstance(element, list):
            self._process_list_element(element, parent)
        else:
            self._process_single_value_element(element)

    def _process_dict_element(self, element, parent=None, element_id=None):
        if all(isinstance(value, dict) for value in element.values()):
            for key, value in element.items():
                self._process_element(value, parent, key)
        else:
            node_id = self._next_id()
            if element_id:
                self._doc_id_to_internal_id[element_id] = node_id
            else:
                self._map_known_id_to_generated(element, node_id)

            vertex = self._create_vertex(node_id)
            self._link_to_parent(vertex, parent)

            for key, value in element.items():
                if not isinstance(value, (dict, list)):
                    self._add_property_to_vertex(vertex, key, value)
                else:
                    self._process_element(value, vertex)

    def _add_property_to_vertex(self, vertex, key, value):
        value = self._parse_value(value)
        vertex.add_attribute(key, value)

    def _create_vertex(self, node_id):
        vertex_name = f"node{node_id}"
        vertex = Graph.Vertex(node_id, name=vertex_name)
        self._graph_structure.insert_created_vertex(vertex)
        self._vertices_map[node_id] = vertex
        return vertex

    def _link_to_parent(self, current, parent):
        if parent:
            self._explicit_links.setdefault(parent.Id, []).append(current.Id)

    def _map_known_id_to_generated(self, element, gen_id):
        for key, value in element.items():
            if re.match(self._id_matcher, str(key).lower()):
                self._doc_id_to_internal_id[value] = gen_id

    def _process_list_element(self, elements, parent=None):
        for item in elements:
            if isinstance(item, (dict, list)):
                self._process_element(item, parent)
            else:
                if item in self._doc_id_to_internal_id:
                    node = self._vertices_map[self._doc_id_to_internal_id[item]]
                    self._link_to_parent(node, parent)
                else:
                    self._inferred_links.setdefault(parent.Id, []).append(item) if parent else self._process_single_value_element(item)

    @staticmethod
    def _parse_value(value):
        if isinstance(value, str):
            value = JsonFileLoader._try_parse_boolean(value) or JsonFileLoader._try_parse_float(value) or JsonFileLoader._try_parse_date(value)
        return value

    @staticmethod
    def _try_parse_boolean(value):
        return value.lower() == "true" if value.lower() in ["true", "false"] else None

    @staticmethod
    def _try_parse_float(value):
        try:
            return float(value)
        except ValueError:
            return None

    @staticmethod
    def _try_parse_date(value):
        try:
            return parse(value, fuzzy=False)
        except ValueError:
            return None

    def _process_single_value_element(self, value):
        parsed_value = self._parse_value(value)
        node_id = self._next_id()
        vertex = self._create_vertex(node_id)
        vertex.add_attribute("value", parsed_value)

    def get_identifier(self):
        return "JsonFileLoader"

    def name(self):
        return "JsonFileLoader"
