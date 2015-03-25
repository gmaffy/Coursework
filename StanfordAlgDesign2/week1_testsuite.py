import unittest
import week1_greedyalg as alg

#PROBLEM 1, 2: SUBOPTIMAL AND OPTIMAL SCHEDULING
jobs_test_1 = alg.prob1_reader('jobs_test_1.txt')
jobs_test_2 = alg.prob1_reader('jobs_test_2.txt')
jobs_test_3 = alg.prob1_reader('jobs_test_3.txt')

class SchedulingTest(unittest.TestCase):
	def test_set_1(self):
		self.assertEqual(alg.prob1(jobs_test_1),31814)
		self.assertEqual(alg.prob2(jobs_test_1),31814)
	def test_set_2(self):
		self.assertEqual(alg.prob1(jobs_test_2),61545)
		self.assertEqual(alg.prob2(jobs_test_2),60213)
	def test_set_3(self):
		self.assertEqual(alg.prob1(jobs_test_3),688647)
		self.assertEqual(alg.prob2(jobs_test_3),674634)


if __name__ == "__main__":
	suite1 = unittest.TestLoader().loadTestsFromTestCase(SchedulingTest)
	unittest.TextTestRunner(verbosity=2).run(suite1)