"""Chapter 4 of Bioinformatics Algorithms Course"""
import itertools, random

def composition(text, k, sort = True):
    """For a string text and an integer k, return all k-mers appearing in
    text (including duplicate k-mers) in lexicographic order"""
    if sort:
        return sorted([text[pos:pos+k] for pos in range(len(text) - k + 1)])
    else:
        return [text[pos:pos+k] for pos in range(len(text) - k + 1)]

def genomepath_to_string(string_collection):
    """For a collection of strings string_collection with overlap between
    each string and the next equal to len(string) - 1, assemble the collection
    into a single string of length len(string_collection) - 1"""
    final_string = string_collection[0]
    for idx in range(1, len(string_collection)):
        final_string += string_collection[idx][-1]
    return final_string

def suffix(string):
    """Return portion of string excluding first letter"""
    return string[1:]

def prefix(string):
    """Return portion of string excluding last letter"""
    return string[:-1]

def overlap_graph(string_collection):
    """For a collection of kmer patterns string_collection, return the
    overlap graph. The overlap graph connects kmers pattern and pattern'
    if suffix(pattern) == prefix(pattern')"""
    adjacency_list = []
    for kmer in string_collection:
        for kmer2 in string_collection:
            if suffix(kmer) == prefix(kmer2):
                adjacency_list.append(kmer + " -> " + kmer2)
    return sorted(adjacency_list)

def precedence(str0, str1):
    """For two strings str0 and str1, return 0 if str0 comes first in
    alphabetical order and 1 if str1 comes first in alphabetical order"""
    return int([str0, str1] != sorted([str0, str1]))
    
def path_graph(text, k):
    adjacency_list = []
    nodes = composition(text, k-1, sort=False)
    edges = composition(text, k, sort=False)
    for node_idx in range(1, len(nodes)):
        adjacency_list.append(nodes[node_idx - 1] + " -> " + nodes[node_idx])
    for idx1, item1 in enumerate(adjacency_list):
        for idx2, item2 in enumerate(adjacency_list):
            if not idx1 == idx2 and item1[0:k-1] == item2[0:k-1]:
                if precedence(item1[k+3:], item2[k+3:]): #if in reverse alpha order
                    #item1 should get added to end of item2
                    adjacency_list[idx2]+= ','+item1[k+3:]
                    adjacency_list.remove(item1)
                else:
                    adjacency_list[idx1]+= ','+item2[k+3:]
                    adjacency_list.remove(item2)
    return sorted(adjacency_list)
                
def composition_graph(text, k):
    adjacency_list = []
    nodes = composition(text, k-1, sort=False)
    edges = composition(text, k, sort=False)
    for node_idx in range(1, len(nodes)):
        adjacency_list.append(nodes[node_idx - 1] + " -> " + nodes[node_idx])
    return adjacency_list

def debruijn(patterns):
    """For a collection of kmers patterns, return the adjacency list of the
    de Bruijn graph"""
    nodes = []
    k = len(patterns[0])
    adjacency_list = []
    for pattern in patterns:
        nodes.extend(composition(pattern, len(pattern)-1))
    nodes = sorted(list(set(nodes)))
    for kmer in patterns:
        for node1 in nodes:
            if node1 == prefix(kmer):
                for node2 in nodes:
                    if node2 == suffix(kmer):
                        adjacency_list.append(node1+' -> '+node2)
                    else:
                        pass
            else:
                pass

    for idx1, item1 in enumerate(adjacency_list):
        for idx2, item2 in enumerate(adjacency_list):
            if not item1==item2 and item1[0:k-1] == item2[0:k-1]:
                if precedence(item1[k+3:], item2[k+3:]): #if in reverse alpha order
                    #item1 should get added to end of item2
                    adjacency_list[idx2]+= ','+item1[k+3:]
                    adjacency_list.remove(item1)
                else:
                    adjacency_list[idx1]+= ','+item2[k+3:]
                    adjacency_list.remove(item2)
    return sorted(adjacency_list)

def debruijn_binary(patterns):
    nodes = []
    k = len(patterns[0])
    adjacency_list = []
    for pattern in patterns:
        nodes.extend(composition(pattern, len(pattern)-1))
    nodes = sorted(list(set(nodes)))
    for kmer in patterns:
        for node1 in nodes:
            if node1 == prefix(kmer):
                for node2 in nodes:
                    if node2 == suffix(kmer):
                        adjacency_list.append(node1+' -> '+node2)
                    else:
                        pass
            else:
                pass
    #print adjacency_list
    for idx1, item1 in enumerate(adjacency_list):
        for idx2, item2 in enumerate(adjacency_list):
            if not item1==item2 and item1[0:k-1] == item2[0:k-1]:
                if precedence(item1[k+3:], item2[k+3:]): #if in reverse alpha order
                    #item1 should get added to end of item2
                    adjacency_list[idx2]+= ','+item1[k+3:]
                    adjacency_list.remove(item1)
                else:
                    adjacency_list[idx1]+= ','+item2[k+3:]
                    adjacency_list.remove(item2)
    return sorted(adjacency_list)

def text_to_graph(filename):
    """Convert text representation of graph (e.g. "0 -> 3\n 1 -> 0,3") into
    an adjacency dictionary where keys represent nodes and values represent
    lists of target nodes."""
    adjacency_dict = {}
    fo = open(filename, 'r')
    for line in fo:
        line_copy = line.strip()
        value = []
        key = int(line[0:line_copy.index('-')-1])    
        line_copy = line_copy[line_copy.index('>')+1:].strip()
        while True:
            try:
                value.append(int(line_copy[0:line_copy.index(',')]))
                line_copy = line_copy[line_copy.index(',')+1:].strip()
            except ValueError:
                value.append(int(line_copy))
                break
        adjacency_dict[key] = value
    fo.close()
    return adjacency_dict

def list_diff(list1, list2):
    """Find any items in list1 that are not in list2"""
    return [x for x in list1 if x not in list2]

def format_eulerian_cycle(cycle_list):
    """Take the list output of eulerian_cycle and format it as node0 -> node1 -> ... -> nodeN"""
    cycle = str(cycle_list[0][0])
    for node in cycle_list[1:]:
        cycle += "->" + str(node[0])
    cycle += "->"+str(cycle_list[-1][-1])
    return cycle

#graph = text_to_graph("graph_example.txt")
#print format_eulerian_cycle(eulerian_cycle("graph_example.txt"))

def eulerian_cycle(graph_filename, add_edge = ()):
    """Form a cycle Cycle by randomly walking in graph without visiting the same
    edge twice. Should be formulated to run in linear time by maintaining the
    current cycle being built as well as the list of unused edges incident to
    each node and the list of nodes on the current cycle that have unused edges."""
    graph = text_to_graph(graph_filename)
    nodes = graph.keys()
    used_edges = []
    all_edges = []
    for k,v in graph.items():
        if len(v) == 1:
            all_edges.append((k,v[0]))
        else:
            v0 = [vi for vi in v]
            for vi in v0:
                all_edges.append((k,vi))
    #add any extra edges and nodes if needed
    if len(add_edge)!=0:
        #print graph[add_edge[0]]
        all_edges.append(add_edge)
        nodes = list(set(nodes).union(add_edge))
        if add_edge[0] in graph.keys():
            graph[add_edge[0]] = graph[add_edge[0]]+[add_edge[1]]
        else:
            graph[add_edge[0]] = [add_edge[1]]

    #randomly choose a start node
    start_node = random.choice(nodes)
    #randomly walk the graph
    while len(used_edges) != len(all_edges):
        try:
            target_node = random.choice(graph[start_node])
            graph[start_node].remove(target_node)
            if graph[start_node] == []: #remove start node if it has no outgoing edges
                del graph[start_node]
            used_edges.append((start_node, target_node))
            start_node = target_node
        except:
            if len(used_edges) == len(all_edges):
                return used_edges
            else:
                break
    print used_edges
    while True:
    #randomly select an entrance point into the graph
        while True:
            try:
                start_node = random.choice(graph.keys()) #start at a random node that still has outgoing edges
                target_node = random.choice(graph[start_node])
                possible_targets = []
                for idx, item in enumerate(used_edges):
                    if item[0] == target_node:
                        possible_targets.append(idx)
                if not possible_targets == []:
                    entrance_point = random.choice(possible_targets)
                    break
            except IndexError:
                #print "err"
                return used_edges
        #enter the graph at the chosen point and traverse along the pre-set path
        graph[start_node].remove(target_node)
        if graph[start_node] == []:
            del graph[start_node]
        new_used_edges = [(start_node, target_node)]
        new_used_edges.extend(used_edges[entrance_point:])
        new_used_edges.extend(used_edges[:entrance_point])
        used_edges = new_used_edges
        #randomly walk further in the graph, if possible
        start_node = used_edges[-1][-1]
        while len(used_edges) != len(all_edges):
            try:
                target_node = random.choice(graph[start_node])
                graph[start_node].remove(target_node)
                if graph[start_node] == []: #remove start node if it has no outgoing edges
                    del graph[start_node]
                used_edges.append((start_node, target_node))
                start_node = target_node
            except:
                break
        #if there are still unused edges, repeat
        if len(used_edges) == len(all_edges):
            return used_edges


def eulerian_path(graph_filename):
    """For a nearly-complete graph, find an Eulerian path starting at one unbalanced node and ending at anohter unbalanced
    node."""
    graph = text_to_graph(graph_filename)
    nodes = set(graph.keys()).union(set([item for sublist in graph.values() for item in sublist])) #need to do this way because graph is not guaranteed to be strongly connected
    #check in and out degree of every node
    degree_dict = {node : [0,0] for node in nodes}
    #[in_degree, out_degree]
    for out_node in graph.keys():
        degree_dict[out_node][1] = len(graph[out_node])
        for in_node in graph[out_node]:
            degree_dict[in_node][0]+=1
    #find the two unbalanced nodes
    for item in degree_dict.keys():
        if degree_dict[item][0]<degree_dict[item][1]:
            needs_in = item
        if degree_dict[item][0]>degree_dict[item][1]:
            needs_out = item
    #add the necessary edge
    extra_edge = (needs_out, needs_in)
    #find the eulerian path
    cycle = eulerian_cycle(graph_filename, add_edge = extra_edge)
    #remove the extra edge and cut open the loop into a straight path
    extra_edge_index = cycle.index(extra_edge)
    new_cycle = cycle[extra_edge_index+1:] + cycle[:extra_edge_index]
    return new_cycle

#cycle = eulerian_path("graph_example.txt")
#cyclef = format_eulerian_cycle(cycle)
#print cyclef

def text_to_graph2(collection_of_strings, binary=False):
    if binary:
        debruj = debruijn_binary(collection_of_strings)
    else:
        debruj = debruijn(collection_of_strings)
    text_graph = {}
    for item in debruj:
        start, end = item[0:item.index('-')].split()[0], [item[item.index('>')+1:].split()[0]]
        end = end[0].split(",")
        end = filter(None, end)
        #print start, end, text_graph
        if start in text_graph.keys():
            text_graph[start] = text_graph[start] + end
        else:
            text_graph[start] = end
    return text_graph

def eulerian_path_text(graph):
    """For a nearly-complete graph, find an Eulerian path starting at one unbalanced node and ending at anohter unbalanced
    node."""
    nodes = set(graph.keys()).union(set([item for sublist in graph.values() for item in sublist])) #need to do this way because graph is not guaranteed to be strongly connected
    #check in and out degree of every node
    degree_dict = {node : [0,0] for node in nodes}
    #[in_degree, out_degree]
    for out_node in graph.keys():
        degree_dict[out_node][1] = len(graph[out_node])
        for in_node in graph[out_node]:
            degree_dict[in_node][0]+=1
    #find the two unbalanced nodes
    for item in degree_dict.keys():
        if degree_dict[item][0]<degree_dict[item][1]:
            needs_in = item
        if degree_dict[item][0]>degree_dict[item][1]:
            needs_out = item
    #add the necessary edge
    extra_edge = (needs_out, needs_in)
    #find the eulerian path
    #print extra_edge
    cycle = eulerian_cycle_text(graph, add_edge = extra_edge)
    #remove the extra edge and cut open the loop into a straight path
    extra_edge_index = cycle.index(extra_edge)
    new_cycle = cycle[extra_edge_index+1:] + cycle[:extra_edge_index]
    return new_cycle

def eulerian_cycle_text(graph, add_edge = ()):
    """Form a cycle Cycle by randomly walking in graph without visiting the same
    edge twice. Should be formulated to run in linear time by maintaining the
    current cycle being built as well as the list of unused edges incident to
    each node and the list of nodes on the current cycle that have unused edges."""
    nodes = graph.keys()
    used_edges = []
    all_edges = []
    for k,v in graph.items():
        if len(v) == 1:
            all_edges.append((k,v[0]))
        else:
            v0 = [vi for vi in v]
            for vi in v0:
                all_edges.append((k,vi))
    #add any extra edges and nodes if needed
    if len(add_edge)!=0:
        all_edges.append(add_edge)
        nodes = list(set(nodes).union(add_edge))
        if add_edge[0] in graph.keys():
            graph[add_edge[0]] = graph[add_edge[0]]+[add_edge[1]]
        else:
            graph[add_edge[0]] = [add_edge[1]]
    #randomly choose a start node
    start_node = random.choice(nodes)
    #print graph, "graph", nodes, "nodes"
    #randomly walk the graph
    while len(used_edges) != len(all_edges):
        try:
            target_node = random.choice(graph[start_node])
            graph[start_node].remove(target_node)
            if graph[start_node] == []: #remove start node if it has no outgoing edges
                del graph[start_node]
            used_edges.append((start_node, target_node))
            start_node = target_node
        except:
            if len(used_edges) == len(all_edges):
                return used_edges
            else:
                break
    #print used_edges
    while True:
    #randomly select an entrance point into the graph
        while True:
            try:
                start_node = random.choice(graph.keys()) #start at a random node that still has outgoing edges
                target_node = random.choice(graph[start_node])
                possible_targets = []
                for idx, item in enumerate(used_edges):
                    if item[0] == target_node:
                        possible_targets.append(idx)
                if not possible_targets == []:
                    entrance_point = random.choice(possible_targets)
                    break
            except IndexError:
                #print "err"
                return used_edges
        #enter the graph at the chosen point and traverse along the pre-set path
        graph[start_node].remove(target_node)
        if graph[start_node] == []:
            del graph[start_node]
        new_used_edges = [(start_node, target_node)]
        new_used_edges.extend(used_edges[entrance_point:])
        new_used_edges.extend(used_edges[:entrance_point])
        used_edges = new_used_edges
        #randomly walk further in the graph, if possible
        start_node = used_edges[-1][-1]
        while len(used_edges) != len(all_edges):
            try:
                target_node = random.choice(graph[start_node])
                graph[start_node].remove(target_node)
                if graph[start_node] == []: #remove start node if it has no outgoing edges
                    del graph[start_node]
                used_edges.append((start_node, target_node))
                start_node = target_node
            except:
                break
        #if there are still unused edges, repeat
        if len(used_edges) == len(all_edges):
            return used_edges

def format_eulerian_text(text_euler_cycle):
    text = text_euler_cycle[0][0]
    for idx in range(1,len(text_euler_cycle)):
        text += text_euler_cycle[idx][0][-1]
    text += text_euler_cycle[-1][-1][-1]
    return text

def nonoverlap(str1, str2):
    """Return any non-overlapping characters between two partially-overlapping strings. If str1==str2,
    return empty string."""
    if str1 == str2:
        return ""
    else:
        for overlap in range(1,len(str1)+1):
            if str1[-overlap:] == str2[0:overlap]:
                pass
            else:
                final_overlap = overlap - 1
                for dummy in range(final_overlap):
                    str1 = str1[:-1]
                #print str1, str2[overlap-1:]
                return str1+str2[overlap-1:]

def format_eulerian_text_binary(text_euler_cycle):
    print text_euler_cycle
    for item in text_euler_cycle:
        if item[0]==item[1]:
            text_euler_cycle.remove(item)
    print text_euler_cycle
    #eliminate reciprocal connections
    removals = []
    for idx in range(len(text_euler_cycle)-1):
        if text_euler_cycle[idx][::-1] == text_euler_cycle[idx+1]:
            removals.append(text_euler_cycle[idx])
            removals.append(text_euler_cycle[idx+1])
    for item in removals:
        text_euler_cycle.remove(item)
    print text_euler_cycle
    text = ""
    for idx in range(0,len(text_euler_cycle)):
        text += text_euler_cycle[idx][0][0]
    text += text_euler_cycle[-1][-1][1:]
    return text

#x = format_eulerian_text(eulerian_path_text(text_to_graph(txt)))

def generate_binary_strings(k):
    """Return all possible binary strings of length k"""
    return sorted([''.join(i) for i in itertools.product('01', repeat=k)])

def universal_binary_circular_string(k):
    txt = generate_binary_strings(k)
    return format_eulerian_text(eulerian_cycle_text(text_to_graph(txt, binary=True)))[0:-k+1]

def paired_composition(k,d,text):
    """Generate all read pairs of length k separated by distance d within a string text"""
    return sorted([(text[pos:pos+k],text[pos+k+d:pos+2*k+d]) for pos in range(len(text) - 2*k - d + 1)])

def format_paired_composition(comp_list):
    str_list = []
    for comp in comp_list:
        str_list.append("("+comp[0]+"|"+comp[1]+")")
    return str_list

def prefix_pair(paired_read):
    k = paired_read.index("|") - paired_read.index("(") - 1
    return paired_read[0:k]+paired_read[k+1:k+1+k]+")"

def suffix_pair(paired_read):
    k = paired_read.index("|") - paired_read.index("(") - 1
    return "("+paired_read[2:k+2]+paired_read[k+3:k+3+k]

def composition_graph_pair(k,d,text):
    edges = format_paired_composition(paired_composition(k,d,text))
    graph = dict()
    for idx1, edge1 in enumerate(edges):
        for idx2, edge2 in enumerate(edges):
            if not idx1 == idx2:
                if suffix_pair(edge1) == prefix_pair(edge2):
                    graph[prefix_pair(edge1)] = prefix_pair(edge2)
    return graph

def debruijn_pair(pair_graph):
    dgraph = {node : [] for node in pair_graph.keys()}
    for k, v in pair_graph.items():
        dgraph[k] = dgraph[k] + [v]
    return dgraph

def debruijn_from_pairs(pair_list):
    pair_tuple_list = [(pair[0:pair.index("|")], pair[pair.index("|")+1:]) for pair in pair_list]
    edges = format_paired_composition(pair_tuple_list)
    graph = dict()
    for idx1, edge1 in enumerate(edges):
        for idx2, edge2 in enumerate(edges):
            if not idx1 == idx2:
                if suffix_pair(edge1) == prefix_pair(edge2):
                    graph[prefix_pair(edge1)] = prefix_pair(edge2)
    dgraph = {node : [] for node in graph.keys()}
    for k, v in graph.items():
        dgraph[k] = dgraph[k] + [v]
    return dgraph

def eulerian_pair_path_to_genome(pair_path):
    genome = ""
    for item in pair_path:
        genome += item[1]
    genome += pair_path[-1][2:pair_path[-1].index("|")]
    genome += pair_path[-2][pair_path[-2].index("|")+1:pair_path[-2].index(")")]
    genome += pair_path[-1][-2]
    return genome

def string_spelled_by_patterns(pattern_list):
    string = ""
    for pat in pattern_list:
        string += pat[0]
    string += pattern_list[-1][1:]
    return string

def string_spelled_by_gapped_patterns(gapped_patterns, k, d):
    first_patterns = [item[1:item.index("|")] for item in gapped_patterns]
    second_patterns = [item[item.index("|")+1:item.index(")")] for item in gapped_patterns]
    prefix_string = string_spelled_by_patterns(first_patterns)
    suffix_string = string_spelled_by_patterns(second_patterns)
    print prefix_string
    print suffix_string
    for i in range(k+d+1, len(prefix_string)):
        if prefix_string[i] != suffix_string[i-k-d]:
            print "there is no string spelled by the gapped patterns"
            return None
    return prefix_string + suffix_string[-(k+d):]

def genome_from_pairs(k,d,pair_list):
    path = eulerian_path_text(debruijn_from_pairs(pair_list))
    print path[-1]
    #print path
    final_path = [p[0] for p in path]
    final_path.append(path[-1][-1])
    #print final_path
    str_final = string_spelled_by_gapped_patterns(final_path, k, d)
    print final_path[-1]
    return str_final

def maximal_nonbranching_paths(graph):
    used_nodes = set([])
    #paths = set([])
    paths = []
    all_nodes = set(graph.keys()).union(set([item for sublist in graph.values() for item in sublist])) #need to do this way because graph is not guaranteed to be strongly connected
    nodes = graph.keys()
    #print nodes
    #check in and out degree of every node
    degree_dict = {node : [0,0] for node in all_nodes}
    #[in_degree, out_degree]
    for out_node in graph.keys():
        degree_dict[out_node][1] = len(graph[out_node])
        for in_node in graph[out_node]:
            degree_dict[in_node][0]+=1
    for node in nodes:
        if not degree_dict[node][0] == degree_dict[node][1] == 1:
            #print node, "branch"
            if degree_dict[node][1] > 0:
                used_nodes = used_nodes.union(set([node]))
                for out in graph[node]:
                    non_branching_path = [(node, out),]
                    used_nodes = used_nodes.union(set([out]))
                    while degree_dict[out][0] == degree_dict[out][1] == 1:
                        non_branching_path.append((out, graph[out][0]))
                        used_nodes = used_nodes.union(set([out]))
                        out = graph[out][0]
                    
                    paths.append(non_branching_path)

    #print paths                    
    #find isolated cycles
    unused_nodes = set(nodes).difference(used_nodes)
    iso_cycle_used_nodes = []
    for node in unused_nodes:
        if not node in iso_cycle_used_nodes:
            if degree_dict[node][0] == degree_dict[node][1] == 1:
                #node is part of an isolated cycle
                start = node
                out = graph[node][0]
                path = [(start, out)]
                iso_cycle_used_nodes.append(start)
                iso_cycle_used_nodes.append(out)
                while degree_dict[start][1] == 1 and not path[0][0] == path[-1][-1]:
                    start = out
                    out = graph[start][0]
                    path.append((start, out))
                    iso_cycle_used_nodes.append(start)
                    iso_cycle_used_nodes.append(out)
                paths.append(path)
    return paths

def path_format_arrows(paths):
    string_list = []
    for item in paths:
        #print item
        string = str(item[0][0])+" -> "
        for sub_item in item[1:]:
            #print sub_item
            string += str(sub_item[0])+" -> "
        #print item[-1][-1][1:], string
        string += str(item[-1][-1])
        string_list.append(string)
    return sorted(string_list)

def path_format_contigs(paths):
    string_list = []
    for item in paths:
        #print item
        string = str(item[0][0][0])
        for sub_item in item[1:]:
            #print sub_item, 'sub'
            string += str(sub_item[0][0][0])
        string += str(item[-1][-1])
        string_list.append(string)
    return sorted(string_list)

#g = maximal_nonbranching_paths(text_to_graph("graph_example.txt"))
#g = path_format(g)
