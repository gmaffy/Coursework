"""Implementation of Project 1 - Degree distributions for graphs"""

##Part 1: Representing Directed Graphs as Dictionaries

#Define directed graph constants

EX_GRAPH0 = {0: set([1, 2]), 1: set([]), 2: set([])}
EX_GRAPH1 = {0: set([1,4,5]), 1: set([2,6]), 2: set([3]), 3: set([0]), 4: set([1]), 5: set([2]), 6: set([])}
EX_GRAPH2 = {0: set([1,4,5]), 1: set([2,6]), 2: set([3,7]), 3: set([7]), 4: set([1]), 5: set([2]), 6: set([]), 7: set([3]), 8: set([1,2]), 9: set([0, 4, 5, 6, 7, 3])}

#Function to make complete graph
def make_complete_graph(num_nodes):
    """Input integer number of notes and return dictionary corresponding to complete directed graph"""
    nodes = range(0,num_nodes)
    graph_dict = {}
    
    for item_1 in nodes:
        item_1_outs = list()
        for item_2 in nodes:
            if not item_1 == item_2:
                item_1_outs.append(item_2)
        graph_dict[item_1]=set(item_1_outs)

    return graph_dict

##Part 2: Computing Degree Distributions

def compute_in_degrees(digraph):
    """Take dict representation of directed graph and return dict with node: in-degree pairs"""
    deg_dict = dict()

    #initialize deg_dict with nodes from digraph
    keys = digraph.keys()
    for node in keys:
        deg_dict[node]=0

    #loop through edges of digraph and count in-degree
    for node in keys:
        for edge_set in digraph.values():
            if node in edge_set:
                deg_dict[node]+=1

    return deg_dict

def in_degree_distribution(digraph):
    """Take dict representation of directed graph"""
    dist_dict = dict()
    
    deg_dict = compute_in_degrees(digraph)

    for value in deg_dict.values():
        try:
            dist_dict[value]+=1
        except KeyError:
            dist_dict[value]=1

    return dist_dict


##Application: Brute-Force Algorithm to Generate Random Directed Graphs
import random

def make_random_graph(num_nodes, p=0.5):
    """Input integer number of notes and return dictionary corresponding to randomly-conntected directed graph"""
    nodes = range(0,num_nodes)
    graph_dict = {}
    
    for item_1 in nodes:
        item_1_outs = list()
        for item_2 in nodes:
            if not item_1 == item_2 and random.random()<p:
                item_1_outs.append(item_2)
        graph_dict[item_1]=set(item_1_outs)

    return graph_dict

##Application: DPA Algorithm to Iteratively Generate Randomly-Connected Graphs
def dpa_graph(n, m):
    """Generate a graph with n nodes where each new node is randomly connected to m other nodes (m<=n)"""
    #Generate a complete graph of size m
    m_graph = make_complete_graph(m)
    m_graph_clone = dict(m_graph)
    
    #Grow graph by adding n-m nodes, where each new node is connected to m nodes randomly chosen from existing nodes
    counter = m
    while counter<n:
        out_nodes = []
        for dummy_var in range(0,m):
            out_nodes.append(random.choice(m_graph_clone.keys()))
        m_graph_clone[counter] = set(out_nodes) #eliminate duplicate choices; N.B. connectivity may be < m for this reason
        counter+=1
    return m_graph_clone

##Optimized code to implement DPA
##Code provided by Rice University
class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
    
