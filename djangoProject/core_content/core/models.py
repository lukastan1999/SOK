from django.db import models


# Create your models here.


class Graph:
    # ------------------------- Ugnježdena klasa Vertex -------------------------
    class Vertex:
        """ Struktura koja predstavlja čvor grafa."""

        def __init__(self, Id, name=None, attributes=None, neighbors=None):
            self._Id = Id
            self._name = name
            self._attributes = {} if attributes is None else attributes
            self._neighbors = [] if neighbors is None else neighbors

        @property
        def Id(self):
            return self._Id

        @property
        def name(self):
            return self._name

        @property
        def attributes(self):
            return self._attributes

        @property
        def neighbors(self):
            return self._neighbors

        @neighbors.setter
        def neighbors(self, value):
            if value is None:
                self._neighbors = []
            else:
                self._neighbors = value

        def __hash__(self):  # omogućava da Vertex bude ključ mape
            return hash(id(self))

        def __str__(self):
            return str(self._Id)

        def add_attribute(self, key, value):
            self._attributes[key] = value

        def add_neighbor(self, v):
            if self._neighbors is None or len(self._neighbors) == 0:
                self._neighbors = []
                self._neighbors.append(v)
            else:
                self._neighbors.append(v)

    # ------------------------- Ugnježdena klasa Edge -------------------------
    class Edge:
        """ Struktura koja predstavlja ivicu grafa """
        __slots__ = '_origin', '_destination', '_element'

        def __init__(self, origin, destination, element):
            self._origin = origin
            self._destination = destination
            self._element = element

        def endpoints(self):
            """ Vraća torku (u,v) za čvorove u i v."""
            return (self._origin, self._destination)

        def opposite(self, v):
            """ Vraća čvor koji se nalazi sa druge strane čvora v ove ivice."""
            if not isinstance(v, Graph.Vertex):
                raise TypeError('v mora biti instanca klase Vertex')
            if self._destination == v:
                return self._origin
            elif self._origin == v:
                return self._destination
            raise ValueError('v nije čvor ivice')

        @property
        def element(self):
            """ Vraća element vezan za ivicu"""
            return self._element

        def __hash__(self):  # omogućava da Edge bude ključ mape
            return hash((self._origin, self._destination))

        def __str__(self):
            return '({0},{1},{2})'.format(self._origin, self._destination, self._element)

    # ------------------------- Metode klase Graph -------------------------
    def __init__(self, directed=False):
        """ Kreira prazan graf (podrazumevana vrednost je da je neusmeren).

		Ukoliko se opcioni parametar directed postavi na True, kreira se usmereni graf.
		"""
        self._outgoing = {}
        # ukoliko je graf usmeren, kreira se pomoćna mapa
        self._incoming = {} if directed else self._outgoing

        # Ovaj atribut generalno ne igra nikakvu ulogu osim ako u podacima postoji striktna
        # hijerarhija stabla kao sto je neki xml dokument, tada ga je potrebno setovati
        self._root = None

    @property
    def root(self):
        return self._root

    def _validate_vertex(self, v):
        """ Proverava da li je v čvor(Vertex) ovog grafa."""
        if not isinstance(v, self.Vertex):
            raise TypeError('Očekivan je objekat klase Vertex')
        if v not in self._outgoing:
            raise ValueError('Vertex ne pripada ovom grafu.')

    def is_directed(self):
        """ Vraća True ako je graf usmeren; False ako je neusmeren."""
        return self._incoming is not self._outgoing  # graf je usmeren ako se mape razlikuju

    def vertex_count(self):
        """ Vraća broj čvorova u grafu."""
        return len(self._outgoing)

    def vertices(self):
        """ Vraća iterator nad svim čvorovima grafa."""
        return self._outgoing.keys()

    def edge_count(self):
        """ Vraća broj ivica u grafu."""
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        # ukoliko je graf neusmeren, vodimo računa da ne brojimo čvorove više puta
        return total if self.is_directed() else total // 2

    def edges(self):
        """ Vraća set svih ivica u grafu."""
        result = set()  # pomoću seta osiguravamo da čvorove neusmerenog grafa brojimo samo jednom
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())  # dodavanje ivice u rezultujući set
        return result

    def get_edge(self, u, v):
        """ Vraća ivicu između čvorova u i v ili None ako nisu susedni."""
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self._outgoing[u].get(v)

    def degree(self, v, outgoing=True):
        """ Vraća stepen čvora - broj(odlaznih) ivica iz čvora v u grafu.

		Ako je graf usmeren, opcioni parametar outgoing se koristi za brojanje dolaznih ivica.
		"""
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        """ Vraća sve (odlazne) ivice iz čvora v u grafu.

		Ako je graf usmeren, opcioni parametar outgoing se koristi za brojanje dolaznih ivica
		tako sto se postavi na False
		"""
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def incident_vertices(self, v, outgoing=True):
        """ Vraća sve odlazne cvorove iz čvora v u grafu.
		Odlazni cvorovi - svi cvorovi na koje dati cvor pokazuje

		Ako je graf usmeren, opcioni parametar outgoing se koristi za dolazne cvorova
		tako sto se postavi na False

		Dolazni cvorovi - svi cvorovi koji pokazuju na dati cvor
		"""
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge.opposite(v)

    def get_incident_vertices(self, v, outgoing=True):

        res = {}
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            neighbor = edge.opposite(v)
            res[neighbor.Id] = neighbor

        return res

    def get_vertex_by_Id(self, Id):
        """Vraca vertex sa prosledjenim Id ukoliko postoji, inace None
		"""
        for v in self.vertices():
            if v.Id == Id:
                return v
        return None

    def insert_new_vertex(self, Id, name=None, attributes=None):
        """ Ubacuje i vraća novi čvor (Vertex)"""
        if self.get_vertex_by_Id(Id) is not None:
            raise ValueError('Vertex with this Id already exist.')
        v = self.Vertex(Id, name, attributes)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}  # mapa različitih vrednosti za dolazne čvorove
        return v

    def insert_created_vertex(self, v):
        """ Ubacuje i vraća čvor (Vertex)"""
        if self.get_vertex_by_Id(v.Id) is not None:
            raise ValueError('Vertex with this Id already exist.')
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}
        return v

    def insert_edge(self, u, v, x=None):
        """ Ubacuje i vraća novu ivicu (Edge) od u do v sa pomoćnim elementom x.

		Baca ValueError ako u i v nisu čvorovi grafa.
		Baca ValueError ako su u i v već povezani.
		"""
        if self.get_edge(u, v) is not None:  # uključuje i proveru greške
            raise ValueError('u and v are already adjacent')
        e = self.Edge(u, v, x)
        self._outgoing[u][v] = e
        # ukoliko se radi o neusmerenom grafu, incoming ce biti isto sto i outgoing
        # pa cemo dobiti dvostruku vezu izmedju cvorova
        self._incoming[v][u] = e
        if not self.is_directed():
            self.get_vertex_by_Id(u.Id).add_neighbor(v)
            self.get_vertex_by_Id(v.Id).add_neighbor(u)
        else:
            self.get_vertex_by_Id(u.Id).add_neighbor(v)

    def is_tree(self):
        """Proverava da li je dati graf stablo (neusmeren i aciklican graf)
		"""
        if self.is_directed() or self.__has_cycle_in_undirected_graph():
            return False
        return True

    def has_cycle(self):
        if self.__has_cycle_in_undirected_graph():
            return True
        return False

    def __dfs_has_cycle(self, current, parent, visited):
        """Pomocna metoda u proveri da li graf ima ciklusa
		"""
        visited[current] = True
        for v in self.incident_vertices(current):
            if not visited[v]:
                if self.__dfs_has_cycle(v, current, visited):
                    return True
            elif parent is not None and v.Id != parent.Id:
                return True
        return False

    def __has_cycle_in_undirected_graph(self):
        """Metoda proverava da li je graf ciklican
		"""
        visited = {}
        for v in self.vertices():
            visited[v] = False
        for v in self.vertices():
            if not visited[v]:
                if self.__dfs_has_cycle(v, None, visited):
                    return True
        return False

    def pretty_print(self):
        print("SELF OUTGOING")
        for k, v in self._outgoing.items():
            print('--------')
            print(k)
            for i, j in v.items():
                print('{} : {}'.format(i, j))
            print('--------')

        print("SELF INCOMING")
        for k, v in self._incoming.items():
            print('--------')
            print(k)
            for i, j in v.items():
                print('{} : {}'.format(i, j))
            print('--------')

    def get_list_roots(self):
        roots = []
        if self._root is not None:
            roots.append(self._root)
        else:
            visited = []
            for v in self.vertices():
                if v not in visited:
                    visited.append(v)
                    roots.append(v)
                    for child in v.neighbors:
                        visited.append(child)
                else:
                    if v.neighbors is not []:
                        for child in v.neighbors:
                            visited.append(child)
        return roots
