"""Test suite for algdesign_graphcontract."""

import algdesign_graphcontract as alg
import unittest

#####################################
#GRAPH 1:
# 3--4-----5--6
# |\/|     |\/|
# |/\|     |/\|
# 2--1-----7--8
#expected result: 2 cuts

graph1a = """1 2 3 4 7
2 1 3 4
3 1 2 4
4 1 2 3 5
5 4 6 7 8
6 5 7 8
7 1 5 6 8
8 5 6 7"""

#randomly permuted version of above graph; result should be the same
graph1b = """1 4 2 7 3
2 4 1 3
3 1 2 4
4 5 1 2 3
5 8 7 6 4
6 8 5 7
7 6 8 5 1
8 7 6 5"""

#GRAPH 2:
# 3--4-----5--6
# |\/|     |\/|
# |/\|     |/\|
# 2--1     7--8
#expected result: 1 cut

graph2a = """1 2 3 4
2 1 3 4
3 1 2 4
4 1 2 3 5
5 4 6 7 8
6 5 7 8
7 5 6 8
8 5 6 7"""

#randomly permuted version of above graph
graph2b = """1 3 4 2
2 1 4 3
3 1 2 4
4 5 3 2 1
5 4 8 6 7
6 8 7 5
7 5 8 6
8 5 7 6"""

#GRAPH 3: expect 3 cuts
graph3 = """1 19 15 36 23 18 39 
2 36 23 4 18 26 9
3 35 6 16 11
4 23 2 18 24
5 14 8 29 21
6 34 35 3 16
7 30 33 38 28
8 12 14 5 29 31
9 39 13 20 10 17 2
10 9 20 12 14 29
11 3 16 30 33 26
12 20 10 14 8
13 24 39 9 20
14 10 12 8 5
15 26 19 1 36
16 6 3 11 30 17 35 32
17 38 28 32 40 9 16
18 2 4 24 39 1
19 27 26 15 1
20 13 9 10 12
21 5 29 25 37
22 32 40 34 35
23 1 36 2 4
24 4 18 39 13
25 29 21 37 31
26 31 27 19 15 11 2
27 37 31 26 19 29
28 7 38 17 32
29 8 5 21 25 10 27
30 16 11 33 7 37
31 25 37 27 26 8
32 28 17 40 22 16
33 11 30 7 38
34 40 22 35 6
35 22 34 6 3 16
36 15 1 23 2
37 21 25 31 27 30
38 33 7 28 17 40
39 18 24 13 9 1
40 17 32 22 34 38"""


class ContractionTest(unittest.TestCase):
	"""Unit test for merge function"""
	def test_graph1a(self):
		self.assertEqual(alg.multicontract(200, alg.read_graph_direct, graph1a)[0], 2)

	def test_graph1b(self):
		self.assertEqual(alg.multicontract(200, alg.read_graph_direct, graph1b)[0], 2)

	def test_graph2a(self):
		self.assertEqual(alg.multicontract(200, alg.read_graph_direct, graph2a)[0], 1)

	def test_graph2b(self):
		self.assertEqual(alg.multicontract(200, alg.read_graph_direct, graph2b)[0], 1)

	def test_graph3(self):
		self.assertEqual(alg.multicontract(200, alg.read_graph_direct, graph3)[0], 3)
	

suite = unittest.TestLoader().loadTestsFromTestCase(ContractionTest)
unittest.TextTestRunner(verbosity=2).run(suite)