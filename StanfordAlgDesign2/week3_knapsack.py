"""Week 3 of Stanford's Algorithms: Design & Analysis II: the Dynamic Programming Paradigm.

Problem 1 asks for a naive implementation of a dynamic algorithm to solve the knapsack problem.
The input is a list of values and weights for hypothetical objects. The goal is to determine
the combination of items that maximize value, subject to a cosntraint on total item weight
called capacity. This algorithm can be efficiently and correctly solved by a dynamic approach
on a two-dimensional array.

Problem 2 asks for an efficient implementation of the knapsack algorithm on a dataset that
is too large to store in memory at any one time. My implementation uses the insight that the 
dynamic algorithm only considers two columns of the two-dimensional array at any one time: i.e.,
all relevant information from previous columns is reflected in the most recent two columns.
Therefore we can use a generator to examine items one at a time, storing only the two most
recent columns of the array as we go and discarding older columns."""


import time


##################################################

def problem1_reader(filename):
	output = [] #store each node as (value, size)
	with open(filename, 'r') as fo:
		for idx, line in enumerate(fo):
			if idx == 0:
				capacity = int(line.split()[0])
			else:
				value, weight = line.split()
				output.append((int(value), int(weight)))
	return capacity, output

def problem1_knapsack(capacity, value_size_list):

	#initialize first row x=0,1,2...,capacity to zero
	A = [[0 if dummy2 == 0 else None for dummy1 in range(capacity)] for dummy2 in range(len(value_size_list))]
	#print len(A), len(A[0])
	#print len(value_size_list), capacity
	for i in range(1,len(value_size_list)):
		for x in range(capacity):
			#print i, x
			value_i, weight_i = value_size_list[i]
			#print value_i, weight_i
			if weight_i > x:
				A[i][x] = A[i-1][x]
			else:
				A[i][x] = max(A[i-1][x], A[i-1][x-weight_i] + value_i)
	return A[len(value_size_list)-1][capacity-1]

##################################################

def problem2_knapsack(filename):
	start = time.time()
	with open(filename) as fo:
		for idx, line in enumerate(fo):
			print "line", idx, '\t'+"elapsed", time.time() - start
			if idx == 0:
				capacity = int(line.split()[0])
				#initialize the mini-array
				A = [[0 if dummy2 == 0 else None for dummy1 in range(capacity)] for dummy2 in range(2)]
			else:
				for x in range(capacity):
					value_i, weight_i = int(line.split()[0]), int(line.split()[1])
					if weight_i > x:
						A[1][x] = A[0][x]
					else:
						A[1][x] = max(A[0][x], A[0][x-weight_i] + value_i)
				#dump the first row of the cache, move down the second row
				A[0] = A[1]
				A[1] = [None for dummy1 in range(capacity)] #replace the second row with None's
	return A[0][capacity-1]

##################################################

def weighted_independent_sets(path_graph_array):
	"""Input: path_graph array should be a list of integer weights assigned to each node
	in a linear path graph.
	Output will be the maximum possible sum of weights over non-adjacent nodes in the graph."""
	S = 0
	i = len(path_graph_array) - 1
	while i>=0:
		if path_graph_array[i-1]>=path_graph_array[i-2]+path_graph_array[i]:
			i-=1
		else:
			i-=2
			S+=path_graph_array[i]
	return S

print weighted_independent_sets([4,4,5,4])


if __name__ == "__main__":
	pass

	#PROBLEM 1
	# FILENAME = "knapsack1.txt"
	# cap, v_s_list = problem1_reader(FILENAME)
	# print problem1_knapsack(cap, v_s_list)

	#PROBLEM 2
	# print problem2_knapsack("knapsack_big.txt")
