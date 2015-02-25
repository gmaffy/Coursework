
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
				num_targets += 1
				break
			else:
				pass
	return num_targets

print two_sum(integers_to_hash('algo1-programming_prob-2sum.txt'))