"""Two faster implementations of FrequentWords
First relies on creating an array of all possible kmers within a string
by assigning each possible kmer a numeric code, then sliding once through the string
and incrementing the counts in the array.
Second relies on assigning each kmer a numeric code during one slide through the string,
then sorting the list of codes and finding the longest run of consecutive entries.
Also contains algorithms that extend the ability of FrequentWords in order to allow
for mismatches."""

import bioin_patterncount as patterncount
import itertools

def pattern_to_number(pattern):
    """Input oligo and return integer representing its lexicographic order
    among oligos of the same length (e.g. AA = 0, AC = 1, etc.)"""
    trans_table = {'A' : 0, 'C' : 1, 'G' : 2, 'T' : 3}
    total = 0
    multiplier = 1
    for letter in pattern[::-1]:
        total += trans_table[letter] * multiplier
        multiplier *= 4
    return total

def convert_to_base(number, base):
    """Convert base 10 number to base specified by second argument"""
    if number == 0:
        return number
    number_string = ""
    dividend = number
    remainder = 0
    while not dividend == 0:
        remainder = dividend % base
        dividend = dividend / base
        number_string += str(remainder)
    return int(number_string[::-1])
        
def number_to_pattern(number, seq_length):
    """Reverse process of pattern_to_number"""
    trans_table = {'0' : 'A', '1' : 'C', '2' : 'G', '3' : 'T'}
    num_string = str(convert_to_base(number, 4))
    pattern = ""
    for digit in num_string:
        pattern += trans_table[digit]
    if len(pattern) < seq_length:
        return "A" * (seq_length - len(pattern)) + pattern
    else:
        return pattern

def computing_frequencies(text, k):
    """Array-based method to compute most frequent k-mers in text
    in O(len(text) * k)"""
    frequency_array = list()
    for index in range(4 ** k):
        frequency_array.append(0)
    for index in range(len(text)-k+1):
        pattern = text[index:index+k]
        code = pattern_to_number(pattern)
        frequency_array[code] = frequency_array[code] + 1
    return frequency_array

def write_answer(array, filename):
    """Write comma-separated array to text file in format preferred by course"""
    fo = open(filename, 'w')
    for item in array:
        fo.write(str(item)+' ')
    fo.close()

def faster_frequent_words(text, k):
    """Use frequency array to compute most frequent k-mers in text"""
    frequent_patterns = set([])
    frequency_array = computing_frequencies(text, k)
    max_count = max(frequency_array)
    for index in range(4 ** k):
        if frequency_array[index] == max_count:
            pattern = number_to_pattern(index, k)
            frequent_patterns = frequent_patterns.union(set([pattern]))
    return (frequent_patterns, max_count)

def frequent_words_by_sorting(text, k):
    """Find most frequent k-mer by assigning each possible k-mer an index, sorting,
    then counting the longest run of the same index"""
    frequent_patterns = set([])
    index_list = list()
    count_list = list()
    for index in range(len(text)-k+1):
        pattern = text[index:index+k]
        index_list.append(pattern_to_number(pattern))
        count_list.append(1)
    index_list.sort()
    for index in range(1,len(text)-k+1):
        if index_list[index] == index_list[index - 1]:
            count_list[index] = count_list[index - 1] + 1
    max_count = max(count_list)
    for index in range(len(text) - k + 1):
        if count_list[index] == max_count:
            pattern = number_to_pattern(index_list[index], k)
            frequent_patterns = frequent_patterns.union(set([pattern]))
    return (frequent_patterns, max_count)

ALL_KMERS = list()
def all_possible_kmers(k):
    """Function to compute all possible sequences of length k"""
    #store output as global variable; should increase efficiency
    #if same kmer length will be used on multiple datasets
    global ALL_KMERS
    if len(ALL_KMERS)>0 and len(ALL_KMERS[0]) == k:
        pass
    else:
        possibilities = [i for i in itertools.product('AGCT', repeat = k)]
        joined_possibilities = list()
        for tup in possibilities:
            joined_possibilities.append(''.join(tup))
        ALL_KMERS = joined_possibilities
    return ALL_KMERS

def frequent_words_with_mismatches_v1(text, k, hamming_dist):
    """Find the most frequent word(s) of length within a text, allowing up to
    hamming_dist mismatches. N.B. that the most frequent word need not actually
    occur in the text -- for example, input ("ATATA", 3, 2) returns 10 distinct
    patterns that occur twice, despite the fact that there are only two distinct
    3-mers that actually occur in the text, and one of those patterns that
    actually does occur in the text ('TAT') is not one of the most frequent
    3-mers. Runs very inefficiently; use v3 instead!"""
    #enumerate all possible kmers
    possible_kmers = set(all_possible_kmers(k))
    #enumerate kmers that actually occur in text
    patterns_in_text = list()
    for index in range(len(text)-k+1):
        pattern = text[index:index+k]
        patterns_in_text.append(pattern)
    print patterns_in_text
    #pare down to those that are within hamming_dist of each pattern in text
    relevant_kmers = set([])
    for kmer in possible_kmers:
        for pattern in patterns_in_text:
            if patterncount.hamming_distance(pattern, kmer) <= hamming_dist:
                relevant_kmers = relevant_kmers.union(set([kmer]))
                break
            else:
                pass
    relevant_kmers = relevant_kmers.union(patterns_in_text) #add all patterns that actually occur in text!
    #initialize frequency array
    frequency_array = list()
    for index in range(4 ** k):
        frequency_array.append(0)
    #loop through text and count frequencies
    for pattern in patterns_in_text:
        pattern_list = [kmer for kmer in relevant_kmers if patterncount.hamming_distance(kmer, pattern) <= hamming_dist]
        pattern_list = set(pattern_list)
        pattern_list = pattern_list.union(set([pattern]))
        code_list = [pattern_to_number(pat) for pat in pattern_list]
        for code in code_list:
            frequency_array[code] = frequency_array[code] + 1
    #count most frequent patterns
    frequent_patterns = set([])
    max_count = max(frequency_array)
    for index in range(4 ** k):
        if frequency_array[index] == max_count:
            pattern = number_to_pattern(index, k)
            frequent_patterns = frequent_patterns.union(set([pattern]))
    return (frequent_patterns, max_count)    

def frequent_words_with_mismatches_v2(text, k, hamming_dist):
    """(Failed) attempt to improve the efficiency of v1"""
    #initialize frequency array
    frequency_array = list()
    for index in range(4 ** k):
        frequency_array.append(0)
    #list all patterns in text
    patterns_in_text = list()
    for index in range(len(text)-k+1):
        pattern = text[index:index+k]
        patterns_in_text.append(pattern)
    #create list of all possible kmers
    possible_kmers = all_possible_kmers(k)
    #go through patterns and compare to kmers
    for pattern in patterns_in_text:
        for kmer in possible_kmers:
            if patterncount.hamming_distance(pattern, kmer) <= hamming_dist:
                frequency_array[pattern_to_number(kmer)] = frequency_array[pattern_to_number(kmer)] + 1
    frequent_patterns = set([])
    max_count = max(frequency_array)
    for index in range(4 ** k):
        if frequency_array[index] == max_count:
            pattern = number_to_pattern(index, k)
            frequent_patterns = frequent_patterns.union(set([pattern]))
    return (frequent_patterns, max_count)

def find_neighbors(kmer, hamming_dist, letters = 'AGCT'):
    """Helper generator to find all kmers within hamming_dist of the starting
    kmer."""
    for indices in itertools.combinations(range(len(kmer)), hamming_dist):
        this_kmer = [[char] for char in kmer]
        for index in indices:
            orig_char = kmer[index]
            #this_kmer[index] = [l for l in letters if l != orig_char] #uncomment this if you want to coerce there into being hamming_dist mutations
            this_kmer[index] = [l for l in letters]
        for poss in itertools.product(*this_kmer):
            yield ''.join(poss)

def frequent_words_with_mismatches_v3(text, k, hamming_dist):
    """Find frequent words with mismatches by first identifying neighbors
    of each substring and counting them. Most efficient algorithm; use this one!!!!"""
    #initialize frequency array
    frequency_array = list()
    for index in range(4 ** k):
        frequency_array.append(0)
    #loop through text and identify substrings of length k
    for index in range(len(text)-k+1):
        pattern = text[index:index+k]
    #for each substring, identify all possible neighbors within hamming_dist
        neighbors = set(find_neighbors(pattern, hamming_dist))
        neighbors = neighbors.union(set([pattern]))
    #count the substring and its neighbors
        for string in neighbors:
            frequency_array[pattern_to_number(string)] = frequency_array[pattern_to_number(string)] + 1
    #find the most common item(s) among the frequency array
    frequent_patterns = set([])
    max_count = max(frequency_array)
    for index in range(4 ** k):
        if frequency_array[index] == max_count:
            pattern = number_to_pattern(index, k)
            frequent_patterns = frequent_patterns.union(set([pattern]))
    return (frequent_patterns, max_count)
