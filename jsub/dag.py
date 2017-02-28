import random
import copy


class DAGVertexNotFoundError(Exception):
    pass

class DAGEdgeNotFoundError(Exception):
    pass

class DAGCycleError(Exception):
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


class DAG:
    def __init__(self):
        self.__graph = {}
        self.__graph_reverse = {}


    def __validate_vertex(self, *vertice):
        for vertex in vertice:
            if vertex not in self.__graph:
                raise DAGVertexNotFoundError('Vertex "%s" does not belong to DAG' % vertex)


    def add_vertex(self, vertex):
        if vertex not in self.__graph:
            self.__graph[vertex] = set()
            self.__graph_reverse[vertex] = set()

    def add_edge(self, v_from, v_to):
        self.__validate_vertex(v_from, v_to)
        if dag_has_path_to(v_to, v_from, self.__graph):
            raise DAGCycleError('Cycle if add edge from "%s" to "%s"' % (v_from, v_to))

        self.__graph[v_from].add(v_to)
        self.__graph_reverse[v_to].add(v_from)

    def remove_edge(self, v_from, v_to):
        self.__validate_vertex(v_from, v_to)
        if v_to not in self.__graph[v_from]:
            raise DAGEdgeNotFoundError('Edge not found from "%s" to "%s"' % (v_from, v_to))

        self.__graph[v_from].remove(v_to)
        self.__graph_reverse[v_to].remove(v_from)


    def edge_size(self):
        size = 0
        for vertex in self.__graph:
            size += self.indegree(vertex)
        return size

    def successors(self, vertex):
        self.__validate_vertex(vertex)
        return set(self.__graph[vertex])

    def predecessors(self, vertex):
        self.__validate_vertex(vertex)
        return set(self.__graph_reverse[vertex])

    def indegree(self, vertex):
        self.__validate_vertex(vertex)
        return len(self.__graph_reverse[vertex])

    def outdegree(self, vertex):
        self.__validate_vertex(vertex)
        return len(self.__graph[vertex])

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
