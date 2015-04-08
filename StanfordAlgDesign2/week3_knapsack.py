




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

FILENAME = "knapsack1.txt"
cap, v_s_list = problem1_reader(FILENAME)
#print cap
#print v_s_list
print problem1_knapsack(cap, v_s_list)