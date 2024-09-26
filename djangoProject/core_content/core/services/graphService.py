from core.models import Graph
from dateutil.parser import parse
from datetime import datetime
import copy

class GraphService:

    @staticmethod
    def search(G, query):
        if G is None:
            return None
        separator = " "
        query_list = query.split(separator)
        retval = Graph(G.is_directed())
        vertices = {}
        newVertices = {}
        for v in G.vertices():
            for i in v.attributes.keys():
                for q in query_list:
                    if i == q:
                        vertices[v.Id] = v
                        newVertex = copy.deepcopy(v)
                        newVertex.neighbors = None
                        newVertices[v.Id] = newVertex
                        if retval.get_vertex_by_Id(v.Id) is None:
                            retval.insert_created_vertex(newVertex)

        for k1, v1 in newVertices.items():
            for k2, v2 in newVertices.items():
                if G.get_edge(vertices[k1], vertices[k2]) is not None:
                    if retval.get_edge(v1, v2) is None:
                        retval.insert_edge(v1, v2)
        return retval

    @staticmethod
    def filter(G, atr, operator, value):
        if G is None:
            return None
        retval = Graph(G.is_directed())
        vertices = {}
        newVertices = {}
        for v in G.vertices():
            for i in v.attributes.keys():
                if i == atr:
                    compareTo = v.attributes[i]
                    if GraphService.__vertex_match_query(value, operator, compareTo):
                        vertices[v.Id] = v
                        newVertex = copy.deepcopy(v)
                        newVertex.neighbors = None
                        newVertices[v.Id] = newVertex
                        retval.insert_created_vertex(newVertex)
				        
        for k1, v1 in newVertices.items():
            for k2, v2 in newVertices.items():
                if G.get_edge(vertices[k1], vertices[k2]) is not None:
                    if retval.get_edge(v1, v2) is None:
                        retval.insert_edge(v1, v2)
        return retval

    @staticmethod
    def __vertex_match_query(value, operator, compareTo):
        value = try_parse_boolean(value)
        if type(value) is bool:
            return GraphService.__matched(value, operator, compareTo)

        value = try_parse_float(value)
        if type(value) is float:
            return GraphService.__matched(value, operator, compareTo)

        value = try_parse_date(value)
        if type(value) is datetime:
            return GraphService.__matched(value, operator, compareTo)

        return GraphService.__matched(value, operator, compareTo)

    @staticmethod
    def __matched(value, operator, compareTo):
        if operator == "==":
            return compareTo == value
        if operator == ">":
            return compareTo > value
        if operator == ">=":
            return compareTo >= value
        if operator == "<":
            return compareTo < value
        if operator == "<=":
            return compareTo <= value
        if operator == "!=":
            return compareTo != value

def try_parse_boolean(value):
    if value.lower() == "false":
        value = False
    elif value.lower() == "true":
        value = True
    return value


def try_parse_float(value):
    try:
        value = float(value)
    finally:
        return value

def try_parse_date(value):
    try:
        value = parse(value, False)
    finally:
        return value
