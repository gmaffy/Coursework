




def problem1_reader(filename):
	output = [] #store each node as (value, size)
	with open(filename, 'r') as fo:
		for idx, line in enumerate(fo:)
			if idx == 0:
				capacity = int(line.split()[0])
			else:
				value, weight = line.split()
				output.append(int(value), int(weight))
	return output

def problem1_knapsack(capacity, value_size_list):

	#initialize first row x=0,1,2...,capacity to zero
	A = [[0 if dummy2 == 0 else None for dummy1 in range(capacity)] for dummy2 in range(len(value_size_list))]

	for i in range(1,len(value_size_list)):
		for x in range(capacity):
			value_i, weight_i = value_size_list[i]
			if weight_i > x:
				A[i][x] = A[x][i-1]
			else:
				A[x,i] = max(A[x][i-1], A[x-weight_i][i-1] + value_i)
	return A[capacity][len(value_size_list)]

