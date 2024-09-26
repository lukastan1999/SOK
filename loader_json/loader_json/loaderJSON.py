from core.models import Graph
from core.services.services import LoadBase
import json
import re
from dateutil.parser import parse
from datetime import datetime


class JsonLoader(LoadBase):

	def __init__(self):
		self.__generated_id = -1
		self.__vertices = {}
		self.__possible_ids = re.compile(r"(id|identifier)[0-9]?")
		self.__documentIdsMapper = {}
		self.__links = {}
		self.__potential_links = {}
		self.__graph = Graph(True)

	def __generate_id(self):
		self.__generated_id += 1
		return self.__generated_id

	def __reset_state(self):
		self.__generated_id = -1
		self.__vertices = {}
		self.__documentIdsMapper = {}
		self.__links = {}
		self.__potential_links = {}
		self.__graph = Graph(True)

	def load_data(self, source) -> Graph:
		if not source.endswith(".json"):
			return Graph()
		try:
			with open("test_data/" + source) as file:
				self.__reset_state()
				data = json.load(file)
				self.__process_node(data)
				self.__add_edges()
				return self.__graph
		except:
			return Graph()

	def __add_edges(self):
		self.__add_sure_edges()
		self.__add_potential_edges()

	def __add_sure_edges(self):
		for node, neighbours in self.__links.items():
			for n in neighbours:
				fromm = self.__vertices[node]
				too = self.__vertices[n]
				if self.__graph.get_edge(fromm, too) is None:
					self.__graph.insert_edge(fromm, too)

	def __add_potential_edges(self):
		for node, neighbours in self.__potential_links.items():
			for n in neighbours:
				fromm = self.__vertices[node]
				if n in self.__documentIdsMapper:
					too = self.__vertices[self.__documentIdsMapper[n]]
					if self.__graph.get_edge(fromm, too) is None:
						self.__graph.insert_edge(fromm, too)
				else:
					nodeId = self.__generate_id()
					too = self.__create_vertex(nodeId)
					self.__add_atribute_to_vertex(too, "value", n)
					if self.__graph.get_edge(fromm, too) is None:
						self.__graph.insert_edge(fromm, too)

	def __process_node(self, currentNode, parent=None, id=None):
		if type(currentNode) is dict:
			self.__process_dict_node(currentNode, parent, id)
		elif type(currentNode) is list:
			self.__process_list_node(currentNode, parent)
		else:
			self.__process_primitive_node(currentNode)

	def __process_dict_node(self, currentNode, parent=None, id=None):
		if self.__all_values_are_dict_type(currentNode):
			for k, v in currentNode.items():
				self.__process_node(v, parent, k)
		else:
			nodeId = self.__generate_id()
			if id is not None:
				self.__documentIdsMapper[id] = nodeId
			else:
				self.__map_node_idValue_if_exist_to_generated_id(currentNode, nodeId)

			vertex = self.__create_vertex(nodeId)
			self.__create_link_to_parent(vertex, parent)

			for k, v in currentNode.items():
				if type(v) is not dict and type(v) is not list:
					self.__add_atribute_to_vertex(vertex, k, v)
				else:
					self.__process_node(v, vertex)

	def __add_atribute_to_vertex(self, vertex, key, value):
		value = self.__parse_value_of_attribute(value)
		vertex.add_attribute(key, value)

	def __create_vertex(self, nodeId):
		vertexName = "name" + str(nodeId)
		vertex = Graph.Vertex(nodeId, name=vertexName)
		self.__graph.insert_created_vertex(vertex)
		self.__vertices[nodeId] = vertex
		return vertex

	def __create_link_to_parent(self, currentNode, parent):
		if parent is not None:
			if parent.Id not in self.__links:
				self.__links[parent.Id] = []
			self.__links[parent.Id].append(currentNode.Id)

	def __map_node_idValue_if_exist_to_generated_id(self, currentNode, generatedId):
		for k, v in currentNode.items():
			if re.match(self.__possible_ids, str(k).lower()):
				self.__documentIdsMapper[v] = generatedId

	@staticmethod
	def __all_values_are_dict_type(currentNode):
		for k, v in currentNode.items():
			if type(v) is not dict:
				return False
		return True

	def __process_list_node(self, currentNode, parent=None):
		for element in currentNode:
			if type(element) is dict or type(element) is list:
				self.__process_node(element, parent)
			else:
				if element in self.__documentIdsMapper:
					node = self.__vertices[self.__documentIdsMapper[element]]
					self.__create_link_to_parent(node, parent)
				else:
					if parent is not None:
						if parent.Id not in self.__potential_links:
							self.__potential_links[parent.Id] = []
						self.__potential_links[parent.Id].append(element)
					else:
						self.__process_primitive_node(element)

	@staticmethod
	def __try_parse_boolean(value):
		if value.lower() == "false":
			value = False
		elif value.lower() == "true":
			value = True
		return value

	@staticmethod
	def __try_parse_float(value):
		try:
			value = float(value)
		finally:
			return value

	@staticmethod
	def __try_parse_date(value):
		try:
			value = parse(value, False)
		finally:
			return value

	def __parse_value_of_attribute(self, value):
		try:
			value = self.__try_parse_boolean(value)
			if type(value) is bool:
				return value

			value = self.__try_parse_float(value)
			if type(value) is float:
				return value

			value = self.__try_parse_date(value)
			if type(value) is datetime:
				return value
		finally:
			return value

	def __process_primitive_node(self, currentNode):
		value = self.__parse_value_of_attribute(currentNode)
		nodeId = self.__generate_id()
		vertex = self.__create_vertex(nodeId)
		vertex.add_attribute("value", value)

	def identifier(self):
		return "jsonLoader"

	def name(self):
		return "jsonLoader"
