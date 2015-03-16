"""Script to solve two basic data structure problems:
1) The Two-Sum problem: given an array A of integers (positive or negative) and a target sum T,
determine whether there are two distinct integers in A, x and y, such that x+y=T. 
Can be implemented efficiently by loading A into a hash table.

2) The Median Maintenance problem: given a stream of integers, arriving one-by-one from an unsorted
array, determine the median of the integers at any given point in time.
Can be implemented efficiently using two heaps: one min and one max."""

import heap

#####################################################
################ PROBLEM 1: TWO-SUM #################
#####################################################

def integers_to_hash(filename):
	hash = dict()
	with open(filename, 'r') as fo:
		for line in fo:
			hash[int(line)] = True
	return hash

def two_sum(hash_table):
	target_range = range(-10000,10001)
	num_targets = 0
	for twosum in target_range:
		if not twosum % 100:
			print twosum, num_targets
		for key in hash_table.keys():
			if (twosum - key) in hash_table and not key == (twosum - key):
				print twosum, key, twosum - key
				num_targets += 1
				break
			else:
				pass
	return num_targets


#print two_sum(integers_to_hash('algo1-programming_prob-2sum.txt'))

#####################################################
########### PROBLEM 2: MEDIAN MAINTENANCE ###########
#####################################################

def median_maintainance(filename):

	median_array = [] #maintain a running array of the median at each time step
	min_heap = heap.MinHeap() #use min heap to store elements larger than the current median
	max_heap = heap.MaxHeap() #use max heap to store elements smaller than the current median

	##initialize data stream
	with open(filename, 'r') as stream:
		for line in stream:
			new_data = int(line.strip())
			#print new_data
			if min_heap.size() == max_heap.size() == 0: #first data point
				median = new_data
				min_heap.insert(new_data)
				median_array.append(median)

			elif max_heap.size() == 0: #second data point
					if new_data <= min_heap.show_min():
						max_heap.insert(new_data) #easy case -- new data belongs in max heap
					else: #complicated case -- new data belongs in min heap, but data in min heap needs to be bumped down
						max_heap.insert(min_heap.extract_min())
						min_heap.insert(new_data)
					median = max(max_heap.array) #by convention, if two heaps are equal sized median is root of max_heap
					median_array.append(median)

			else:
				##load new data into the appropriate heap
				
				if new_data <= min_heap.show_min(): #new data is in the lower half of total dataset
					max_heap.insert(new_data)
				else:
					min_heap.insert(new_data)

				#print max_heap, min_heap
				##find the median
				if min_heap.size() == max_heap.size():
					#if heaps are equally sized, median is average of two roots
					median = max(max_heap.array)
					median_array.append(median)
					#no rebalancing needed -- we are done with this round

				else:
					if min_heap.size() > max_heap.size():
						#if min heap is bigger, median is the root of min heap
						rebal = min(min_heap.array)
						min_heap.array.remove(rebal)
						#rebalance the heaps by loading the former root of the min heap into the max heap
						max_heap.insert(rebal)

					else:
						#if max heap is bigger, median is root of max heap
						rebal = max(max_heap.array)
						max_heap.array.remove(rebal)
						#rebalance the heaps by loading the former root of the max heap into the min heap
						min_heap.insert(rebal)

					#if two heaps are same size after rebalancing, take mean of two roots
					if min_heap.size() == max_heap.size():
						median = max(max_heap.array)
					elif min_heap.size() < max_heap.size():
						median = max(max_heap.array)
					else:
						median = min(min_heap.array)
					median_array.append(median)
				print max(max_heap.array), min(min_heap.array), max_heap.size(), min_heap.size()

	#print 5000 in max_heap.array
	print sum(median_array)
	
	return sum(median_array)%10000

def median_maintainance_from_array(stream):

	median_array = [] #maintain a running array of the median at each time step
	min_heap = heap.MinHeap() #use min heap to store elements larger than the current median
	max_heap = heap.MaxHeap() #use max heap to store elements smaller than the current median

	##initialize data stream
	for integer in stream:
			new_data = integer
			#print new_data
			if min_heap.size() == max_heap.size() == 0: #first data point
				median = new_data
				min_heap.insert(new_data)
				median_array.append(median)

			elif max_heap.size() == 0: #second data point
					if new_data <= min_heap.show_min():
						max_heap.insert(new_data) #easy case -- new data belongs in max heap
					else: #complicated case -- new data belongs in min heap, but data in min heap needs to be bumped down
						max_heap.insert(min_heap.extract_min())
						min_heap.insert(new_data)
					median = max(max_heap.array) #by convention, if two heaps are equal sized median is root of max_heap
					median_array.append(median)

			else:
				##load new data into the appropriate heap
				
				if new_data <= min_heap.show_min(): #new data is in the lower half of total dataset
					max_heap.insert(new_data)
				else:
					min_heap.insert(new_data)

				#print max_heap, min_heap
				##find the median
				if min_heap.size() == max_heap.size():
					#if heaps are equally sized, median is average of two roots
					median = max(max_heap.array)
					median_array.append(median)
					#no rebalancing needed -- we are done with this round

				else:
					if min_heap.size() > max_heap.size():
						#if min heap is bigger, median is the root of min heap
						rebal = min(min_heap.array)
						min_heap.array.remove(rebal)
						#rebalance the heaps by loading the former root of the min heap into the max heap
						max_heap.insert(rebal)

					else:
						#if max heap is bigger, median is root of max heap
						rebal = max(max_heap.array)
						max_heap.array.remove(rebal)
						#rebalance the heaps by loading the former root of the max heap into the min heap
						min_heap.insert(rebal)

					#if two heaps are same size after rebalancing, take mean of two roots
					if min_heap.size() == max_heap.size():
						median = max(max_heap.array)
					elif min_heap.size() < max_heap.size():
						median = max(max_heap.array)
					else:
						median = min(min_heap.array)
					median_array.append(median)
				print max(max_heap.array), min(min_heap.array)

	print sum(median_array)
	
	return sum(median_array)%10000

print median_maintainance_from_array([int(i) for i in """3
7
4
1
2
6
5""".split()])
print median_maintainance('Median.txt')