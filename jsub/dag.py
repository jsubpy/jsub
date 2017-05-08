import random
import copy


class DagVertexNotFoundError(Exception):
    pass

class DagEdgeNotFoundError(Exception):
    pass

class DagCycleError(Exception):
    pass


def dag_endpoints(graph):
    endpoints = set()
    for v_f, v_t in graph.items():
        if not v_t:
            endpoints.add(v_f)
    return endpoints

def dag_has_path_to(v_from, v_to, graph):
    if v_from == v_to:
        return True
    for v in graph[v_from]:
        if dag_has_path_to(v, v_to, graph):
            return True
    return False


class UnorderedGraph(object):
    def __init__(self):
        self.__graph = {}
        self.__graph_reverse = {}

        self.__starts = set()
        self.__terminals = set()


    def is_vertex_valid(self, vertex):
        return vertex in self.__graph

    def is_edge_valid(self, v_from, v_to):
        return (v_from in self.__graph) and (v_to in self.__graph[v_from])

    def has_path_to(self, v_from, v_to):
        return dag_has_path_to(v_from, v_to, self.__graph)


    def vertice(self):
        return self.graph.keys()


    def add_vertex(self, vertex):
        if vertex not in self.__graph:
            self.__starts.add(vertex)
            self.__terminals.add(vertex)
            self.__graph[vertex] = set()
            self.__graph_reverse[vertex] = set()

    def add_edge(self, v_from, v_to):
        self.__graph[v_from].add(v_to)
        self.__graph_reverse[v_to].add(v_from)

    def remove_edge(self, v_from, v_to):
        self.__graph[v_from].remove(v_to)
        self.__graph_reverse[v_to].remove(v_from)


class Dag(object):
    def __init__(self, handler):
        self.__handler = handler

    def __validate_vertex(self, *vertice):
        for vertex in vertice:
            if not self.__handler.is_vertex_valid(vertex):
                raise DagVertexNotFoundError('Vertex "%s" does not belong to DAG' % vertex)


    def add_vertex(self, *vertice):
        for vertex in vertice:
            self.__handler.add_vertex(vertex)

    def add_edge(self, v_from, *v_tos):
        self.__validate_vertex(v_from, *v_tos)

        for v_to in v_tos:
            if self.__handler.has_path_to(v_to, v_from):
                raise DagCycleError('Cycle if add edge from "%s" to "%s"' % (v_from, v_to))
            self.__handler.add_edge(v_from, v_to)

    def remove_edge(self, v_from, v_to):
        self.__validate_vertex(v_from, v_to)
        if not self.__handler.is_edge_valid(v_from, v_to):
            raise DagEdgeNotFoundError('Edge not found from "%s" to "%s"' % (v_from, v_to))

        self.__handler.remove_edge(v_from, v_to)


    def edge_size(self):
        size = 0
        for vertex in self.__handler.vertice():
            size += self.indegree(vertex)
        return size


    def successors(self, vertex):
        self.__validate_vertex(vertex)
        return self.__graph[vertex]

    def predecessors(self, vertex):
        self.__validate_vertex(vertex)
        return self.__graph_reverse[vertex]

    def indegree(self, vertex):
        self.__validate_vertex(vertex)
        return len(self.predecessors(vertex))

    def outdegree(self, vertex):
        self.__validate_vertex(vertex)
        return len(self.successors(vertex))


    def all_starts(self):
        return dag_endpoints(self.__graph_reverse)

    def all_terminals(self):
        return dag_endpoints(self.__graph)


    def topo_sort(self):
        dag_temp = copy.deepcopy(self)

        vertice_zero_indegree = dag_temp.all_starts()
        sorted_vertice = vertice_zero_indegree[:]

        while vertice_zero_indegree:
            vertex = random.choice(vertice_zero_indegree)
            sorted_vertice.append(vertex)
            vertice_zero_indegree.remove(unit)

            for v_to in dag_temp.successors(unit):
                dag_temp.remove_edge(vertex, v_to)
                if dag_temp.indegree(v_to) == 0:
                    vertice_zero_indegree.add(v_to)

        return sorted_vertice


class Dag(DagBase):
    def __init__(self):
        super(Dag, self).__init__()


class OrderedDag(DagBase):
    def __init__(self):
        super(OrderedDag, self).__init__()
