
from core.models import Graph
import random
from datetime import  datetime

# Create your tests here.

colors_attribute = ["red", "blue", "white", "orange", "black", "pink", "green"]
languages_attribute = ["Spanish", "French", "Italian", "Russian", "English", "Serbian"]

def generate_random_attributes(n):
    attributes = []
    for i in range(n):
        attributes.append({
            "name" : "name" + str(i),
            "color" : random.choice(colors_attribute),
            "size" : random.randint(0,22),
            "status" : True if i%2 == 0 else False,
            "language" : random.choice(languages_attribute)
        })

    return attributes

def generate_vetrexs(n):
    attributes = generate_random_attributes(n)
    vertexs = []
    for i in range(n):
        vertexs.append(Graph.Vertex(i ,"naziv" + str(i), attributes[i]))

    return vertexs

class Node:
    def __init__(self, vertex, parent_index):
        self.vertex = vertex
        self.parent_index = parent_index
        self.left = None
        self.right = None

#6 cvorova, neusmeren, aciklican
def create_small_tree():
    graph = Graph()
    vertexs = generate_vetrexs(6)
    attributes = generate_random_attributes(6)

    graph.insert_created_vertex(vertexs[0])
    graph.insert_created_vertex(vertexs[1])
    graph.insert_created_vertex(vertexs[2])
    graph.insert_created_vertex(vertexs[3])
    graph.insert_created_vertex(vertexs[4])
    graph.insert_created_vertex(vertexs[5])

    graph.insert_edge(vertexs[0], vertexs[3])
    graph.insert_edge(vertexs[1], vertexs[3])
    graph.insert_edge(vertexs[2], vertexs[3])
    graph.insert_edge(vertexs[3], vertexs[4])
    graph.insert_edge(vertexs[4], vertexs[5])

    return graph

#100 cvorova, neusmeren i aciklican graf
def create_big_tree():
    graph = Graph()
    vertexs = generate_vetrexs(50)

    currentVertex = None

    for i in range(50):
        if i == 0:
            graph.insert_created_vertex(vertexs[i])
            currentVertex = Node(vertexs[i], i)
            continue
        else:
            if (currentVertex.left == None):
                currentVertex.left = vertexs[i]
                graph.insert_created_vertex(vertexs[i])
                graph.insert_edge(vertexs[currentVertex.parent_index], vertexs[i])
                continue
            elif (currentVertex.right == None):
                currentVertex.right = vertexs[i]
                graph.insert_created_vertex(vertexs[i])
                graph.insert_edge(vertexs[currentVertex.parent_index], vertexs[i])
                continue

        if currentVertex.left != None and currentVertex.right != None:
            graph.insert_created_vertex(vertexs[i])
            graph.insert_edge(vertexs[currentVertex.parent_index], vertexs[i])
            currentVertex = Node(vertexs[i], i)
            continue

    return graph

#5 cvorova, neusmeren ciklican
def create_small_cycle_graph():
    graph = Graph()
    vertexs = generate_vetrexs(5)
    attributes = generate_random_attributes(5)

    graph.insert_created_vertex(vertexs[0])
    graph.insert_created_vertex(vertexs[1])
    graph.insert_created_vertex(vertexs[2])
    graph.insert_created_vertex(vertexs[3])
    graph.insert_created_vertex(vertexs[4])

    graph.insert_edge(vertexs[0], vertexs[1])
    graph.insert_edge(vertexs[0], vertexs[2])
    graph.insert_edge(vertexs[1], vertexs[2])
    graph.insert_edge(vertexs[0], vertexs[3])
    graph.insert_edge(vertexs[3], vertexs[4])

    return graph

#neusmeren, ciklican, 13 cvorova
def create_middle_cycle_graph():
    graph = Graph()
    vertexs = generate_vetrexs(13)
    attributes = generate_random_attributes(13)

    graph.insert_created_vertex(vertexs[0])
    graph.insert_created_vertex(vertexs[1])
    graph.insert_created_vertex(vertexs[2])
    graph.insert_created_vertex(vertexs[3])
    graph.insert_created_vertex(vertexs[4])
    graph.insert_created_vertex(vertexs[5])
    graph.insert_created_vertex(vertexs[6])
    graph.insert_created_vertex(vertexs[7])
    graph.insert_created_vertex(vertexs[8])
    graph.insert_created_vertex(vertexs[9])
    graph.insert_created_vertex(vertexs[10])
    graph.insert_created_vertex(vertexs[11])
    graph.insert_created_vertex(vertexs[12])

    graph.insert_edge(vertexs[0], vertexs[1])
    graph.insert_edge(vertexs[1], vertexs[2])
    graph.insert_edge(vertexs[2], vertexs[3])
    graph.insert_edge(vertexs[2], vertexs[4])
    graph.insert_edge(vertexs[3], vertexs[6])
    graph.insert_edge(vertexs[6], vertexs[7])
    graph.insert_edge(vertexs[3], vertexs[5])
    graph.insert_edge(vertexs[4], vertexs[5])
    graph.insert_edge(vertexs[4], vertexs[8])
    graph.insert_edge(vertexs[5], vertexs[9])
    graph.insert_edge(vertexs[9], vertexs[10])
    graph.insert_edge(vertexs[10], vertexs[11])
    graph.insert_edge(vertexs[10], vertexs[12])
    graph.insert_edge(vertexs[11], vertexs[12])

    return graph

#100 cvorova, neusmeren, ciklican
def create_big_cycle_graph():
    graph = Graph()
    vertexs = generate_vetrexs(100)

    currentVertex = None
    counter = 0
    left_index = None
    for i in range(100):
        if i == 0:
            graph.insert_created_vertex(vertexs[i])
            currentVertex = Node(vertexs[i], i)
            continue
        else:
            if (currentVertex.left == None):
                currentVertex.left = vertexs[i]
                graph.insert_created_vertex(vertexs[i])
                graph.insert_edge(vertexs[currentVertex.parent_index], vertexs[i])
                left_index = i
                continue
            elif (currentVertex.right == None):
                currentVertex.right = vertexs[i]
                graph.insert_created_vertex(vertexs[i])
                graph.insert_edge(vertexs[currentVertex.parent_index], vertexs[i])
                if counter == 10 or counter == 20 or 30:
                    graph.insert_edge(vertexs[left_index], vertexs[i])
                    counter += 1
                continue

        if currentVertex.left != None and currentVertex.right != None:
            graph.insert_created_vertex(vertexs[i])
            graph.insert_edge(vertexs[currentVertex.parent_index], vertexs[i])
            currentVertex = Node(vertexs[i], i)
            continue

    return graph

def create_small_direct():
    graph = Graph(True)
    vertexs = generate_vetrexs(4)
    attributes = generate_random_attributes(4)

    graph.insert_created_vertex(vertexs[0])
    graph.insert_created_vertex(vertexs[1])
    graph.insert_created_vertex(vertexs[2])
    graph.insert_created_vertex(vertexs[3])

    graph.insert_edge(vertexs[0], vertexs[1])
    graph.insert_edge(vertexs[0], vertexs[2])
    graph.insert_edge(vertexs[2], vertexs[1])
    graph.insert_edge(vertexs[2], vertexs[3])

    return graph

#12 cvorova, usmeren, mislim da je bez ciklusa
def create_middle_direct():
    graph = Graph(True)
    vertexs = generate_vetrexs(12)

    graph.insert_created_vertex(vertexs[0])
    graph.insert_created_vertex(vertexs[1])
    graph.insert_created_vertex(vertexs[2])
    graph.insert_created_vertex(vertexs[3])
    graph.insert_created_vertex(vertexs[4])
    graph.insert_created_vertex(vertexs[5])
    graph.insert_created_vertex(vertexs[6])
    graph.insert_created_vertex(vertexs[7])
    graph.insert_created_vertex(vertexs[8])
    graph.insert_created_vertex(vertexs[9])
    graph.insert_created_vertex(vertexs[10])
    graph.insert_created_vertex(vertexs[11])

    graph.insert_edge(vertexs[0], vertexs[2])
    graph.insert_edge(vertexs[0], vertexs[4])
    graph.insert_edge(vertexs[0], vertexs[3])
    graph.insert_edge(vertexs[2], vertexs[5])
    graph.insert_edge(vertexs[2], vertexs[1])
    graph.insert_edge(vertexs[1], vertexs[9])
    graph.insert_edge(vertexs[1], vertexs[10])
    graph.insert_edge(vertexs[9], vertexs[6])
    graph.insert_edge(vertexs[10], vertexs[6])
    graph.insert_edge(vertexs[4], vertexs[7])
    graph.insert_edge(vertexs[7], vertexs[10])
    graph.insert_edge(vertexs[4], vertexs[11])
    graph.insert_edge(vertexs[11], vertexs[8])

    graph.get_vertex_by_Id(2).add_attribute("hahaha", "test1")
    graph.get_vertex_by_Id(2).add_attribute("boolean", True)
    graph.get_vertex_by_Id(2).add_attribute("broj", 4)
    graph.get_vertex_by_Id(2).add_attribute("datum", datetime(2020, 3, 3))

    graph.get_vertex_by_Id(5).add_attribute("hahaha", "test2")
    graph.get_vertex_by_Id(5).add_attribute("boolean", True)
    graph.get_vertex_by_Id(5).add_attribute("broj", 4)
    graph.get_vertex_by_Id(5).add_attribute("datum", datetime(2021, 4, 3))

    graph.get_vertex_by_Id(1).add_attribute("hahaha", "test3")
    graph.get_vertex_by_Id(1).add_attribute("boolean", True)
    graph.get_vertex_by_Id(1).add_attribute("broj", 4)
    graph.get_vertex_by_Id(1).add_attribute("datum", datetime(2020, 5, 3))

    graph.get_vertex_by_Id(9).add_attribute("hahaha", "test4")
    graph.get_vertex_by_Id(9).add_attribute("broj", 3.432)
    graph.get_vertex_by_Id(9).add_attribute("boolean", True)
    graph.get_vertex_by_Id(9).add_attribute("datum", datetime(2020, 7, 3))

    graph.get_vertex_by_Id(6).add_attribute("hahaha", "test4")
    graph.get_vertex_by_Id(6).add_attribute("boolean", True)
    graph.get_vertex_by_Id(6).add_attribute("broj", 3.432)
    graph.get_vertex_by_Id(6).add_attribute("datum", datetime(2020, 8, 8))

    graph.get_vertex_by_Id(10).add_attribute("hahaha", "test4")
    graph.get_vertex_by_Id(10).add_attribute("boolean", False)
    graph.get_vertex_by_Id(10).add_attribute("broj", 3.432)
    graph.get_vertex_by_Id(10).add_attribute("datum", datetime(2021, 5, 3))

    return graph

#100 cvorova, usmeren, mislim da je bez ciklusa
def create_big_direct():
    graph = Graph(True)
    vertexs = generate_vetrexs(200)

    currentVertex = None
    for i in range(200):
        if i == 0:
            graph.insert_created_vertex(vertexs[i])
            currentVertex = Node(vertexs[i], i)
            continue
        else:
            if (currentVertex.left == None):
                currentVertex.left = vertexs[i]
                graph.insert_created_vertex(vertexs[i])
                graph.insert_edge(vertexs[currentVertex.parent_index], vertexs[i])
                continue
            elif (currentVertex.right == None):
                currentVertex.right = vertexs[i]
                graph.insert_created_vertex(vertexs[i])
                graph.insert_edge(vertexs[currentVertex.parent_index], vertexs[i])
                continue

        if currentVertex.left != None and currentVertex.right != None:
            graph.insert_created_vertex(vertexs[i])
            graph.insert_edge(vertexs[currentVertex.parent_index], vertexs[i])
            currentVertex = Node(vertexs[i], i)
            continue

    return graph




