"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2
import matplotlib.pyplot as plt
import math
import random

# Set timeout for CodeSkulptor if necessary
# import codeskulptor
# codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

###################################

class DiGraph(object):
    def __init__(self, graph_dict = None):
        self.graph_dict = graph_dict
        self.m = 0

    def load_graph(self, graph_dict):
        assert type(graph_dict) == type({})
        self.graph_dict = graph_dict

    def __compute_degree_per_node(self):
        degree_per_node = {}

        for node in self.graph_dict.keys():
            for target in self.graph_dict[node]:
                try:
                    degree_per_node[target] += 1
                    self.m += 1
                except KeyError:
                    degree_per_node[target] = 1
                    self.m += 1
        return degree_per_node

    def mean_out_degree(self):
        all_edges = []
        for key in self.graph_dict.keys():
            all_edges.extend(self.graph_dict[key])
        return len(all_edges)/float(len(self.graph_dict.keys()))

    def compute_degree_dist(self):
        assert self.graph_dict

        degree_dist = {}

        degree_per_node = self.__compute_degree_per_node()
        total_degree = 0.0

        for node in degree_per_node.keys():
            degree = degree_per_node[node]
            total_degree += 1.0
            try:
                degree_dist[degree] += 1.0
            except KeyError:
                degree_dist[degree] = 1.0

        return {degree : degree_dist[degree]/total_degree for degree in degree_dist.keys()}

    def generate_ER(self, n, p = 0.5):
        graph_dict = {}
        for node1 in xrange(n):
            graph_dict[node1] = []
            for node2 in xrange(n):
                if not node1 == node2 and random.random() > p:
                    graph_dict[node1].append(node2)
        self.load_graph(graph_dict)

    def generate_complete(self, n):
        graph_dict = {}
        for node1 in xrange(n):
            graph_dict[node1] = []
            for node2 in xrange(n):
                if not node1 == node2:
                    graph_dict[node1].append(node2)
        self.load_graph(graph_dict)

    def total_indegree(self):
        total_indegree = 0
        return sum(self.__compute_degree_per_node().values())

    def generate_DPA(self, n, m):
        #self.generate_complete()
        all_in_nodes = [i for i in xrange(n)]
        self.graph_dict = {}

        #for node in self.graph_dict.keys():
        #       all_in_nodes.extend(self.graph_dict[node])

        #all_in_nodes.extend([i for i in xrange(m,n)])

        for i in xrange(m,n):
            all_in_nodes.append(i)
            to_add = list(set(random.sample(all_in_nodes, m)))
            #print all_in_nodes
            #print to_add
            self.graph_dict[i] = to_add
            all_in_nodes.extend(to_add)


        #print self.graph_dict



    def loglogplot(self):
        degree_dist = self.compute_degree_dist()

        fig, ax = plt.subplots()

        x = [math.log(degree) for degree in degree_dist.keys() if degree]
        y = [math.log(degree_dist[degree]) for degree in degree_dist.keys() if degree]

        ax.scatter(x, y)

        ax.set_xlabel('log2(in-degree)', fontsize=20)
        ax.set_ylabel('log2(number of nodes)', fontsize=20)
        ax.set_title('In-Degree Distribution of Rich-Get-Richer Graph (n=27,700; m=13)')

        ax.grid(True)
        fig.tight_layout()

        plt.show()

    def linearplot(self):
        degree_dist = self.compute_degree_dist()

        fig, ax = plt.subplots()

        x = [degree for degree in degree_dist.keys() if degree]
        y = [degree_dist[degree] for degree in degree_dist.keys() if degree]

        ax.scatter(x, y)

        ax.set_xlabel('in-degree', fontsize=20)
        ax.set_ylabel('number of nodes', fontsize=20)
        ax.set_title('In-Degree Distribution of ER Graph (n=1,000; p=0.5)')

        ax.grid(True)
        fig.tight_layout()

        plt.show()



if __name__ == "__main__":
    #cite_graph = DiGraph(load_graph(CITATION_URL))
    #print cite_graph.mean_out_degree()
    #m = 12.7
    cite_graph = DiGraph()
    cite_graph.generate_DPA(27700,13)
    cite_graph.loglogplot()
    #cite_graph.loglogplot()