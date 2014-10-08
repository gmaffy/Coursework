"""PatternCount algorithm for Bioinformatics"""

def pattern_count(text, pattern):
    """Input two strings and return number of times string pattern appears within
    string text"""
    count = 0
    for index in range(len(text)-len(pattern)):
        if text[index:index+len(pattern)] == pattern:
            count+=1
    return count

def reverse_complement(pattern):
    """Return reverse complement of pattern"""
    dna_revcomps = {'A' : 'T', 'T' : 'A', 'C' : 'G', 'G' : 'C'}
    rev_comp = ""
    for base in pattern[::-1]:
        rev_comp += dna_revcomps[base]
    return rev_comp

def pattern_count_with_revcomps(text, pattern):
    return pattern_count(text, pattern) + pattern_count(text, reverse_complement(pattern))

def hamming_distance(str1, str2):
    """Input two strings of equal length and count mismatches between them"""
    assert len(str1) == len(str2)
    hamming_count = 0
    for index in range(len(str1)):
        if str1[index] != str2[index]:
            hamming_count += 1
    return hamming_count

def approximate_pattern_find(text, pattern, hamming_dist):
    """Return count of occurrances of pattern within text, including
    variants of pattern where the hamming distance from the variant to
    the pattern is less than hamming_dist"""
    index_list = list()
    for index in range(len(text)-len(pattern)+1):
        if text[index:index+len(pattern)] == pattern:
            index_list.append(index)
        elif hamming_distance(pattern, text[index:index+len(pattern)]) <= hamming_dist:
            index_list.append(index)
    return index_list

def approximate_pattern_count(text, pattern, hamming_dist):
    return len(approximate_pattern_find(text, pattern, hamming_dist))
