import random
import sys

sys.setrecursionlimit(20000)

def condense(string):
    """Remove any dash characters from a string and return the string."""
    unwanted = set(["-", " "])
    new_string = ""
    for char in string:
        if char in unwanted:
            pass
        else:
            new_string += char
    return new_string

def transpose(list_of_lists):
    """Matrix transpose a list of lists"""
    return map(list, zip(*list_of_lists))

def recursive_change(money, coins):
    """Recursive algorithm to compute minimum number of coins to return change
    equal to the amount money, for a tuple or list of coin demoninations coins.
    This algorithm is highly inefficient because the same value of money will
    be called over and over again."""
    #print money
    if money == 0:
        return 0
    min_num_coins = float('inf')
    for coin in coins:
        if money >= coin:
            num_coins = recursive_change(money - coin, coins)
            if num_coins + 1 < min_num_coins:
                min_num_coins = num_coins + 1
    return min_num_coins


        
def dynamic_minnumcoins(m_array, final_index, coins):
    while len(m_array) < final_index + 1:
        curr_index = len(m_array)
        min_val = float("inf")
        for denom in coins:
            if m_array[curr_index - denom] < min_val:
                min_val = m_array[curr_index - denom]
        m_array.append(min_val + 1)
    return m_array

def dpchange(money, coins):
    """More efficient dynamic programming implementation of recursive_change."""
    min_num_coins = [0]
    for m in range(1,money+1):
        min_num_coins.append(float("inf"))
        for coin in coins:
            if m >= coin:
                if min_num_coins[m - coin] + 1 < min_num_coins[m]:
                    min_num_coins[m] = min_num_coins[m - coin] + 1
    return min_num_coins[money]
                    

def south_or_east(i,j):
    """Recursive solver for the Manhattan tourist problem. Computes the longest
    path to node (i,j) in a rectangular grid and is based off the observation
    that the only way to reach (i,j) is to go south from (i-1,j) or east
    from (i, j-1). Recall that graph is indexed so top left is (0,0) and bottom
    right is (n,m)."""
    pass

def format_matrix(multiline_string):
    """Turn a multiline string into a matrix (list of lists)"""
    undesired = ("", " ")
    matrix = []
    current_row = []
    for item in multiline_string:
        if not item in undesired:
            if item == "\n":
                matrix.append(current_row)
                current_row = []
            else:
                current_row.append(int(item))
    if len(current_row) > 0:
        matrix.append(current_row)
    return matrix

def zero_matrix(n,m):
    """Create row matrix (list of lists) with n rows and m columns,
    with all entries set to 0."""
    return [[0 for dummy in range(m)] for dummy in range(n)]

def manhattan_tourist(n, m, down, right):
    """For weight matrices down and right, where down[i][j] and right[i][j]
    are the respective weights of the vertical and horizontal edges entering
    node (i,j); and integers n and m; find the longest path from source (0,0)
    to sink (n,m) in the n x m rectangular grid whose edges are defined by the
    matrices down and right."""
    s = zero_matrix(n+1,m+1)
    for i in range(1,n+1):
        s[i][0] = s[i-1][0] + down[i-1][0]
    print s
    for j in range(1,m+1):
        s[0][j] = s[0][j-1] + right[0][j-1]
    print s
    for i in range(1,n+1):
        for j in range(1,m+1):
            s[i][j] = max([s[i-1][j]+down[i-1][j], s[i][j-1]+right[i][j-1]])
    print s
    return s[n][m]


##down = format_matrix("""1 0 4 0 1 4 2 2 1 2 0 2 3 4 0 2 4 3
##4 3 2 4 0 0 0 1 4 3 1 3 3 0 1 2 3 2
##4 1 3 2 0 2 3 2 2 1 4 3 0 3 4 0 4 0
##0 2 2 2 0 4 2 0 2 3 3 4 0 2 3 1 1 4
##4 4 3 0 0 3 4 1 4 1 2 0 2 3 4 3 3 1
##0 0 0 0 2 2 4 1 4 3 1 3 1 1 4 2 0 1
##4 1 1 3 2 1 1 1 4 3 3 0 2 3 3 1 4 3
##4 1 1 1 0 1 3 4 0 4 1 4 2 0 3 1 4 3
##4 0 1 1 0 3 4 3 4 1 2 0 3 2 1 3 0 2
##4 2 2 2 0 1 3 3 3 1 0 2 0 1 0 4 0 2
##2 0 4 1 1 0 4 3 1 1 1 4 1 3 3 1 1 2""")
##right = format_matrix("""4 0 1 4 0 0 3 0 3 0 0 4 1 4 1 1 4
##1 4 2 2 3 1 2 3 4 1 2 2 2 2 2 0 0
##2 0 4 2 4 3 4 3 4 3 1 4 0 1 1 4 4
##0 0 0 1 0 4 1 1 0 3 2 4 0 2 0 3 1
##2 0 4 3 2 2 2 3 1 2 1 0 1 2 1 3 1
##4 2 0 1 2 2 3 2 0 4 0 4 3 2 2 1 3
##1 4 4 4 1 4 4 3 4 1 3 0 4 3 2 4 4
##1 1 4 2 0 1 4 4 4 4 1 0 2 2 1 2 0
##1 0 4 2 0 2 3 0 3 4 1 4 3 4 2 3 1
##1 0 1 0 0 3 2 0 0 2 2 0 2 0 3 1 2
##2 2 1 1 3 0 2 1 1 4 4 3 0 4 0 2 2
##2 3 4 4 2 1 4 1 0 4 1 1 4 0 1 1 3""")
##print manhattan_tourist(11,17,down,right)

def nodes_with_indegree_zero(graph):
    """Given a dict() representation of a graph, return a set of all nodes
    with no incoming edges."""
    candidate_nodes = graph.keys()
    values = [item for sublist in graph.values() for item in sublist]
    for v in values:
        if v in candidate_nodes:
            candidate_nodes.remove(v)
    return list(set(candidate_nodes))

def indegree(graph, node):
    """Return indegree of given node"""
    return [item for sublist in graph.values() for item in sublist].count(node)

def topological_ordering(graph):
    """Reconstruct a graph into a topological ordering of nodes. Relies on fact
    that any directed acyclic graph (DAG) will have a node with no incoming edges.
    Remove this node from the graph, along with all of its edges,s process iteratively."""
    node_list = []
    candidates = nodes_with_indegree_zero(graph)
    while len(candidates) > 0:
        a = random.choice(candidates)
        node_list.append(a)
        candidates.remove(a)
        if not graph[a] == []:
            edge_list = graph[a]
            for edge in edge_list:
                if indegree(graph, edge) == 1:
                    candidates.append(edge)
            graph[a] = []
        else:
           node_list.append(a)     
    if len([item for sublist in graph.values() for item in sublist]) > 0:
        return "the input graph is not a DAG"
    else:
        return node_list

def lcs_backtrack(v,w):
    s = zero_matrix(len(v)+1, len(w)+1)
    backtrack = zero_matrix(len(v)+1, len(w)+1)
    #first construct the DAG corresponding to the two sequences
    for i in range(1, len(v)+1):
        for j in range(1, len(w)+1):
            if v[i-1] == w[j-1]:
                s[i][j] = max([s[i-1][j], s[i][j-1], s[i-1][j-1] + 1])
            else:
                s[i][j] = max([s[i-1][j], s[i][j-1]])

            #now keep track of which edge was traversed
            if s[i][j] == s[i-1][j-1]+1 and v[i-1] == w[j-1]:
                backtrack[i][j] = "diag"
            elif s[i][j] == s[i-1][j]:
                backtrack[i][j] = "down"
            else:
                backtrack[i][j] = "right"
##    for i in s:
##        print i
    return backtrack

def output_lcs(backtrack, v, i, j):
    """For backtrack matrix backtrack, output a LCS between the i-prefix of v and the
    j-prefix of w."""
    #print "call", i, j
    if i == 0 or j == 0:
        return ""
    else:
        if backtrack[i][j] == "diag":
            return output_lcs(backtrack, v, i-1, j-1) + v[i-1]
        elif backtrack[i][j] == "right":
            return output_lcs(backtrack, v, i, j-1)
        elif backtrack[i][j] == "down":
            return output_lcs(backtrack, v, i-1, j)

v, w = "AGGCCT", "TAGGCC"
print output_lcs(lcs_backtrack(v,w), v, len(v), len(w))
print output_lcs(lcs_backtrack(w,v), w, len(w), len(v))

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
    for item in list(set([item for sublist in adjacency_dict.values() for item in sublist])):
        if not item in adjacency_dict.keys():
            adjacency_dict[item] = []
    return adjacency_dict

g = text_to_graph("graph_example.txt")
candidates = nodes_with_indegree_zero(g)
#print topological_ordering(g)

#v should be shorter sequence
#v = "GACTGCGCCAGACGACCTTGCGGCAAGCGGAACACGATGTGGCTAGGTGTAAGTCCATTCCACACATTAACACGAATTTGACGATACTGGGAAATTACCAAATAGGCCCACGCGGTGAACGGATCACCGGCCCTAGAATCACTTACTTCCTAAATCACTATTAGCAAAGGACCAGACAGGGTATAGCGAGGCCCATTACACAGACTGTATTACATTTGAGAATGTATGGCTAATAGATACTATCAATTGATAGAGCGAAAAAGGTTGCAGCCCCAACGTGGAACCCAAATAATTGTTGTGGGGCATGGTTCTATAACGTACTCGGAGAGGATTCAGATGTAAGCCCGTACTATGCTGCTAACCAACCGAAATTTGATTACTATCCTGGATTGGTTTGGACGACTGGTGGAGTTGCTCCTCATAGCTCGTGTAATTACGTAATACTCTTCGTATTACCGCTACCCGGTGGGGCAAAGACCCTGTATCTTCGTCGAGTCTGCAGTGCTACTTACGAAACTGGATCGCGCGAAGTTATCTGAGCAGGCGAAAGTGTAAATGCCACTCTTGCAGGGGTTGCCGGGCGACTTCTTCTCGAATCTTTAAAAGGGCGGTACATGGGTGTTAAGGCTTCCACACGGTGTCTCGTCGGACCGTCCTTGAGCGCAGAACTCATGAGTTGTTTCGCACGCGACAGAATGGTCCTTCACACTGATACGAGGCCTTCGGCAATTCTCGCTGGTGCTTATCAGTAACGGCGAATGTTCTCAGCGTATTTTTGGAGGAATTTTCGCGGTGTTTCTCCCTGTTGACTAAAATCCTAAC"
#w = "GAGCAAAAGCCACTTACCACGTCCTATCTTCTGGGGGTAACTTATACTGCTGCTATGTAGAAGTACATGGAATCAATCAGAGTCGCTTTCGTGGAGAGTCGACTGGACAAATTTTACGCTCTGAGCGACGTCATGCGTGACAGAATGCTTCTACAAGGAACACCGTTCTTGGCTCGGTCTCGCCCCGCGCTTGCTTCATACATTGCAGGCGGATAAATCGCCTTCACATGGTAGGCCGGTCCACCGGTCTCTCCCCGTGTGCATACGAGGAATGTTATGTGTCGGGGTCAGGTATCGTTACATATAGCGGTATTGTAGGATTTGGGCGTTGATAGTTAGGTAAACTAACGAATACCGGATAGGTGATGCCTCGTTAACTAACCACGGCCAATGGAAGCCGACGGTGTTCCGTGGCTTCTTAAGGCAGGGCTTAGCTACTAGACACTGCCCGCAGATATTACCGGTGGGTGATTAATGTGGTGTCGTTGTGCGCACCTATACCAGACGGCCCATTTGCCTAGTTGCATACCGCGTGGCTGGCACCCCGACAAATTCTTCCACACCTCAACCGGCGACATCCGCCAGTAGGTGCCACCCAGTACAAGGATTCCGATATGGGCTATGGTAGTTCTAGCGACAGACCCTCCTGGGAGTGTGTCCGCTCCATCAGGTCAGCGCAGGCGATGTTTGGAAGGCGACTTGTCCATCATAGTATTCGGCCATAGTGATCTTCTACCTGAACATGTTCGCCGTAAAAAAGCGAGACGGTTATTACGTTTAATAACCCTGGAGGCAGTAAATCACTTCAAAAGCACATCTGATGTGCCAAACTAAGCGAACTGTCGAAGGGCCATGCTACACTAAGTGATTTAAAAGGCTACTACTGGTCCTTGGAGTAGCCGTAGCTTGCGTAAACACCGCCCCATGCCTAATTCTTTACAACTTGCAACGTGCCATCTCGCTGTAGGCGGCCAAAGAATGCCGGTT"

#back = lcs_backtrack(v,w)
##for i in back:
##    print i
#x = output_lcs(back, v, len(back)-1, len(back[0])-1)

def max_node(graph):
    return max(graph.keys())

def format_DAG_by_endnode(graph):
    """Take list of node->node:weight strings and create a dictionary keyed
    by the ending node."""
    graph_dict = {}
    for line in graph:
        end_node = int(line[line.index(">")+1:line.index(":")])
        start_node = int(line[0:line.index("-")])
        weight = int(line[line.index(":")+1:])
        if end_node in graph_dict.keys():
            graph_dict[end_node].append((start_node, end_node, weight))
        else:
            graph_dict[end_node] = [(start_node, end_node, weight)]
    return graph_dict

def format_DAG_by_startnode(graph):
    graph_dict = {}
    for line in graph:
        end_node = int(line[line.index(">")+1:line.index(":")])
        start_node = int(line[0:line.index("-")])
        weight = int(line[line.index(":")+1:])
        if start_node in graph_dict.keys():
            graph_dict[start_node].append((start_node, end_node, weight))
        else:
            graph_dict[start_node] = [(start_node, end_node, weight)]
    return graph_dict

def longest_path_DAG(graph_list, source_idx, sink_idx):
    """Find an LCS, and the length of the LCS, in any directed acyclic graph.
    Graph should be formatted as list of strings of start_node->end_node:weight,
    in increasing order of end_node, e.g.:
    ['0->1:7', '0->2:4', '2->3:2', '1->4:1', '3->4:3']"""
    #s = zero_matrix(max_node(graph)+1, max_node(graph)+1)
    s = {}
    backtrack = {}
    s[source_idx] = 0
    backtrack = {}
    graph = format_DAG_by_endnode(graph_list)
    s = {node : 0 for node in range(source_idx, sink_idx+1)}
    
    graph = format_DAG_by_startnode(graph_list)
    queue = []

    for item in graph[source_idx]:
        backtrack[item[1]] = item[0]
        s[item[1]] = item[2]
        queue.append(item[1])

    print queue
    print graph
    while not len(queue) == 0:
        current = queue.pop()
        if not current in graph.keys():
            pass #this node is a dead-end
        else:
            for item in graph[current]:
                queue.append(item[1])
                if s[item[1]] < s[item[0]]+item[2]:
                    s[item[1]] = s[item[0]] + item[2]
                    backtrack[item[1]] = item[0]
                else:
                    pass #there is already a better way to reach this node
                
##    for end_node in sorted(graph.keys()):
##            current_max = float("-inf")
##            current_edge = None
##            for edge_tup in graph[end_node]:
##                if edge_tup[2] > current_max:
##                    current_max = edge_tup[2]
##                    current_edge = edge_tup[0]
##                    s[end_node] = current_max + s[current_edge]
##                    backtrack[end_node] = current_edge
    print s
    print backtrack
    lcs_length = s[sink_idx]
    lcs = "->"+str(sink_idx)
    start_pos = sink_idx
    while not lcs[0:lcs.index("-")] == str(source_idx):
        start_pos = backtrack[start_pos]
        lcs = str(start_pos) + "->" + lcs

    return lcs, lcs_length

##print longest_path_DAG("""0->1:5
##0->2:6
##0->3:5
##1->2:2
##1->5:9
##2->4:4
##2->5:3
##2->6:7
##3->4:4
##3->5:5
##4->6:2
##5->6:1""", 'a', 'g')
    
##print longest_path_DAG("""0->1:7
##     0->2:4
##     2->3:2
##     1->4:1
##     3->4:3""".split(),0,4)

##x = longest_path_DAG(sorted("""24->31:7
##24->30:19
##17->38:35
##24->42:34
##24->39:26
##2->5:16
##12->39:22
##4->24:37
##16->28:5
##16->20:31
##20->37:14
##19->28:25
##26->36:12
##9->32:0
##2->38:22
##15->32:23
##11->15:23
##22->38:33
##11->13:15
##3->25:27
##23->26:28
##1->31:36
##6->15:37
##34->38:33
##4->5:9
##6->11:2
##1->17:12
##38->40:14
##0->13:25
##22->42:21
##25->31:28
##19->33:11
##30->32:1
##20->28:18
##20->29:15
##13->24:11
##31->33:17
##20->22:31
##6->16:36
##16->35:11
##15->42:38
##13->42:12
##14->18:18
##1->6:23
##18->25:13
##3->32:10
##1->40:19
##3->14:38
##1->29:32
##8->11:18
##1->22:1
##8->39:23
##5->6:2
##4->40:25
##11->42:20""".split()), 3, 33)

# v = short_sequence
# w = long_sequence
BLOSUM_COLS = "A  C  D  E  F  G  H  I  K  L  M  N  P  Q  R  S  T  V  W  Y".split()
BLOSUM = {'A':  [4,0,-2, -1, -2,  0, -2, -1, -1, -1, -1, -2, -1, -1, -1,  1,  0,  0, -3, -2],
'C':  [0,  9, -3, -4, -2, -3, -3, -1, -3, -1, -1, -3, -3, -3, -3, -1, -1, -1, -2, -2],
'D': [-2, -3,  6,  2, -3, -1, -1, -3, -1, -4, -3,  1, -1,  0, -2,  0, -1, -3, -4, -3],
'E': [-1, -4,  2,  5, -3, -2,  0, -3,  1, -3, -2,  0, -1,  2,  0,  0, -1, -2, -3, -2],
'F': [-2, -2, -3, -3,  6, -3, -1,  0, -3,  0,  0, -3, -4, -3, -3, -2, -2, -1,  1,  3],
'G': [0, -3, -1, -2, -3,  6, -2, -4, -2, -4, -3,  0, -2, -2, -2,  0, -2, -3, -2, -3],
'H': [-2, -3, -1,  0, -1, -2,  8, -3, -1, -3, -2,  1, -2,  0,  0, -1, -2, -3, -2,  2],
'I': [-1, -1, -3, -3,  0, -4, -3,  4, -3,  2,  1, -3, -3, -3, -3, -2, -1,  3, -3, -1],
'K': [-1, -3, -1,  1, -3, -2, -1, -3,  5, -2, -1,  0, -1,  1,  2,  0, -1, -2, -3, -2],
'L': [-1, -1, -4, -3,  0, -4, -3,  2, -2,  4,  2, -3, -3, -2, -2, -2, -1,  1, -2, -1],
'M': [-1, -1, -3, -2,  0, -3, -2,  1, -1,  2,  5, -2, -2,  0, -1, -1, -1,  1, -1, -1],
'N': [-2, -3,  1,  0, -3,  0,  1, -3,  0, -3, -2,  6, -2,  0,  0,  1,  0, -3, -4, -2],
'P': [-1, -3, -1, -1, -4, -2, -2, -3, -1, -3, -2, -2,  7, -1, -2, -1, -1, -2, -4, -3],
'Q': [-1, -3,  0,  2, -3, -2,  0, -3,  1, -2,  0,  0, -1,  5,  1,  0, -1, -2, -2, -1],
'R': [-1, -3, -2,  0, -3, -2,  0, -3,  2, -2, -1,  0, -2,  1,  5, -1, -1, -3, -3, -2],
'S':  [1, -1,  0,  0, -2,  0, -1, -2,  0, -2, -1,  1, -1,  0, -1,  4,  1, -2, -3, -2],
'T':  [0, -1, -1, -1, -2, -2, -2, -1, -1, -1, -1,  0, -1, -1, -1,  1,  5,  0, -2, -2],
'V':  [0, -1, -3, -2, -1, -3, -3,  3, -2,  1,  1, -3, -2, -2, -3, -2,  0,  4, -3, -1],
'W': [-3, -2, -4, -3,  1, -2, -2, -3, -3, -2, -1, -4, -4, -2, -3, -3, -2, -3, 11,  2],
'Y': [-2, -2, -3, -2,  3, -3,  2, -1, -2, -1, -1, -2, -3, -1, -2, -2, -2, -1,  2,  7]}
for key in BLOSUM.keys():
    val = BLOSUM[key]
    new_val = {k : val[idx] for idx, k in enumerate(BLOSUM_COLS)}
    BLOSUM[key] = new_val

PAM_COLS = "A  C  D  E  F  G  H  I  K  L  M  N  P  Q  R  S  T  V  W  Y".split()
PAM = {'A': [2, -2,  0,  0, -3,  1, -1, -1, -1, -2, -1,  0,  1,  0, -2,  1,  1,  0, -6, -3],
'C': [-2, 12, -5, -5, -4, -3, -3, -2, -5, -6, -5, -4, -3, -5, -4,  0, -2, -2, -8,  0],
'D': [0, -5,  4,  3, -6,  1,  1, -2,  0, -4, -3,  2, -1,  2, -1,  0,  0, -2, -7, -4],
'E':  [0, -5,  3,  4, -5,  0,  1, -2,  0, -3, -2,  1, -1,  2, -1,  0,  0, -2, -7, -4],
'F': [-3, -4, -6, -5,  9, -5, -2,  1, -5,  2,  0, -3, -5, -5, -4, -3, -3, -1,  0,  7],
'G':  [1, -3,  1,  0, -5,  5, -2, -3, -2, -4, -3,  0,  0, -1, -3,  1,  0, -1, -7, -5],
'H': [-1, -3,  1,  1, -2, -2,  6, -2,  0, -2, -2,  2,  0,  3,  2, -1, -1, -2, -3,  0],
'I': [-1, -2, -2, -2,  1, -3, -2,  5, -2,  2,  2, -2, -2, -2, -2, -1,  0,  4, -5, -1],
'K': [-1, -5,  0,  0, -5, -2,  0, -2,  5, -3,  0,  1, -1,  1,  3,  0,  0, -2, -3, -4],
'L': [-2, -6, -4, -3,  2, -4, -2,  2, -3,  6,  4, -3, -3, -2, -3, -3, -2,  2, -2, -1],
'M': [-1, -5, -3, -2,  0, -3, -2,  2,  0,  4,  6, -2, -2, -1,  0, -2, -1,  2, -4, -2],
'N':  [0, -4,  2,  1, -3,  0,  2, -2,  1, -3, -2,  2,  0,  1,  0,  1,  0, -2, -4, -2],
'P':  [1, -3, -1, -1, -5,  0,  0, -2, -1, -3, -2,  0,  6,  0,  0,  1,  0, -1, -6, -5],
'Q':  [0, -5,  2,  2, -5, -1,  3, -2,  1, -2, -1,  1,  0,  4,  1, -1, -1, -2, -5, -4],
'R': [-2, -4, -1, -1, -4, -3,  2, -2,  3, -3,  0,  0,  0,  1,  6,  0, -1, -2,  2, -4],
'S':  [1,  0,  0,  0, -3,  1, -1, -1,  0, -3, -2,  1,  1, -1,  0,  2,  1, -1, -2, -3],
'T':  [1, -2,  0,  0, -3,  0, -1,  0,  0, -2, -1,  0,  0, -1, -1,  1,  3,  0, -5, -3],
'V':  [0, -2, -2, -2, -1, -1, -2,  4, -2,  2,  2, -2, -1, -2, -2, -1,  0,  4, -6, -2],
'W': [-6, -8, -7, -7,  0, -7, -3, -5, -3, -2, -4, -4, -6, -5,  2, -2, -5, -6, 17,  0],
'Y': [-3,  0, -4, -4,  7, -5,  0, -1, -4, -1, -2, -2, -5, -4, -4, -3, -3, -2,  0, 10]}
for key in PAM.keys():
    val = PAM[key]
    new_val = {k : val[idx] for idx, k in enumerate(PAM_COLS)}
    PAM[key] = new_val

def lcs_backtrack_penalized(v,w, penalty_matrix = BLOSUM, indel_penalty = 5):
    """v is shorter sequence and forms rows"""
    s = zero_matrix(len(v)+1, len(w)+1)
    #initialize first row/ column to 0, -5, -10, etc. instead of 0,0,0...
    for idx, item in enumerate(s[0]):
        s[0][idx] = idx * -1 * indel_penalty
    for idx, row in enumerate(s):
        s[idx][0] = idx * -1 * indel_penalty
    backtrack = zero_matrix(len(v)+1, len(w)+1)
    #first construct the DAG corresponding to the two sequences
    for i in range(1, len(v)+1):
        for j in range(1, len(w)+1):
            s[i][j] = max([s[i-1][j] - indel_penalty, s[i][j-1] - indel_penalty, s[i-1][j-1] + penalty_matrix[v[i-1]][w[j-1]]])
            #now keep track of which edge was traversed
            if s[i][j] == s[i-1][j-1]+penalty_matrix[v[i-1]][w[j-1]]:
                backtrack[i][j] = "diag"
            elif s[i][j] == s[i-1][j] - indel_penalty:
                backtrack[i][j] = "down"
            elif s[i][j] == s[i][j-1] - indel_penalty:
                backtrack[i][j] = "right"
            else:
                raise ValueError, "Matrix value does not match neighbors"

##    for i in s:
##        print i
    print "Alignment score", s[-1][-1]
    return backtrack


def output_lcs_penalized(backtrack, v, i, j):
    """For backtrack matrix backtrack, output a LCS between the i-prefix of v and the
    j-prefix of w."""

    if i == 0 and j == 0:
        return ""
    elif i == 0:
        return output_lcs_penalized(backtrack, v, i, j-1) + "-"
    elif j == 0:
        return output_lcs_penalized(backtrack, v, i-1, j) + v[i-1]
    else:
        if backtrack[i][j] == "diag":
            return output_lcs_penalized(backtrack, v, i-1, j-1) + v[i-1]
        elif backtrack[i][j] == "right":
            return output_lcs_penalized(backtrack, v, i, j-1) + "-"
        elif backtrack[i][j] == "down":
            return output_lcs_penalized(backtrack, v, i-1, j) + v[i-1] #seems to work
        

#v = "WQEKAVDGTVPSRHQYREKEDRQGNEIGKEFRRGPQVCEYSCNSHSCGWMPIFCIVCMSYVAFYCGLEYPMSRKTAKSQFIEWCDWFCFNHWTNWAPLSIVRTSVAFAVWGHCWYPCGGVCKTNRCKDDFCGRWRKALFAEGPRDWKCCKNDLQNWNPQYSQGTRNTKRMVATTNQTMIEWKQSHIFETWLFCHVIIEYNWSAFWMWMNRNEAFNSIIKSGYPKLLLTQYPLSQGSTPIVKPLIRRDQGKFWAWAQMWWFREPTNIPTADYCHSWWQSRADLQNDRDMGPEADASFYVEFWYWVRCAARTYGQQLGIIWNNRLKTRNPCPYSADGIQNKENYVFWWKNMCTKSHIAFYYCLQNVAHYTHDVTAEFNPVKCIDWLQGHMVLSSWFKYNTECKKLFVHEKCECYRMFCGVVEDIFGVRFHTGWKHLSTAKPVPHVCVYNPSVQERRNINDFYIFYEIAPAVKNLVLSAQPLHDYTKKCAFNYTPITITRIISTRNQIIWAHVVIACQFYSPHQMLLIELAMDKYCADMNVRRSTEGHQPMHACRSTFGPGMAAKEPLVTFTLVAFWQWPNHEFQYVYMYTEDKIIQIGPHLSNGCEMVEYCVDCYAKRPCYRAYSAEAQYWRMITEAEDYSYKTRNAIAATATVRGQYCHPFRWLGIVWMAHHDCFFANECGTICIPQMAEMRPPETTPYEIDIIFMMFWKEHMSTTILDVVGMYRPATFSHWHDAHHQCEPYLTPLMCQSKLVFDAAFTQVGVKGVWYHTEKLELMAGFNHMKFKKEEAQQSCFYWFQDCPDYDPPDAVRKTDEKHIRAHGEIWWLMRYYCMYHILHIASRHEWMHLRWDQACTNPGYELFEFIPWVLRRYVVYDKIRYNYSYRNSASMEFV"
#w = "AMTAFRYRQGNPRYVKHFAYEIRLSHIWLLTQMPWEFVMGIKMPEDVFQHWRVYSVCTAEPMRSDETYEQKPKPMAKWSGMTIMYQAGIIRQPPRGDRGVSDRNYSQCGKQNQAQLDNNPTWTKYEIEWRVQILPPGAGVFEGDNGQNQCLCPNWAWEQPCQWGALHSNEQYPNRIHLWAPMSKLHIKIEKSSYNRNAQFPNRCMYECEFPSYREQVDSCHYENVQIAFTIFSGAEQKRKFCSCHFWSNFIDQAVFSTGLIPWCYRRDDHSAFFMPNWNKQYKHPQLQFRVAGEGTQCRPFYTREMFTKVSAWRIAGRFAGPYERHHDAHLELWYQHHKVRTGQQLGIIWNNRDKTRNPCPFSAYYNKLPWWKINQNAFYNCLQNIAHSTHDETHEFNPVKCIDWLQGTMVPTECKKGFVHEKCECYRNPGPPLHDMYHQMEDIFGVRFDCLTGWKHLSDYNPCQERRNINDFYIFAYEIAPAVKNLVLSPQPLADATKKCAFNYTPLDQSPVVIACKWYIHQPICMLLIVLICAMDKYNAHMIVIRTTEGQQPMHACRMTEGPGMCMKEPLVTFTLPAQWQWPNHEFKYVYMYVLNYHLSQYTYTDEGHAGGQHYSFNVAVDVGMAWGHNRCYCQPACYSQQETQTRTIDYEKWQYMKHQAFKWGLWFCEQERHAWFKGQNRCEMFTAKMTRMGADSNLDQYKLMLAQNYEEQWEQPIMECGMSEIIEIDPPYRSELIFTFWPFCTYSPWQNLIKCRCNNVIEEMDQCVPLTFIGFGVKQAGGIQAWAFYKEEWTSTYYLMCQCMKSDKAQYPYEIILFWMQPMDTGEQEPPQQNMWIFLPHSWFFDWCCNAPWSEICSSRHDHGQCQDAFYPCELFTVFDDIFTAEPVVCSCFYDDPM"
#w = "PENALTY"
#v = "MEANLY"

##w = "WECCTQAIARNLNKCWLKDFPESREVCRDVYRVYQGKQEPFQYRADNCHHCHRKALIELMWKRTNVLPPCNWGLMDWYRKVTFAVTWKTNPLWDDGDYEWFQQDFGRWWIRSRDGSVCINIGKESCHICRHHQGWKRNYSPSYVPHDVPEEHKPDSQMPEIFVLHMCAQQPFHQCVTWLYHAWWPCVSRALQICWWWHNSCPAMWNKSYSETDWFYYMCNFVAIHGRHVIVRVHTHTTEHHCLAREMSEQLFTEWQCAITKWLVVTMWCEARWPKAVGIQPAPFFVYAEYCNIFKGMRPKKRCQKQYHNKECPECNWGICVPIDMEWEQLERHYSEGWDPNTMDLVQDCHMCWFSTYCPCESRYKYYIPWYKVVRVDCWNYTGYHKWVWFANCKTSGWPSRQFDLFTVWNSCRRWRDGKSTQVHGRMTFRMSKLHYKSKCCQNLACGHFAYYLAEGEKPLFLPNFLEKPSHHQCFWSVSCYARKYNKDQHSIMRFMSQICLACFYWFTSQPQCFKEHLKSHPIYIPWSPILQENMMVDYLFLNWYLIIHKLEVYGWRGSEHTWVTPMVTFSKPNGVAIIVVQTYQLRAGYLSYSTAFFIGVTMRMNTYGEFCPGRKDFGSCHKGWGTAIFRQSGEPMVQMLRRTIFWLKRWKGSFGMWLNTTDEQQFTWTDNCALRITTWFHMFCAAKSCEEGLDQANRCFHIIRWECPLPPICWRPHFHSIFKEVLDPWDVTVCPISTCQDGTDGWSNFSWTMHQMQYDQIGPIYTSELENSEHECEKEGSYVPIEISAMWQGICIFNPEIEMLCTYAGYNFKMIYAPNWRCAQLIFAINKGEFQQKGILWALVTVSQDWKYCAWPYMMCYLTKGVQILPDSCSFRLCHWRTPSPKMQWVERPEQRLNI"
##v = "GLKRYEAYELAPLTQFGFVVYRYTCNSWSSSASMFRWMKDTKAVVKRYWPEQWFGHCHYRCMSFMVWWGGNMSCQPVYFMLMMGEALEAGDFGIPVFHEKRWDRMTGNLCPWMIHFIWRHQTNEGWWGEKVTDVHKNCSHNIKHQCCIYFPVRKDKLNISFPDSKMGVEILQCDMQLFRICQQPNQVVIDVMQKQVKWWSVAFMELNSVKQKYANNNRGEHAFNPDTGVKRCLVRFHLNEHHCAAREMSEFTEWQCAITNWLVETTQWCEDRFPKFVGIQPAPYAEYCNIFAQGMRPKKRCQKQYHCKECPRSQCYPWGICVPIMHYCRSMEWEQLTRWYSEGWDPNQMMLVIDCHMCWFSYYCPCEFCNWRCVRYGRPYYIPWYKVVRVDCWNYTGYHKWVSFANCKTDLHTVWNPCWRDGKSTQVHGRMTFRMSKLHYKSCLQNLACGHFAYYELTAEGEKPLFIPNFLEKPSCYARKRFMSQICLACFYWWTSQPQCFKEHLLRKSHNIYCPWSPIVQFVIYNMMVDYLFLNEQYGWRGLEVQTWVTPMVTFHACAYSTCAKPNGVAIIVVQTYQLRAGYLSYSTNFFIGDTHCVIKQRMNTFCPQWYSFGICREVSIISHTCSFTCLRVVVNHYYLSGKFMIFAHFMDCSQMFWANVVFAERIHGDYMDPQTQVGFDTPTMLAYIDKSCIFTQHPCMPYHEMHGHQPIKYYLVWMVWDSGNDSDRVVFAFYETAGQWKGLATWESTFNNYKQKTAEYPQTRVPCQSYMGKQFTQQHAKNRKVASWEVGYDHHWKVSSLNEHRAGHCGKGQHINNDWRDMALTEAMEFPEPEPFIHGLKMGKAEPNSMLSAWIGQPNHRPCWLGREGTGQESYRKDDRKMGMAMGRGQ"

#back = lcs_backtrack_penalized(v, w)
#V = output_lcs_penalized(lcs_backtrack_penalized(v, w), v, len(v), len(w))



#can run the algorithm on backtrack matrix transpose to get W
#w_back = transpose(back)
#W = output_lcs_penalized(lcs_backtrack_penalized(w, v), w, len(w), len(v))

def lcs_backtrack_penalized_local(v,w, penalty_matrix = PAM, indel_penalty = 5):
    """v is shorter sequence and forms rows"""
    s = zero_matrix(len(v)+1, len(w)+1)
    #initialize first row/ column to 0, -5, -10, etc. instead of 0,0,0...
    for idx, item in enumerate(s[0]):
        #s[0][idx] = idx * -1 * indel_penalty
        s[0][idx] = 0
    for idx, row in enumerate(s):
        #s[idx][0] = idx * -1 * indel_penalty
        s[idx][0] = 0
    backtrack = zero_matrix(len(v)+1, len(w)+1)
    #first construct the DAG corresponding to the two sequences
    for i in range(1, len(v)+1):
        for j in range(1, len(w)+1):
            s[i][j] = max([s[i-1][j] - indel_penalty, s[i][j-1] - indel_penalty, s[i-1][j-1] + penalty_matrix[v[i-1]][w[j-1]], 0])
            #now keep track of which edge was traversed
            if s[i][j] == s[i-1][j-1]+penalty_matrix[v[i-1]][w[j-1]]:
                backtrack[i][j] = "diag"
            elif s[i][j] == 0:
                backtrack[i][j] = "taxi"
            elif s[i][j] == s[i-1][j] - indel_penalty:
                backtrack[i][j] = "down"
            elif s[i][j] == s[i][j-1] - indel_penalty:
                backtrack[i][j] = "right"
            
            else:
                raise ValueError, "Matrix value does not match neighbors"
    #print s
    ##top score is not necessarily bottom right; need to find value
    max_score = float("-inf")
    best_indices = (None, None)
    for idx1 in range(len(s)):
        for idx2 in range(len(s[0])):
            if s[idx1][idx2] > max_score:
                max_score = s[idx1][idx2]
                best_indices = (idx1, idx2)
    print "Alignment score", max_score
    return backtrack, best_indices

##back = lcs_backtrack_penalized_local(v,w)

def output_lcs_penalized_local(backtrack, v, i, j):
    """For backtrack matrix backtrack, output a LCS between the i-prefix of v and the
    j-prefix of w."""
    ##key difference is that we need to backtrack from the highest-scoring node
    ##not necessarily the bottom right node
    print i, j
    if i == 0 and j == 0 or backtrack[i][j] == "taxi":
        return ""
    elif i == 0:
        return output_lcs_penalized_local(backtrack, v, i, j-1) + "-"
    elif j == 0:
        return output_lcs_penalized_local(backtrack, v, i-1, j) + v[i-1]
    else:
        if backtrack[i][j] == "diag":
            return output_lcs_penalized_local(backtrack, v, i-1, j-1) + v[i-1]
        elif backtrack[i][j] == "taxi":
            return output_lcs_penalized_local(backtrack, v, 0, 0)
        elif backtrack[i][j] == "right":
            return output_lcs_penalized_local(backtrack, v, i, j-1) + "-"
        elif backtrack[i][j] == "down":
            return output_lcs_penalized_local(backtrack, v, i-1, j) + v[i-1]

##back = lcs_backtrack_penalized_local(v,w)[0]
##best_coords = lcs_backtrack_penalized_local(v,w)[1]
##print best_coords
##V = output_lcs_penalized_local(back, v, best_coords[0], best_coords[1])
##back = lcs_backtrack_penalized_local(w,v)[0]
##print best_coords
##W = output_lcs_penalized_local(back, w, best_coords[1], best_coords[0])

def edit_distance(v,w, match_score = 0, indel_penalty = 1, mismatch_penalty = 1):
    """v is shorter sequence and forms rows"""
    s = zero_matrix(len(v)+1, len(w)+1)
    #initialize first row/ column to 0, -5, -10, etc. instead of 0,0,0...
    for idx, item in enumerate(s[0]):
        s[0][idx] = idx * -1 * indel_penalty
    for idx, row in enumerate(s):
        s[idx][0] = idx * -1 * indel_penalty
    backtrack = zero_matrix(len(v)+1, len(w)+1)
    #first construct the DAG corresponding to the two sequences
    for i in range(1, len(v)+1):
        for j in range(1, len(w)+1):
            if v[i-1] == w[j-1]:
                s[i][j] = max([s[i-1][j] - indel_penalty, s[i][j-1] - indel_penalty, s[i-1][j-1] + match_score])
            else:
                s[i][j] = max([s[i-1][j] - indel_penalty, s[i][j-1] - indel_penalty, s[i-1][j-1] - mismatch_penalty])

    return -1 * s[-1][-1]

##v = "HVLQMDRRRDGWDIYTKMKKCSNHKLFTTRGNSGCLDKAHVCNVILVGAWETVHMAWMNQHFWQAPRHLNYTGHFHVQRAHDREAMFHGLMMTTFNPTEIHAVDANTDDVLDCMAVNVCESWPECISGDCHDNTIDHPTYQNSGSRMQMDEYWWKPALHQHGVNPAHSGMMGLNWCWQTSGHYKANSQDDNQVYQKAVEWRKKKRKIPECAWEFHLRCAPHCDCWQTKVKFEEVSYWDVGGCKKYWITIYKFMTWTELQTPHICCMEIHGLIYQRNQLPNVAEKFSVCMHSIVVSEACLQHEYFDVNIFIWQASEPIFGFSQCSENHIFWLQFVWDHWYQWPAWFNKGEAPIWCMVDGFCHCTYHHPCCQNLAPRTYCHNDVNFWQYHCATKRIGYIKPQQCGIDAMDIQNTGINGNFSIKWKVTSGEVIKTRQKQCIGHQYWDRNQAGIDNIFYINWPRALKSHYKDGINWRDAMDGSIHQCVYWCEMCKERELFHWSTDRATVCQSTSHYDDTDRRWCNNLQLHRFEQQYQLRPQYWAWCVQECIRCYARSARRFHRPNPTNHGCTPTQHQSKIVACNPCILDMTVDHNECITWLTCRKWLCIEPRGHWMPRLISCNPEEEKFIPISYWDRGTFQTDWQCMHWYCNMYPYYPIEDFIFHSDYGEFAIQVEIWFRSADPIAQGLQLGPQLLMAYAMQFRCHYCA"
##w = "HVLQSDRRRDHTKYGMCKFFTTRGNSDCLDKAHVWSAVWCHSVGAWETVHMAWMNQECHLNYTGHGHVKAHGWFCHHWFMFATTFELKFNPTEIRAVDANTDDVLQPSWPECISGDCHGGVADDMNINAYQNSKWCGSRHRNHCCVGMWMDEYKWKYKVYYSHHQPAANPNELLQHGVNPAHTVMTGLNWALIRANEQKAVEWRRPPEFHHCWQTKVLDVWKYWKTIYKFMTWTELQTPHRHGLIYQRNQLPWMHMIVVSEACLQHEYYVFFDVESNNLIFIWQTSERDYMYTYDMPIFGFSQCSESHIFWLQFVWDHWYQWPVWFNKGEAPIWCMVDGVCHCTVHHPCTDPQQLFFLCQYTCHNDVNSYHKATKRWRGEILIKEQQCGICTGINGNFDGGICIKFKVTSGEVIKTRQPHCMRRYQKSNDKSCIGHRYWDRNQAGYLQIKYSKSAYKDGINWRDAMNRQFPRMTTWCMYTPWVYWCEMCKEMWRELFHNSTDRATVNTDRRWCNELQLHRFEQQYQLRPQYWAPCVQECIRCYARSVTNHICTPTQHQSKIVAGMYATIDYGSRMIACNPCILDMTVDHNLCYRKWLCIELRGHWMPRWISCNEEEEKFIPISYWDRGTFQTDWQCMCIDDMMRNHWYPNKPYYQYVITRYEIRNDDFIFHSDYGEFARYVEIPFRSADSRQNPGFANDPPQLLIAFRRHLYHFRCHDCA"
##print edit_distance(v,w)

def simplescore_lcs_fitting(v, w, match_score = 1, indel_penalty = 1, mismatch_penalty = 1):
    s = zero_matrix(len(v)+1, len(w)+1)
    #initialize first row/ column to 0, -5, -10, etc. instead of 0,0,0...
    for idx, item in enumerate(s[0]):
        s[0][idx] = idx * -1 * indel_penalty
    for idx, row in enumerate(s):
        s[idx][0] = idx * -1 * indel_penalty
    backtrack = zero_matrix(len(v)+1, len(w)+1)

    for i in range(1, len(v)+1):
        for j in range(1, len(w)+1):
            #free taxi ride to beginning of shorter string
            if j == 1:
                if v[i-1] == w[j-1]: #match
                    s[i][j] = max([s[i-1][j] - indel_penalty, s[i][j-1] - indel_penalty, s[i-1][j-1] + match_score, 0])
                    #now keep track of which edge was traversed
                    if s[i][j] == s[i-1][j-1]+ match_score:
                        backtrack[i][j] = "diag"
                    elif s[i][j] == 0:
                        backtrack[i][j] = "taxi"
                    elif s[i][j] == s[i-1][j] - indel_penalty:
                        backtrack[i][j] = "down"
                    elif s[i][j] == s[i][j-1] - indel_penalty:
                        backtrack[i][j] = "right"
                else: #mismatch
                    if s[i][j] == s[i-1][j-1] - mismatch_penalty:
                        backtrack[i][j] = "diag"
                    elif s[i][j] == 0:
                        backtrack[i][j] = "taxi"
                    elif s[i][j] == s[i-1][j] - indel_penalty:
                        backtrack[i][j] = "down"
                    elif s[i][j] == s[i][j-1] - indel_penalty:
                        backtrack[i][j] = "right"
            else:
                s[i][j] = max([s[i-1][j] - indel_penalty, s[i][j-1] - indel_penalty, s[i-1][j-1] + penalty_matrix[v[i-1]][w[j-1]]])
                #now keep track of which edge was traversed
                if s[i][j] == s[i-1][j-1]+penalty_matrix[v[i-1]][w[j-1]]:
                    backtrack[i][j] = "diag"
                elif s[i][j] == 0:
                    backtrack[i][j] = "taxi"
                elif s[i][j] == s[i-1][j] - indel_penalty:
                    backtrack[i][j] = "down"
                elif s[i][j] == s[i][j-1] - indel_penalty:
                    backtrack[i][j] = "right"

            #free taxi ride from end of shorter string
                
    max_score = float("-inf")
    best_indices = (None, None)
    for idx1 in range(len(s)):
        for idx2 in range(len(s[0])):
            if s[idx1][idx2] > max_score:
                max_score = s[idx1][idx2]
                best_indices = (idx1, idx2)
    print "Alignment score", max_score
    return backtrack, best_indices
    
def lcs_affine(v, w, penalty_matrix = BLOSUM, gap_open = -11, gap_extension = -1):
    """Tri-level DAG alignment algorithm"""
    s_upper = zero_matrix(len(v)+1, len(w)+1)
    s_middle = zero_matrix(len(v)+1, len(w)+1)
    s_lower = zero_matrix(len(v)+1, len(w)+1)
    backtrack_middle = zero_matrix(len(v)+1, len(w)+1)
    backtrack_upper = zero_matrix(len(v)+1, len(w)+1)
    backtrack_lower = zero_matrix(len(v)+1, len(w)+1)

    for idx in range(len(s_upper[0])):
        s_upper[0][idx] = idx * gap_extension

    for idx in range(len(s_lower)):
        s_lower[idx][0] = idx * gap_extension

##    print s_upper
##    print s_middle
##    print s_lower

    current_location = "middle"
    
    for i in range(1, len(v)+1):
        for j in range(1, len(w)+1):
            s_lower[i][j] = max([s_lower[i-1][j] + gap_extension, s_middle[i-1][j] + gap_open])
            s_upper[i][j] = max([s_upper[i][j-1] + gap_extension, s_middle[i][j-1] + gap_open])
            s_middle[i][j] = max([s_lower[i][j], s_middle[i-1][j-1] + penalty_matrix[v[i-1]][w[j-1]], s_upper[i][j]])

            
            if s_middle[i][j] == s_lower[i][j]:
                backtrack_middle[i][j] = "lower_to_middle"
                current_location = "lower"
            elif s_middle[i][j] == s_middle[i-1][j-1] + penalty_matrix[v[i-1]][w[j-1]]:
                backtrack_middle[i][j] = "diag"
            elif s_middle[i][j] == s_upper[i][j]:
                backtrack_middle[i][j] = "upper_to_middle"
                current_location = "upper"
            else:
                raise ValueError #not recognized
                

            
            if s_upper[i][j] == s_upper[i][j-1] + gap_extension:
                backtrack_upper[i][j] = "right"
            elif s_upper[i][j] == s_middle[i][j-1] + gap_open:
                backtrack_upper[i][j] = "middle_to_upper"
                current_location = "middle"
            else:
                raise ValueError #not recognized

            
            if s_lower[i][j] == s_lower[i-1][j] + gap_extension:
                backtrack_lower[i][j] = "up"
            elif s_lower[i][j] == s_middle[i-1][j] + gap_open:
                backtrack_lower[i][j] = "middle_to_lower"
                current_location = "middle"
    
##    print s_upper
##    print s_middle
##    print s_lower
    print s_middle[-1][-1]
    return backtrack_upper, backtrack_middle, backtrack_lower



def output_lcs_affine_backtrack(v, w, backtrack_upper, backtrack_middle, backtrack_lower):
    current_location = "middle"
    i = len(v)
    j = len(w)
    string = ""
    while not i == 0 and not j == 0:
        if current_location == "middle":
            if backtrack_middle[i][j] == "diag":
                string += v[i-1]
                i -= 1
                j -= 1
            elif backtrack_middle[i][j] == "lower_to_middle":
                current_location = "lower"
            elif backtrack_middle[i][j] == "upper_to_middle":
                current_location = "upper"
            else:
                raise ValueError

        elif current_location == "lower":
            if backtrack_lower[i][j] == "up":
                string += v[i-1]
                i -= 1
            elif backtrack_lower[i][j] == "middle_to_lower":
                string += v[i-1]
                i -= 1
                current_location = "middle"
            else:
                raise ValueError

        elif current_location == "upper":
            if backtrack_upper[i][j] == "right":
                string += "-"
                j -= 1
            elif backtrack_upper[i][j] == "middle_to_upper":
                string += "-"
                j -= 1
                current_location = "middle"
            else:
                raise ValueError

        else:
            raise ValueError

    return string[::-1]

##v = "YVNAQNRVWQGKKFRTQTHYDWQCIQGLYVDSPPVLQETMFRKIDAEPTHRSCMRQCISQDCFHDRYNMVHNIIVFII"
##w = "YVSYQNRVWSGKKVRTMDWQCIWGLYPVQDNDCPPVLQYAKQNGGDWMMPMVRKISAEPTHRSWQKCFHDRYNCVHNIIVFIA"
##output = lcs_affine(v,w)          
##print output_lcs_affine_backtrack(v, w, output[0], output[1], output[2])
##output = lcs_affine(w,v)          
##print output_lcs_affine_backtrack(w, v, output[0], output[1], output[2])



def find_middle_edge(v, w, penalty_matrix = BLOSUM, indel_penalty = -5):
    score_matrix = zero_matrix(len(v)+1, len(w)+1)
    for idx in range(len(score_matrix[0])):
        score_matrix[0][idx] = idx * indel_penalty
    for idx in range(len(score_matrix)):
        score_matrix[idx][0] = idx * indel_penalty

    for i in range(1,len(v)+1):
        for j in range(1, len(w)+1):

            score_matrix[i][j] = max([score_matrix[i-1][j] + indel_penalty, score_matrix[i][j-1] + indel_penalty, score_matrix[i-1][j-1] + penalty_matrix[v[i-1]][w[j-1]]])

    
    middle_col = len(w)/2

    middle_node = (None, None)

    max_score = float("-inf")
    index = None
    for i in range(len(v)+1):
        if score_matrix[i][middle_col] >= max_score:
            max_score = score_matrix[i][middle_col]
            index = i
    
    middle_node = (index, middle_col)
    #print middle_node

    candidate_edges = [(middle_node[0]+1, middle_node[1]+1), (middle_node[0], middle_node[1]+1), (middle_node[0]+1, middle_node[1])]

    best_edge = (None, None)
    max_score = float("-inf")
    for r,c in candidate_edges:
        if score_matrix[r][c] > max_score:
            max_score = score_matrix[r][c]
            best_edge = (r,c)
    #print best_edge
    return middle_node, best_edge

    if middle_node[0] == best_edge[0] -1 and middle_node[1] == best_edge[1] - 1:
        return middle_node, "diag"
    elif middle_node[0] == best_edge[0] and middle_node[1] == best_edge[1] - 1:
        return middle_node, "right"
    elif middle_node[1] == best_edge[1] and middle_node[0] == best_edge[0] - 1:
        return middle_node, "down"
    else:
        raise ValueError

##w = "TSQWRGGMTVPTFYDQIKMAPNNSVASVLDKNFRMEDCLWVFNQMHQGVLRAGKLYAFTPGEPHKFYSTELSQACVWSMAKVLPMCTNNLQEIWTEVHGTRCAMFYYANYHPLGYPGDDARHERSEAASNRLTHTYYRQNSLKYNKAIEVPKKPFNHGDMSFNHERPEDIGIFQTKQTDWCILVQLQHMPRGCKSYAVVVMTDPFCSCPAVMQHDILFTVIQMHPQAMPLGYWLPLRLDYCCTAFAYWASPTANLFWFMTLTMCRRCMSWACQHLVREPFYTSIAHTQIKFQNEQCGDYCICLEWMRWKGDEELHERVGTKFFSCNNMRQRCCAMELQEYEFQVECPELWWIDFASGELIPHDNWRRIYREIYSAMGCVRMRLMIVNIYVTCQCNNYKACIRLPLQAWHCFCHKQNDQIHYEANHIAKQCAYKDDENLSEPVKDVVHFQFNFRKYWRYGVAPFTCHIRKCSLMPARKDIWWFACTHYTDNPCWYMPDQVSHKDCWYAQKNELPFYYMAPTMPERYNGWDYDKRNKWCAPSPIMTLAPYWWVCETGRTRESYQFQRRYICSKAVHCARAVIKTDPGCQCLKWVVCCRARLATMAQGDWYTAIWHQPWELRIITEVEGRDSYGRTDPAILIDNKWLYEGKFSEHLLLQYIKVLWPQNWIDKYEDVFLGYLSRFIPMKVDCSKRGLQWEQSQSFPPQGTFHGGLEHDGHACQRAAHCTNNWNVKTVCSFECMDVHMPAQNERAITDALKRPNTNIQQTAYVKTHYAYYNHWIVISEFHVNIVEIWRCMWNKCFPGMRAADTTPHEKVDQWWRFNDMENVNFTSGQKEQGCRLMDGTAAIRLRDKMYDDTFMMNDHQFAATWDSICRDECDDGEFRITNCTWCACQRFHCRPENMKVVVGIERRHKDQQLCKMLSECMKFKRHRLHCASPNNNPNQSDRTRVEPSPENTETGGRIMFCFDQYRCETHSLLMANAWPLFGAGGVDPVYVAGHWIWQRYPYRIEHCLAGIMCRDDPKDYWKNNTWAEYNEHWIKQDN"
##v = "ECQWCCIHKCEYKEFFNAWFALMRQWINVISMDTTKKQRWNRSMNTNPRVQQKKFHWPRDNFYQHPSNMTTWCGPITDHTINGQRMDFNRTMVCLKVIQPIFFLNDAKLHKYFVCYYRMVSLEWCLWDADSPQPHTLQHPDYLSHHMLDCYVENLVSTSSDAGHGEYSSACAGGLWKSRVNSLPDWIGQEAYRETKANAIIVKNIQIWRKHRWMGCHEIGPGLAPVCAILGYISEMDCCNRMMAETAMGNTVAYERHFQRIGNPSEWFHYELPEREHTWFILKEKLKFKAPVCCYVKMSCFPCTYNMKKLDQWQFNLNYFGNTNVWKCIQSRGMEICDWIRLSIYCEPAQGPCLNVGYQKQGLVNSCSHFGAQYYYWHWMEAKAFLRRRMLNQRGKCVFFWIRCCFDIWNRMITCPLWMREPWDQFIIGCQSMNAKFETQRLSACPAICLNFRMYGVAPFTCRARVDIWWFACTHYQPDQVSHKDCWYACHPARAPKFANELPFYYMAMTMPERYNGWDQDKRNKWCAPSPIMTLAPYWWVCETGRTHESVQFQRHSRYICSKAKSWASETLDHCAIPGCQRLNWCHRDWSIDCWFWCLLDMVIEKFSDNRPRSAAYMLDDAFTCYVERCFYYSIDPLSKMTLFNFQIIGYEWNYRQRERQQHYPAVARENWTCWHRRREMSMSIPWNNSFYMQHTKGICVDEAEFCMWRANWGIGVPKAGSHKTIPGIWAVKARCNVHSIDCLMDYSWYGIKMKQEKFWLWANKGLTRKDRGLYSNMEVNRCLIGKALNCLGRGHFQDVCQAFGPVELTRSYDLHYCFKKSNGRKLHYCHRVHLEKTDLKIQWQERYHFGEFLFQHYLSSKMYDQGSMGGPGEMMPGMKCCGHLDTPIPTKTRLSWNLTYLVWRHEWKFMFLENTIIPVRRMKEIHDWKRQQFQSGHRVVEYVDCSDFRGMTDSEIIERWMNVWCRITLIACSFTDKYWDEKWWMHLFMPPANAMQWKHEWIVCYDQEQTEKCMVQVYTIQHLCRAQRPNVNMV"    
##x = middle_edge(v,w)

mid_edge_list = []

w = "PLEASANTLY"
v = "MEANLY"

def linear_space_alignment_2(v, w, top, bottom, left, right, penalty_matrix = BLOSUM, indel_penalty = -5):
    print v, w, top, bottom, left, right
    if left == right and bottom == top:
        print "null"
        return []
    elif left == right:
        return linear_space_alignment_2(v,w,top,bottom-1,left,right) + [[(bottom -1, right),(bottom, right)]]
    elif bottom == top:
        return linear_space_alignment_2(v,w,top,bottom,left,right-1) + [[(bottom, right - 1),(bottom, right)]]
    else:
        #need to find the middle node
        mid_node, mid_edge = find_middle_edge(v[top:bottom],w[left:right])
        print mid_node, mid_edge
        #return
        return linear_space_alignment_2(v[top:mid_node[1]],w[left:mid_node[0]],top, mid_node[1], left, mid_node[0]) + linear_space_alignment_2(v[mid_edge[1]:bottom],w[mid_edge[0]:right], mid_edge[1], bottom, mid_edge[0], right) + [[mid_node, mid_edge]]



#try generating entire score matrix, then divide and conquer only on that
def build_score_matrix(v, w, penalty_matrix = BLOSUM, indel_penalty = -5):
    score_matrix = zero_matrix(len(v)+1, len(w)+1)
    for idx in range(len(score_matrix[0])):
        score_matrix[0][idx] = idx * indel_penalty
    for idx in range(len(score_matrix)):
        score_matrix[idx][0] = idx * indel_penalty

    for i in range(1,len(v)+1):
        for j in range(1, len(w)+1):

            score_matrix[i][j] = max([score_matrix[i-1][j] + indel_penalty, score_matrix[i][j-1] + indel_penalty, score_matrix[i-1][j-1] + penalty_matrix[v[i-1]][w[j-1]]])

    return score_matrix

#w = "PTGQSYVTTARTTAECRVLHVMPFNYHMASIMDSYVFLNFGPALCMHEWYLCTMRCGWSKVGLGYMTCFCKNYHMSVKDAAYDGDKEMDGMTKWCVMPNCMWENEAQDQMQAWDSKGWQDFCDDIKAGMQFIWDSEPHGNFSEIMSMPFDIDVTIFHMQEPEIVQWTMNPQHSPHRPKSCTMASWRTQHHTAWNHCPVSASAFQPQVDVCDNVRFYGETAMNIVGGQAEAEKMKIHPSYQGHIHLCIGNEDTDGQQLWCQNHMQHEPFRYNDSDGDVTYQKHPACAAIPNIHSWFQPWGIDYQSNRQFGNQMDECYDLWALRVWDEPSVTWYYRHDLHDHSESWQRCETNVMWYKGAKDMRGDLWSPRVMIMVPFLTVWRCGVTCGWLWPKSFSKAMMRAQKIHEFPQQRIKTNGAKPDNEREWQAHHAFNTECKFVGPKPILLSKPWRQVDYDYCSFSDDMHFRKCVLTDEFFNVVSTKMVSQCWFWADTLNPEVSNQFMTQEYIVKMTSVCEVLNGVGGLPFVTADSCSSPVIEWGLWTNDQWEGFFKLYWVMLDNDKNPVKWPHNRGIVHGMWPIWWIEQNPIKVGQACMWYPLIDNYWEDNRDVLKPKEDMMAIDISGQVKGWATDIRPSSWSLYIIPDMVWRGSLCDLARVEYEHKPWHNCTTYHMRCVIFYYFAPIGNHNDATIPGWAEWCYWPKMWEGYVMVNCFTEQQHQAEAAVAWGWYGCTPNVPPVSPIMQSFKMFICPNQFQDLKLMQDPCWVLNKFSVNERQLDHCPMDASDHWSPSHNRWNLTFQAWPGRQEFAWPVLFFFSDVWWDAHDYIYVNVMGYTVYHAWSASWVVTQLGNIHGECWNCMVPPEIVMSNTNQKYEHYMIASREMVTPHRRRYAVCTFRNLAWKSFDQQFFCRENFIGIFPADCGIIKCEVFRDLQEFFDRENSKCDQNSQKNMHKFKYCFQFQPQDPVKQRLNPVHPWCRSEEDGLRTQEDIVRPAQYNEWPMHQNDAKLVQGCCIYKYKRKWIPRKYLKTYGTNMPEHFYYQRQVLSRYGSMRRMWIKNEQYVDHRDRYVMLEPGCETFFYSFVMEWDEINDNNSRSKEVAPPKEFDYMYNNTCHDTWRFSEQVKNDNQTQFFVKQTFVRLHLQLDQILPEAIFMSFTLDWPQYGYQIAKGNTFKCMQFTNYKGSTFGWLDVGPGNRPRHWWKTVFWQKWWISMWLDVQDLSKDAFDNMWEKQAMQKPKFHDTRFLQAESKDTRSKEADSKVDPWWRQHSQERFYPGGSECCWMDALHPLKLRNFVEFVVVTKLPNCLWHAFFQYFPEMWLCFMDHASPKQKVWRMNCYRADFCYFMCELGYETDDRSAETAIVMYEPMQMGWNHWWWLTWLHMACTLIIDHIMMNLQVALYGCIQPLNFWMATFHLVWQAKVFFFFAFERFHTHVIMCQKAKENESHRLQPEERMSKWHYTCCGTMFHVNWHAEQGKSGMYTQALRLTHFTVWDQGSHLMCTGIYMDMPQNHCSWARHRTDPCALVVHWGPKVPKPNDTFGCHPNNSEIEPFPPRDDAQANHIEDCHEYRFCGMTHNAYTDHPGFLRNCTENVTEKIMEGPLYPWDNDRGSHAQLVMWCRVASEAVQWVSSGYKGINSAYRYVNLWGKHICRAWQDWDWVGVHIQCNHIWGQETDPDEQWLCIHENGINFFDSNLADYTAEQEDFGDWYCQKSHLHSKVDVKQYSQIATIIWTWQHTNCGCSTCWVPLHRIFSLDNDVPPCIQVYMGDKRQMWRNKDNHNKSQMTYMKLECMFPDKDFRQQSTGERPVTELMCKNIWTVHYCYIAMFYDVEPKCDIEDCYMGVAYMMSFAEGFMHMYKALVCPKSGSMYDWTVVQIIYTWQYFWHRPETTESTWTNQRHPLQLGWNTSLMENIFAIESMKKMTCYAKEPTMRRAAIWLVQMSSYMVHHKCPRHYNEHLRLLVPCSWCQQDKWNESCQWHHPDPYIMKPSYAWWDLLNTCDPVWRRNTYCCKMANRAAHQDWSSNGDRHNYPVIRMENTSDTHNMNMYESVPERPDTFCGLNSSLQGHEWQMYSQAHHPDMFTENMQDYYYGTIVFCHAGICWCWLMHIQYSCCHYACCIPLKPLCAFIESQCQIVNQSFASRTTCQDQSFPHYLIYEDFVIAYEIWDKTAPQMFPFYYYWRWVDRTDCHVQDETDGSWTKEDCAGCSCSRELSYMGFNWVFPYSRTVQLMMEHVPGWCYMSGVFLKLHPFVGMIQKGKTHHIWHGDRWHGKGYNVSTDYYDCVYYEPCLRNKYMSDVIGYTGWLGWVQTLTDHVKSSPSKGRIPVWNQFTQVKKYQVMEHLFYKGAHQDHICVTCEGWVMPPNQCFWFQDQDSQCSLQSDQMERLEAVCYPTMWYRGAWKRHNHTRLWLTTYDPGYCRNRDWAWVTCCNCIAALMQQESNRKYQWCWCYWSTNHPMHNSDIYVVWDDDGERPDGCSNEIRQAKRPCTCDISDARPLKIYMIYCFPCEGKYIDIWMGKMRAFDFLNFMDGKFTIRDGAIFPPQMVPCNVLVFELVYKSVWAETPTIRGWYQCWPAQKVYANGWISMLVIMDFAQKKFVGHDLSTATCMNHRVDCFKNNVRRHVEPPLMLIMNKIWCEHDFMTAMDVIIYASPDMYMPGKPYLGTFQYPYLYKHGSSDYVELEASKINGYMPYWCHESEDSTCHALHDPAHCDLRWMFMCCPRTTKPYVWMCNTWIRYDKQDLAPVNSFIPAHQDVHPYCTCGRAVWTQKRFWKAWWFLITCPDPHDSYRSFDEVGEPIETACRDDCVINIYHSQYNMSSWAKAVAFIKWMTPLQPYEPCFCQKMEFKQWWEKLCVAWSQPVFNFSIPKHVFIVERYIEDEHWEVIYWMKKFVIPKLHMGPWQSCTIGYREYACIGIDAHDPYRCGDKNMANMRFPWWDIISFLLFQPLPMECSYHGQGTFCLKWIAARNGTYQFRIVEVYKFSSAEVNRNTQYFSHHHMMLMPHNFYHMGTFDYCWLKYPFPTMDWNVSTTSPNILGLENHKDLCIMVMNCEREMTPERIMQYKVLLSLWRENVVMPCCLIALVNLLGQNKENTPLDCPKMPMVMDYHPRKFWLSPGFIGKYHIAQRTRQWRLIFCPAQTKMDVCASYPFPGPRTDHTRSMWLMGHSTAPEFMFMTNKNMQIGCPPVGAQGHVEPPTRQRKGKHQYVCEPWKMWKHKPQWRAWAINWKKVITCWSVSFDFPWDSIFTVKDCELRGGSFAMMRKAYQPPRMSQLPWVVKCNFSPKQGYEQYITVDGKTQKTRVIDPMPDPHHATYGIMFSHQYTVNWIHNCERLTMAKINRVYFTIIADRWGHYCVNINHQTLQMDDMMCYDDSVSGQGYLCMCCTIIPWGQCVNAYIHRCWHCTDVYIHRLLPEQETVFQFCDNHMMAQMHLMPTLNEKGSFSWQRVMSGGVFWIVNGCNMYAFSHHWLAPHHDRTNQGVYMLSQPQMCWALNDDHTYHKNNINAWEPPIGTHTGWLRAEEMTGSPDRLLLIWGFMCRAMYSCHLDACARNLQFNFLMKVGHHNQHQYWAWCEQCLDCKSWDTNASSKLEFNYETLTDLTGHPPQRPDVFFCDDCVAYCEFLKHTSPLDRWYEPRPRRLGQWVKSLGSGNPPACFEWCYIRYDCWYCNVVPIEHTEDPMHWHENWDNNCIGQQHWINVMCQMMTPNNAGIHPVRPCIHPDDNVRMPYECHNMEPERVQFVDQVTGAPYRANATLPCDHDGFEAFMAPDLTETYVQDQKYCKGVPFQMSKPNQASIPLWSYILYSCEMACIEIYIMKGWMLKQSFHGSPHKTVTCIGTHCMIRHQACCNNDKFAVANRAHEFRWYWARLNGQKMIEFFESFRDMIKISPCMRWRDDAPGSGLHIWAAHIFMEVEKLVWTLAIMNCAYAAYPVMEPHPLGWVDTGYVKSHFQLAYSICFCGQIINRIMILQARYQYVAPATCRLHSCGDDAALTPVNWSFNMGHGMPNINYILNWNRKRWGNFRHQMHIPPGQQCRCWRALKDDNVMHEDTT"
#v = "QVPFPTVDVIVCCTGIKCEPMNVGYDQQMKDCFICTREYDIRRLHTIVCGSEWACRLWIEADWEDCEKSFRDFDAPINIVQYAVWRANVETQCPGYLNRTQWIMIGYWFIGTWNAVLIVPKSPAQIETDGIVYKIPCNRYFEHGPYFWRSPWAGPYPTVDRHDSVCHGHLKYGSLPSCQNWEFARPHDLGDACMWEKPQLQLNWNPRPRAIISTGTFSPEQTFWDGMPWKYFWKCPSSVQANKRLYKVLTVVCRQENHGYKETHRKFHIKCLVGQLNQPKPWCVYCVVYRSDYPPPQRWTFWGTPQYIMCFVKPHKLSDESAIGNWWNIGPCDRLVASAWEHCKRLGWYPHGWAKSMFPHMNIMGCSRKFRKASIEWPIMSHVGYCAHWHPFSRRVQFESNINQSLRWVVMSSFKDTDDHVALVCLTPAGEIPVTNVGQALAEQSYRIWSAQEHRAPFTGWMNLFCSIGMTMYIEKCSREPIIKDHDCFNDTADPSDTKVTSWMRKYWIEEDPTWRSNMIHMMGSIFSCNRMSNFMCYPESVRADWPIELWPGRLAIGFMNMGVASLEHYFPFIGFWVDYAPSPSEEHQWRHDAYAYDEVYAMVPMDCKLEGQTYTQCMMWKIDLVLLWSGNSEICIEQHESFSRSIYGHVSKAQAVMKYARRGPAHEQFVTGKSQHSQDCTHISPKIMLHSSIRIVAKHDMLRKEPHSDYHMLKTEFQDKYERMTTMMWGFPDWELPHTEQRHKLAGEVRQATASHYQQYYKPDHGTHEYVCPQPCLIAPWASGTPEFEMAYQLTCNGMFAKCYNRRTGQQVLQISVSHSCMRTKMANWYPSMDMFLEMSNGNADLASNRIGHFSYGHEFVEHPNVMWRPDGGRCHGHEAICNGLAYQYMWPVYHNRCNAKWVEVVHHQDSNFLPMIHGAGSHLHHQLAICYLLVCPVTGARCVGENLINFLVIICNWELIVFLIIEMVAEGLRRPMRNKCQATSFNLETYFRKKRMQCTLNRPYMTRTRRPHLWGPELRATNKQRDLPVTAVPCNQAQCKKFWGGVQDQSNDDVNWRDTKWDFSWGFSPAKVHWHQCVYDQGFHNLEYNPCLHWIWYMYTWMIAFERTVGKACHNWEQIPIDSLNNFQVHTDIWIELHCMNMSPYAFVNYSTCNAVAAKWYLELAIAHQSEPQKWFYFVSFILDSRFSPHNMVFYATSDGYRDKLKPLEFDIMMKRGTWTPEHWQSFTPHRKISPVHSTGIHEAVDIYQYFHEPFAMEPACKCMVMIYTVAIVHFKCIANHEVSGGTEINLVRCFHIWHCEEWKYMCHSWFEYNAIFRCEAMLCWKLFCGQSPIDMLTVEVKILWAVTPQMIACADAYLRPFMDWIGAFSLCQQTFCDLFAWPPQVQRFYWTVKEVEEQWYSHWVGKSVNINSSSDHNNRWVLWPYFKLLFNVANHQPDHCREAVWYNVASDRPHVFCMMAGGVPQKTMINQFRHSIIFSVQNPHFYGMQPTWCSERVALVCPKWHAPNAIPPPKFMHARAFWAVPTKCVYQEHDHYWHNHKTSHFPGTSPDIYEVRAQFRSAETHNHPYNDYKPLMFVKTHITIAKFIGGKMHMMGTQGYAMRPCDWESKMMVTFVKVVPPALTCIFFIPAQPHTMTGWALYDRYMVCRMCHEVEPCKWFVIDVDHNQNDSIMRSHPSERGTTGICDQKHHNLQHCNWELDGPPEISMTYPILNSELDLGWYHLWCGDGPMHPKFGRDRGVTEWKVTIKTPFNLAPTIENIDAQSITRWSQYMINKADMWQLQRVPHKCTPKDCYFGQQSFNERELCIWLADPLMAIAMFYKPLVDPPIEMEPKIESFAMYKAVPKSGSWIVVQIIYTPETTGWIEHYDTSTWTNQRHPLLLGWFSMWSCFENIFAWESMKKMTDYAKEPTMRRAAIWLGEDSQQMSSYFVHHKCCRHYNEHLRLLVPCSVIQRCQQDKWNESCQWHHPDPREPWQFGIKKPSYAWWDLLNTCAPFYPDHKNTYCCKMANRAASQDWKSNGDRHNAPVIRMENMYKSVPERPDTSKNDQHPDMFTENTQTIVFCHHDIGWCWLGHIQYSCCHYACVIICIEMLKPLCNWMHRIESQCTIVNQSFASRTTCQDQSFYLIYEMFVIAYEIWDKNAPQMFPYYYYWRWVDRTDCHVQDETDGGCWTKEDCAGCSCSRELSYIEERGYYWVFPYSRTVQAVMMEHVPGWCYMSGVFLKLHPLFHYDIHQTYIMRAVPTEWTQDMPKDHDWKLYQWDLQRKWSYQVGDELDVGPGCLRPAVAAAYFQTTCILCATAYEDYSEKNKEYRHYTACMSGGLFNHGQMESYKFDWMDWHRQGGDEKPDGGDIEHCYYCSNEASYTPATYGYMCNENGSALGRFMVMFVRMFVRASCSNRDLGDRWQWIFTDYWHCDNERAGCEKDMNQNFGGHWPLDYCFEFGWPCCEQRDCMHLCMCSYMVRVSQDFKSIWDERLGMIRDWRFFVSRNLQCMAWTTYKMEFCLQTYSQFILPARLQEVCDGLWLSDCHNYNWGRIMKWGQLKKVMVPRWEMMIAMRWDTRERWMYYVSHSDAEVAEPSVELNLGGMHAIKSTTWMWVKSTKTCRECMNNIYSVFTTCKKKIAMTFTHKPIKHDKPHTFRCMSNQTEPVCHCHDFHCIWKGFGLMHSGLESQFVDIHCKRPWIIHDKRQHSLGIAALKTCYCGVRKNGRGAQTNGRETGDGAEGIQLQIHLHAVRLKVVAHFSNAVLYDGSKRYMENQKHHMTLKSPSNMPYTNGCENGWYRPCHVQAYVANADFASPLEPMVYTKWWDEGSSWLKNRRGCQATQKSQKPKSMRELWLVTHLVGAHEGNCDHRLLFQYPRWIFHSNKYPDGWKHAHRAWDPDSYGDFWVKHGHHDLLLACKEEVLCTLYNFCKQELENLGWVCCVLMNVCWISHFGNGNYPYWHHRHWLHMENDCDIAEELKRVQGYLYRHKWWVGWELCDFFQANQDNHESRLQRLHQHRLTHNHCRFPKVRQQDIAVFWEVVSICGANRLVHIFACMIIKDAHMVERVHNLCDPTWWPQHLAMNSMGWYMQKLVEFMTPCGNLWSRKFCQIQMHGWVYFPRHWWYSIPDEAMVGVRNNESTASVIRVYFDEDINPTNSNPNRKPENHCKELLLNMMGCVRCAFNRKLTPHKEQSVSYMFIHQCYPLCAYNMRCMTTRCESHMTHEFQPGWRRQMETLVICRDAIVQFVMTVMIKRRMTDYSMSITYQEWTFKCLRHNFALRCKSGCAFVLEDQDVQLHGLPMKWYAMFNDMYMFKCIRTYIDEYASPDYNWNQPRWLITYATNTGSHAKTRQSNENCRRRIFYDYNRGMWLVLCTRERIHWWSLPYRKVHVLIPGHISASEHYQNLNNPPMYKAGMAEKSPGWQVTICRIEDVRPFDDDHLYGDEQEVHNSGCAQDSVHVKKMTPVLIDCGDRPIEWTCFQADYYNKPTHRFWRPDVKHPLNKYCHGGCDPDSNRSYCKWEDTCEDTTIKYSRTHSDFNVGSMATKYIDREHNKGSEKWFEGLGQRCNQPGEMKVNFTLEIMTFKPRMRSFDHEPESAMHNQYEFLNDGTTCMGFEKKGIHFFYKNICRNLQQYQCHCPLCYRMLPGQCECQNIIVSPRSVLQHLNCKQNENMKTSSACHRKIMHYKMKIYGVSIERRDQTFAVRMPNFECECWDMWEGSSWLKKWIHRCNDCNLDAPLERPAHFKHDSFWCTFGIWLQYCCCYSGFFCSMAHMMNYCLWCWEPLFPDKWDEYFSLTYDGVEGWCHDLIEQIDGEMLYGLTIPEIMPEGYPRVADDHFPYPEPSDDDSHNDKSEKKRSYLIPSFWQACHCCHFKTQQKCWACNSRIYLEADWLKHAILPIGRRLKRVVTKMHRQVERPVSLMRTFFNPVGCPDTSDNTGLPDLMNWVGQGITVGQCWHETIYGLSAVCWSPMLNTQTAEWTGGKYKTMDGGIARKEGYLGVKKLTQFGDTAWCTWEGHCDTWMRDYMMHWWYATEDMYQKLIGIG"
x = build_score_matrix(v,w)

def linear_alignment(score_matrix, top, bottom, left, right):
    if left == right and bottom == top:
        return []
    elif left == right:
        return linear_alignment(score_matrix,top,bottom-1,left,right) + [[(bottom -1, right),(bottom, right)]]
    elif bottom == top:
        return linear_alignment(score_matrix,top,bottom,left,right-1) + [[(bottom, right - 1),(bottom, right)]]

##w = "NCAMPNGREIACDHSKQLDPTDLCYRSHRFCHFHICNMVDLNFMPFRSHDAKDKYYEMILWMSWSNTMWIRTHFAWEQKCIFQAARFYMAMVHWGLWKNYTWSCRFAVHLMYTCFAWAAGVKYRWAPIHVEINFSYPNRVGHAEANMSYRKHVTEYAMPATYNVWLLPSKAMWWQQWFVPWQPPQIQPYFRIWCVRMMCDKRREYYTISDVNGFWQPSKTSKHAVAFMYSGDYYFMLYNFHQWFYWFSMTHIPGTWYEKKHCMCPHGIRAGHVGFHNIFNVYDPMIRPRGVWFQRSSHMYTNHSGQDSPIVCATNHYDYNVGFKQCLTVHDDITCHVREHWMTPDNMVELVRQVSEGTESCRCKFVQESMKSWYTLYAALNRCHDDCVLHMYHQCFDKSHADKGIKEACFAFLTYVPREYMDATVIWIAGGFNWAMKATIFENRNHHISECFFKEQGSYLYQWPHHQEHKHGRCTFWLCFPRGQKKKEQGQYADETGRVKVASWEESYVIHTWSPKSWRISAVQALTVPSRPGDWCSDVETINKTVKMPNTVWADPHWQRILCGDPMYSNPSVQGHDMKEGMVWEKVQTFYEKMRVGVNQNRDMTFNWSQLMGMAHTQMDRTREWIAVKWNNMPSKNWLGERNECHYYQFFNMHIAQKMAICAPCCPYYMELIEQAKPQPEPQGTITWGTKVMFPNRSEESKLVVVDDVVLETDSYGALSCVKTFLDVVSFKDDAIRQCDTKLSWTGRDDWLEIVQEHPTRKKFDEQYFGYFEVSDKEERMLPRCESDENTNFEFHGICQKCIWPVWWSLHSFVPQKADSYASMNDALYNWTKCNLDYDSDKQYPKWNCWCITYIKIWHPRKGFKLRWGLMSLSVHPLHVRNRDAQQEVFQHGQFRDHQQDYWRHVWNWQQDRLMDPKAAYDPWAYNPKRMIRFHNRHSTSKKKPEHHYYEGYCNMHHQTRTQEFQSRRVQVAPSGIRTTILMHLSWNYTEQCIPYNRKAPCSATHQAYAGRVATKLVHMQYFWWKAIKDKDIFHNNWAVYFHHYGCLGSWQPPEWYLNCWEIAQAAGHFQIFFPAPFGWWPPDGVSGTSVHAHYLHMEYMMQSWKNMAEKMRVSLTKAAKMANKNRLAVSICHPGPIARGQKRVTIVSIEFTWPYKEALEGWTIYVNWEVYCCFWTNYELYMDAMKKKARPCCVQKAMMITWLGDAMQTVRPQIENMMFISEQNILSEELGNSTPSGKQSTGFYNCGDHCCLHRVWTVFTDRMSSHITSFINFWSCGDQQHVLPTCWCGHICHGMCMPWKDPCYLNGWEWKKPFSETQIKENVDWEFTPVGVGDSYPCIWTEQRNSRPNDRCDAATSFPVVYWYRGEWPVIDNMYKYVELLPPQHYEMNCDENNHCWGFDTMNTSCRNFSTFKYMVFFCDHPSEMWGPKQATGMSEFDQFLQCLPAVSPFTWYQRVITYIWHSQMLCAWYQAPRTSFKERHYHYGHTLPDNGIYQIQECWDIVGYWPDKKALVQRCIWGEFQSWGLVFTLFDPVGMYHDYHGWSDWHDASVKNVTSYWDVMSHWAIVKYMTIGMCESAGFCCYDKMNQWATSQVQYDQCNYAYRVILLKGGIIYPDVAGYSCSWYPYPDFFEMCHHMNTRPLWTCQCRCNCVNMWHNIRYCMNECADFYFDMDATQGSETFLHCDRNTMQAWEKSFTAQNDIPHVCCLEYVQRGYTAKMCPKKFNRPIMNSCHEFCFYPGSPPFLNYNPSEPPCAVWAGRNKGGIDNQKVMSLSEYRDRSLTAHQPIWTSGEIVMYCTHNDAQKHAALLCSCGCAIYKGIPLNKDKTQMMQHGDDWVSRVKECNFPPINHFQFHRLYQSGRHQSAQISIPMVSEALDTGNGSIKHLWINWYTTMYDHCFKTNDGPPRDNWCAWRWCMSNNKLAGWETNASGEHKAPRYGVVMWQLFLCPMCHYQHCIWLFFDSKYFPGKHFPQFHKHQCYNNPEPVNQAFDHGGCICAISRACRCLFCFIEWGLIVCDTGQYKQVPAAKWVFCPTCILFQSEKSHHPKKEDFHLGEWTGRSMLLEFKCGKGMFDRMTRFIVREVKNFCSWMAEQVRPGEDYRRMVYLDPTKFNKSGNRYKPQGHYMACVCQRKGNAGQQGNRPTYVRWPNMQTMVQSVIPTKSRSMDCLSHWQMCNQMVMYTHFQHSVQEEFPTVLFGFTPPNNEWDMKHLMDLQTWEHIWLTDDFGMRMIWDRNSPETELFVDNVENLHCVAHTWTNDARYYNCLCCSHHMNIYTFSPWHQNRSHWLYIGMCVNGLEESPALECHKERRQDDVLTTIPFDEMHERGLCFFKRTLQSGRAYFGIHSEGDGNSTIKSRTLTELCCCKNPNMYQTCEQSCWWPIDQRSIEWMLVPSRNMDTVKPHLDTHRQRKVFACVLPHMPSDPFCGVFATYEKLGQAHKCHWWANPAVTAWWETTYNQWHMGHGNRREKQNVPKKRDYEAKMIERWIWECTHKQLSHVFPEAPAFESQPKHAYWQHISNDRWHVFRNQGGFTEKNWPRHIGVRLSFIKRNWQPQRISQAFWRGIFHCHWYAKRFVGLPYLRSINVAGQEFFQEYPLRYIAEMRRITPLDLHQVLTLYLICDKTGFFEFMSMHNCQRCPRFCLTKISACYLELCMSERIAPEHDTSPGGDYRHENTFIMEDKAGQYFGESQMIWWPGMNDISCNVKRINIHTYQRVSPFVFDWGNMGPLCERHGWSMTQTKRLMKQAYRVHNHNRRYDWLFRKFCNWSWVPWGYYLDSCHLKSAEMNFHSQIEFTSENSVNQKDYYSNITNMWVNSVVYAVYKFTHEEYGMLYHVRSIIPADLAWHSTGCKLPPQKDQVWKCQLQKTGTIMAIHQARRLHGVIHKPTNPPDFMMKRYARTPSYAWDNIWMSECSTIAWQVPMCAWCWALWTLFQNRITGCNTPYKVNQMSFAHMREMRTERMCGNKLAPHGYSVPMQHFTHWFFTWHWCAEEPKGGKIFYVWLVFAFTIGFNRWPDSHHDLLQEWIQAWPMQWYIHQPEKWIDRPSRHRTLYHISNTIQFVDSDKTDNVAMWDIEWDWWHLHMFFKNYCKEGESQRYCMEEYMGKLELCMYMCAGYTSQDWHWCKQMIYWRHTPIRAQCMLECIQSRTSSSCTYLDLNGTHMVKEVMKCDWLENTMMVHEIPRNGKTLLYVAEGHDEELAYNAGYYIREYDKNCVLDQEHYYDYSADQPDNFYKDLPHFSYSMTAHEKVSMLRMTQPMAWGMPMYTFEHFSSKSMIIFDTWPAYQAWERAWLMKLKSNHMWPVQLMQMFWPPVFAVAPQIVTPFAVIATYDLMDGQNESMDWRICVYIIGIQRVQACPCQDCDPCIFTALCMWQHYDGYVEGKEFAQCQKPLRPYTVLPMDVMLITNHLDLGSMIKVEHMEASSVMKLSCTCQQFKAKYRDRYHYQTTALEYGYYCVMWISLLWVEILADYAIIWFIRNYCWKWLYVNGPRRGPWQPSQFSQDTEGGHFHHHKHDSHNHYCEIWPTAMCGKDWMLRLPHSVRAQEWQFTRAPNSDLHWNGIMAEIRSCMFFTTRFDMRIPGMETLVSAKQVQSGMNIPCYWNVPNVLPPPCNGYMPLRTVGTCHSNPELGPYDQMSRGGLHYGARIRLTRHSPCIECCYKYCPDDPYRRAHCCGHFHANQCPMQTIIFYMCNRHFGYFHRQREMDITIHMMDQGINSDWDDMCSIINKNIWKWVHNYDNYSEISDKICDGLSVHGMFMISCPFPLNIYWAIWNMCQFVYFYDHIHSPNGVAYMCKGCWQGCHTNWVVSCAMECNLVRRPSHMYMEFKRVLERLKRPGDGSNFMPGHVNFYLHWQILPICNKNCKHIHNKPQSMDLTPPKRFRPPCWQTDRFKDGGHNIWCMGGQSNIQPLCYRYVCRDTLLHTFPIVWRCDSMEFCQIDNNYSIQDPTAKMQRQ"
##v = "HANVHSRTWHWAHYQPANTTRYRDAIYDHSQSRVWLGLNILGKRFRDVLFLRMFDISHCASDIMVDGHHAGMEWGYETLERDHMVCWWFISREVHAECEHIHSDRIPQPPSWHRWDIPIPEAPGFQMEAPMSEIEIVTAEGNDGHRWRSRHTWTHSFTNIVSVNYSEAPNMRIDKELKFTRACIWPANIRDNWFACYRWEMMRWTSTNRWCKKVWNVAGEQYHCDFPPWAHTGEHWPTKIMALMKQMHFHKAWRQSFGNSRHPQFVDFKRIVWSEEEMWPHMGETCYPILMNRDASRWLTFAWGNTWEYEFNVEVAVFPNCDDSAVGQEWHRPSSKWLPFNDIAQSPHNMQVLILFVKMHAQDQGVQKYPLNAWLLVNFVRYSPFLLHHHESMYMAGCPALCINEQAMEMLVLNTVPGVSTGDHSEGRGEHQCADVKIHQAGFSTLQNCPVPHDSMYKRYEGFSYCMMNPEPLGWEYSRKYPKAQSMYYPACCGELREGCDKNRHRHLFKITNFIHFRHTRFPSQFMWEPFLLPMNSQVFYREQKINSNNMRDGLESAPLPDNAICEMYGVCYCFSATAYDCVNPMTEIHDMFRIHWDSHSPYSVVSSNCSVQAPSREYWITWEYHSIVEMNEGGWDFSHPKGPRYDMNGTDPIFNVHCRCVNNRLMVCGARMKNGLWWHRDQLCRNKKHIRYYQSWPPAYFWDWCKNCFEWQYRRFPEQNHMCSSMDNQANLDHKYDAEELNSCPAEGNIGNMWVHWIMTRTIVHAMDQTINTHSDKTEESCMRLPCIFPQARCESIYRRLVSMDFSKPGCLHTDLQGHMQDFYKETYKVHLPYQPWHIYYNYSRNTWRYRHHSQFTEIAVYSTCCNDALCEKLFECDNLKKHIRLCETHINDHTERKWVSSRNQDLMWCWIHRLAHVMSSPQRDTAPCGTQDAKADEYTTYPIRVFMWLWELWYYMCHMRCGWPWADEIEYDDTRSTYGDTNYQQHQPQHPSHWYFPRNRRTREESYRCPVETALPYHCCLTHSFIPDPDGPAHTQMRWMAQVRCELLIRKMPMFLHHCELLLRPYQFIMCWAFGRLVFKEPERICRRHSTSAYNRIRFFEVACCYPFMYRGSQSAFGEVEQALGKTSTDCIRYCDTQMKCHIEHLYGNRCDGSLRFCEKYEQQHFKETTLKHEGYKICRGLHHGTDPEHQLNTVSDLMGEFHRWITFTGHPVGDQSNTICILTQIMTIDVGDSMCPTSILQTAYIPAGHAPGLFPETTFWRMNMTRRPGIFHTCWAKGTSKGTDCDMGRKHPHYSEIDLQTHEYHKKSGIMSWEGDFIAMETIMLYITKGYQLYEAFDDGEEGMRIIPWISIPNLKCFVRHPRWNSHSLCYKFGRFFTRRMIYFHKPYELVQFCMRVQFPPDHKTRQASFKAGTDSEQQCVDHLDMTNQYGPNGDKVDLRRTQFSFCQCYDGKTKHCWMGAGSWFSIIGRWSVFTQHCGLIAAMMRQGTRQAKSRAGELNVKACPHVVWNFVKDMVPRCETMGINMSPRCWMPKFLTGVRCKCIMKDFVWELEQEGPLIMRIKAQYVKDPTQIICISWQMNHIFGQPFGKIYMKGSKWYHCLEYKGMTGDIFAAHTYQLIWYDAKEDCYIVCVTRAVPSIEMIKWKNEDSYQTSCELWIWDQQELFVTVPQAKQKGEELSHLYGARTKFFGGFFFCFGEPFSQMDCKTLDTLLKVNPYEKDKTSLNCVGFHRWHVLFKVTYFTNQCVAYTRYRRCLPSIQGHDWWSMDALCGRGCVKNCWGNIDWRLPGGNHWFKSSNDWHAALLCSCGCAIYKKIPLNKYKKTDDEVSRVKECFFPPITSYQSWQSAQISISMHSEALDTGNGSIKHLWINWYTMYYDHDFKTPDTLVKIWGPPHDNGYPPGAAWRWCMSNNKLAGWETNASGEHCMWLLFLCPMCHYYYCIWLFFDSKYFPGLTFQMLTCDETAKHFLDNAYYNQAFTHGGCICPWGLAISRAYWCLFCFIEWGLIVCDTGQYKQVPAATPNMIADKWLACILQDSEKSHLPKKEDFHLDEQTGCGMLLNKGMFDRMFRFIVREVKNFCSWMASEVGMDEQHRPGEDYLNYRKMVYLDETKFNKSGNRWKPQDEAGHYMAYVGHRKGNAGGQSNPPTYVRQPQTMVFMVMHSDYFCCRIHNMIDWSIFYLWLDMNHLDQHEHNFQWISAMASIVKVPQVNMDNVWRVQFCGVWKSERDICDCFIMDISGVRERTGSSSISKKREAMVQRALAAMNDMEFYDLDTYYRQGQNGVMPFDNYSRGHLNTFIPGSMTFMDDFVWGIDRSRTNEDSDVRYEDFFITHKCLLLWGEVTSWMCYGGRAATHEMDYQNRITANDRTRIQASVCNQLGYDEIFDSDVCGNCGMFWTVGQWNRSRGWLSIWATHQRWDHFWQWVINQVVHHRYFYMRTQKMHSYSATAGGPGGTAFWLIQWVQRKGQDRLQVGGHDNKILKTSIEHHEAMTMHQHKGVWEKAKTNPWARKRFGNWDAMWEGKMYCEGIQKSTKADHNRCAPFNWLIQFHMSHSRAQARFPQNGQTHNVTPLPYFRDHLFWHEYKHNFNSPAAFYFSIQIIDDQGTIMSIDSLHISLNSNWYLSRLEMLEKVFSWGSMNASGNFNQRRDFIEYSWVYGQDQPAEVWQPVRAVNWARCLRYKMQDYFNIWRLPVMWIFTRSPPSGWQFHLELNHEEKHMKTTRKFTKMWANYSIWSRWYNKRWTSRMVFRDASGEYWGPWYFINQLMCMEFHHLHRICTQDCQHNMQFEYWLPDYYAPIKGQAFWASWFVFAFWEWMTWMRNAFNDCNALCVWEKLAFPNVQLEAKDCWCSPTLHSEGPTANMSHNHLTAQQEMIYLAASLYRPNCSVCCNIMTPTRVQIKVYAFRFKNWFNIVAKIAMWDMMHDKEWSEKWCDPWETEPVYANKFSMQIFKCHFDHQVGVFTKCNPCNDGMPRFDREVTLLVMDLMMTGILMQWCWNFRYTNCDGAIGSMCAKVQMFMHCIREYMHDLLIQGCYDYAKDWEFRAKSYKAYLFFYRIAMNNFCVVHVNKDSPPTDSYSYRLAFNWHDEGAQKYYQIIIEVPPSVTWHDGDLNMRHLEHLVVSTPVAYRVLAQCAVGYTGTKVEAINAWDKIMQFIQNECHREHICPNDQYYADYLLKQYIGLYWKPFDCSKPQRIWWKTHEGWIIVPAEIDFTGHRSWSIKCLHVPPWHRYRDQGIPRMRRCSDKEIARPWLCQNSENSFHTEAYSIHCTNMGHWPEKGTPMMVGIWLLISWASYGCYWTCHAAVIDMSAAKWFNEINCWNERGDKTRSGGPNVQGATTGDNEDHFGNDHRMPRTQYLRYIPFPMDLHAQYFEIFLITMWWPPHWTDAHEKEVMRFGEQPCFAAIICGNECHNTETQDGVQSIRKDMIPEIYAKLLNQWVPCDYRWLYVYNSYWHMEDISWACDEHIPDAEYSAAWLPWSCEPWEWWHDEIIAVFCFGVCRRECVHAHSMSLHHGHSSRYNMVDGEEAGGVKHMHLWWHWDLDGLFCKVHSWDDHAISYNYYVMNECTDELVGTQGMNSYNMTLMTWYGEIMSCFFPAGKVLSYYMMAVQPYHYIMHEPMPEAEWRIDFARVINHVWGGVHPLHWTGAYQECNRKKWAHRKTEYYQGKYRAVRPKKTQAADHKSHMMTTNAYWHANEQQSQWMYFLRGKFMQPCNDQCFTSRKRINIKAQYAGVFAPRSWAHNWKCSRYFHIGCSQNGPSYVVQCWQANFLDYDEFEEEVNKRKYNMLGWCILRCIVLNCAVTEWGLGPECKHWCRTRDQAGYWHARRIRMGFDCLSAGPQKIIHHKCAGLQWFDNKCWCRPGTWIEFVCHDKEGDVVEWIKQASTYVKIGVDPWQWGMRVFMKYNSFHVMNYRMQRIYTRGLWSKGGENSFTIPMFMMFRDPQWYQCWFTMPCEWY"
##
##print output_lcs_penalized(lcs_backtrack_penalized(v,w), v, len(v), len(w))
##print output_lcs_penalized(lcs_backtrack_penalized(w,v), w, len(w), len(v))

def simplescore(vi, wj, uk):
    return vi == wj == uk

def multidimensional_align(v, w, u):
    s = [zero_matrix(len(w)+1, len(u)+1) for idx in range(len(v)+1)]
    #v rows, w columns, u stacks
    back = [zero_matrix(len(w)+1, len(u)+1) for idx in range(len(v)+1)]

    for i in range(1, len(v)+1):
        for j in range(1, len(w)+1):
            for k in range(1, len(u)+1):

                s[i][j][k] = max([s[i-1][j][k], s[i][j-1][k], s[i][j][k-1], s[i-1][j-1][k], s[i-1][j][k-1], s[i][j-1][k-1], s[i-1][j-1][k-1] + simplescore(v[i-1], w[j-1], u[k-1])])

                curr = s[i][j][k]

                if curr == s[i-1][j][k]:
                    back[i][j][k] = 'z'
                elif curr == s[i][j-1][k]:
                    back[i][j][k] = 'y'
                elif curr == s[i][j][k-1]:
                    back[i][j][k] = 'x'
                elif curr == s[i-1][j-1][k]:
                    back[i][j][k] = 'zy'
                elif curr == s[i-1][j][k-1]:
                    back[i][j][k] = 'zx'
                elif curr == s[i][j-1][k-1]:
                    back[i][j][k] = 'yx'
                elif curr == s[i-1][j-1][k-1] + simplescore(v[i-1], w[j-1], u[k-1]):
                    back[i][j][k] = 'zyx'
                else:
                    raise ValueError

    print s
    return back

def multidimensional_backtrack(backtrack, v, w, u):
    i = len(v)
    j = len(w)
    k = len(u)

    V, W, U = "", "", ""
    
    while not i == 0 and not j == 0 and not k == 0:
        print i, j, k
        print V, W, U
        move = backtrack[i][j][k]

        print move
        if 'z' in move:
            V += v[i-1]
            i -= 1
        else:
            V += "-"
            
        if 'y' in move:
            W += w[j-1]
            j -= 1
        else:
            W += "-"
            
        if 'x' in move:
            U += u[k-1]
            k -= 1
        else:
            U += "-"

    
    return V[::-1], W[::-1], U[::-1]     

##v = "CTTAGTGAG"
##w = "AAATAAGTT"
##u = "GCGTCTCGCA"
##V = multidimensional_backtrack(multidimensional_align(v,w,u), v, w, u)[0]  

def overlap_alignment(v, w, match = 1, mismatch = -2, indel = -2):

    current_overlap = 1
    best_overlap = None
    best_score = float("-inf")
    best_backtrack = None
    
    max_overlap = min(len(v), len(w)) / 2
    
    while current_overlap < max_overlap:

        v_suffix = v[-current_overlap:]
        w_prefix = w[0:current_overlap]
        
        s = zero_matrix(len(v_suffix)+1, len(w_prefix)+1)
        for idx in range(len(s)):
            s[idx][0] = idx * indel
        for idx in range(len(s[0])):
            s[0][idx] = idx * indel

        backtrack = zero_matrix(len(v_suffix)+1, len(w_prefix)+1)

        for i in range(1, len(v_suffix)+1):
            for j in range(1, len(w_prefix)+1):
                if v_suffix[i-1] == w_prefix[j-1]:
                    s[i][j] = max([s[i-1][j] + indel, s[i][j-1] + indel, s[i-1][j-1] + match])
                #now keep track of which edge was traversed
                    if s[i][j] == s[i-1][j-1] + match:
                        backtrack[i][j] = "diag"
                    elif s[i][j] == s[i-1][j] + indel:
                        backtrack[i][j] = "down"
                    elif s[i][j] == s[i][j-1] + indel:
                        backtrack[i][j] = "right"
                    else:
                        raise ValueError, "Matrix value does not match neighbors"

                else: #mismatch
                    s[i][j] = max([s[i-1][j] + indel, s[i][j-1] + indel, s[i-1][j-1] + mismatch])
                    if s[i][j] == s[i-1][j-1] + mismatch:
                        backtrack[i][j] = "diag"
                    elif s[i][j] == s[i-1][j] + indel:
                        backtrack[i][j] = "down"
                    elif s[i][j] == s[i][j-1] + indel:
                        backtrack[i][j] = "right"
                    else:
                        raise ValueError, "Matrix value does not match neighbors"
        score = s[-1][-1]
        if score > best_score:
            best_score = score
            best_backtrack = backtrack
            best_overlap = current_overlap
        current_overlap += 1

    return best_score, best_backtrack, best_overlap

def overlap_backtrack(backtrack, v, w, overlap):
    v_suffix = v[-overlap:]
    w_prefix = w[0:overlap]

    i, j = len(v_suffix), len(w_prefix)

    V, W = "", ""
    
    while not i == 0 and not j == 0:

        if backtrack[i][j] == "diag":
            V += v_suffix[i-1]
            W += w_prefix[j-1]
            i -= 1
            j -= 1
        elif backtrack[i][j] == "down":
            V += v_suffix[i-1]
            i -= 1
            W += "-"
        elif backtrack[i][j] == "right":
            W += w_prefix[j-1]
            j-=1
            V += "-"
        else:
            print "unrecognized command"
            raise ValueError

    return V[::-1], W[::-1]
