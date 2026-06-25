import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._attori = []
        self._idMapA = {}

    def buildGraph(self, voto1, voto2):
        self._graph.clear()
        self._attori = DAO.getAllNodes(voto1, voto2)
        for a in self._attori:
            self._idMapA[a.id] = a

        self._graph.add_nodes_from(self._attori)

        edges = DAO.getAllEdges(voto1, voto2, self._idMapA)

        for e in edges:
            self._graph.add_edge(e.at1, e.at2, weight=e.peso)

    def getTop3Archi(self):
        lista3Top = sorted(self._graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)

        return lista3Top[0:5]

    def getComponentiConnesse(self):
        components = list(nx.connected_components(self._graph))
        largest = max(components, key=len)
        subgraph = self._graph.subgraph(largest).copy()
        orderedNodes = sorted(subgraph.nodes(), key=lambda n: self._graph.degree(n), reverse=True)
        details = [(n, self._graph.degree(n)) for n in orderedNodes]
        return len(components), largest, details

    def getAllVoti(self):
        return DAO.getAllVoti()

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)