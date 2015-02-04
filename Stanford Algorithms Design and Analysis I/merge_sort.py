"""Efficient implementation of MergeSort Algorithm
O(nlogn) on input size.
Written for Stanford Algorithms: Design and Analysis I"""

import unittest, random, time, math
import matplotlib.pyplot as plt

count = 0

def merge(array1, array2):
	"""O(m) algorithm to iteratively merge two arrays into ascending order."""
	merged_array = []
	while len(array1) > 0 or len(array2) > 0:
		if len(array1) > 0 and len(array2) > 0:
			if array1[0] <= array2[0]:
				merged_array.append(array1[0])
				array1.pop(0)
			else:
				merged_array.append(array2[0])
				array2.pop(0)
		elif len(array1) > 0:
			merged_array.append(array1[0])
			array1.pop(0)
		else:
			merged_array.append(array2[0])
			array2.pop(0)
	return merged_array

class MergeTest(unittest.TestCase):
	"""Unit test for merge function"""
	def test_unequallength(self):
		"""Test how merge handles arrays of unequal length"""
		self.assertEqual(merge([1,3,5],[0,4]),[0,1,3,4,5])
	def test_bothsame(self):
		"""Test how merge handles two identical arrays"""
		self.assertEqual(merge([0],[0]),[0,0])
	def test_emptyarray(self):
		"""Test how merge handles an empty array"""
		self.assertEqual(merge([0],[]),[0])
	def test_duplicate(self):
		"""Test how merge handles duplicated numbers"""
		self.assertEqual(merge([1,1],[2,3,4]),[1,1,2,3,4])

suite = unittest.TestLoader().loadTestsFromTestCase(MergeTest)
unittest.TextTestRunner(verbosity=2).run(suite)

def merge_count(array1, array2):
	"""Linear time algorithm to iteratively merge two arrays into ascending order
	while also counting the number of split inversions between the arrays."""
	global count
	merged_array = []
	num_inversions = 0
	while len(array1) > 0 or len(array2) > 0:
		if len(array1) > 0 and len(array2) > 0:
			if array1[0] <= array2[0]:
				merged_array.append(array1[0])
				array1.pop(0)
			else:
				merged_array.append(array2[0])
				array2.pop(0)
				count += len(array1)
				num_inversions += len(array1)
		elif len(array1) > 0:
			merged_array.append(array1[0])
			array1.pop(0)
		else:
			merged_array.append(array2[0])
			array2.pop(0)
	return merged_array, num_inversions

class MergeCountTest(unittest.TestCase):
	"""Unit test for merge_count function."""
	def test_no_inversions(self):
		"""Determine how merge_count handles a case of no inversions"""
		self.assertEqual(merge_count([1,2,3],[4,5,6])[1], 0)
	def test_inversions(self):
		"""Test example provided in course"""
		self.assertEqual(merge_count([1,3,5],[2,4,6])[1], 3)

suite = unittest.TestLoader().loadTestsFromTestCase(MergeCountTest)
unittest.TextTestRunner(verbosity=2).run(suite)	

def count_inversions(array):
	"""MergeSort-based algorithm to count the number of inversions in an array of length n
	in O(nlogn) time."""
	#base case
	if len(array) == 1 or len(array) == 0:
		return array
	else:
		half_index = len(array)/2
		return merge_count(count_inversions(array[0:half_index]), count_inversions(array[half_index::]))[0]

def merge_sort(array):
	"""Recursive MergeSort algorithm to put an array into ascending order and return that sorted array"""
	#base case 
	if len(array) == 1 or len(array) == 0:
		return array 
	else:
		half_index = len(array)/2
		return merge(merge_sort(array[0:half_index]), merge_sort(array[half_index::]))

class MergeSortTest(unittest.TestCase):
	"""Unit test for merge_sort function"""
	def test_presorted(self):
		"""Test how merge_sort deals with an already-sorted list"""
		self.assertEqual(merge_sort([1,2,3,4]),[1,2,3,4])
	def test_unsorted(self):
		"""Test ability of merge_sort to properly sort a list"""
		self.assertEqual(merge_sort([1,6,5,3,2,4]),[1,2,3,4,5,6])
	def test_duplicates(self):
		"""Test ability of merge_sort to handle duplicates."""
		self.assertEqual(merge_sort([0,0,1,2,3]),[0,0,1,2,3])
	def test_randomsort(self):
		"""Test ability of merge_sort to handle a very long array."""
		a = range(100000)
		random.shuffle(a)
		self.assertEqual(merge_sort(a), sorted(a))

suite = unittest.TestLoader().loadTestsFromTestCase(MergeSortTest)
unittest.TextTestRunner(verbosity=2).run(suite)

# #read in file
# with open("IntegerArray.txt", 'r') as read_file:
# 	int_array = [int(line) for line in read_file]

# #count inversions in file
# sorted_array = count_inversions(int_array)
# print 'Number of inversions in integer array:', count

# #Runtime analysis of MergeSort

# def sort_timetest(input_size, sort_function):
# 	array = range(input_size)
# 	random.shuffle(array)
# 	start_time = time.time()
# 	dummy = sort_function(array)
# 	end_time = time.time()
# 	return end_time - start_time

# n = range(2,100)
# y = [sort_timetest(i, merge_sort) for i in n]
# big_o = [i * math.log(i) for i in n]

# plt.plot(n,y,'r',n,big_o,'b')
# plt.show()