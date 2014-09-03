###Implementation of Project 1 - Degree distributions for graphs

##Part 1: Representing Directed Graphs as Dictionaries

#Define directed graph constants

EX_GRAPH0 = {"nodes" : set([0, 1, 2]), "edges": set([(0,1),(0,2)])}
EX_GRAPH1 = {"nodes": set([0, 1, 2, 3, 4, 5, 6]), "edges": set([(0,4),(0,1),(0,5),(1,6),(2,3),(3,0),(4,1),(5,2)])}
EX_GRAPH2 = {"nodes": set([0,1,2,3,4,5,6,7,8,9]), "edges": set([(0,1),(0,4),(0,5),(1,2),(1,6),(2,7),(2,3),(3,7),(4,1),(5,2),(7,3),(8,1),(8,2),(9,0),(9,4),(9,5),(9,6),(9,7),(9,3)])}

#Function to make complete graph
def make_complete_graph(num_nodes):
    ##Input integer number of notes and return dictionary corresponding to complete directed graph
        nodes = range(0,num_nodes)

        edges = list()
        for item_1 in nodes:
            for item_2 in nodes:
                if not item_1 == item_2:
                    edges.append((item_1, item_2))

        return {"nodes": set(nodes), "edges": set(edges)}

##Part 2: Computing Degree Distributions

def compute_in_degrees(digraph):
    #take dict representation of directed graph and return dict with node: in-degree pairs
    deg_dict = dict()

    #initialize deg_dict with nodes from digraph
    keys = digraph["nodes"]
    for node in keys:
        deg_dict[node]=0

    #loop through edges of digraph and count in-degree
    for node in keys:
        for edge in digraph["edges"]:
            out_edge, in_edge = edge
            if in_edge == node:
                deg_dict[node]+=1

    return deg_dict

def in_degree_distribution(digraph):
    #take dict representation of directed graph 
    dist_dict = dict()
    
    deg_dict = compute_in_degrees(digraph)

    for value in deg_dict.values():
        try:
            dist_dict[value]+=1
        except KeyError:
            dist_dict[value]=1

    return dist_dict
