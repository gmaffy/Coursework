import math, random

def neighbors(pattern, d):
    """Helper function to recursively find all kmers within d of the starting kmer.
    Recursive alternative to find_neighbors."""
    if d == 0:
        return set([pattern])
    if len(pattern)==1:
        return set(['A', 'G', 'C', 'T'])
    neighborhood = set([])
    first, suffix = pattern[0], pattern[1::]
    suffix_neighbors = neighbors(suffix, d)
    for text in suffix_neighbors:
        if hamming_distance(suffix, text) < d:
            for nucleotide in 'AGCT':
                neighborhood = neighborhood.union([nucleotide + text])
        else:
            neighborhood = neighborhood.union([first + text])
    return neighborhood

def hamming_distance(str1, str2):
    """Input two strings of equal length and count mismatches between them"""
    assert len(str1) == len(str2)
    hamming_count = 0
    for index in range(len(str1)):
        if str1[index] != str2[index]:
            hamming_count += 1
    return hamming_count

def substrings(string, k):
    """Return all substrings of length k in a string"""
    subs = set([])
    for idx in range(len(string)-k+1):
            subs = subs.union(set([string[idx:idx+k]]))
    return subs

def redundant_substrings(string, k):
    subs = []
    for idx in range(len(string)-k+1):
        subs.append(string[idx:idx+k])
    return subs

def patterns_in_dna(dna, k):
    """Return all kmers in collection of strings dna"""
    kmers = set([])
    for string in dna:
        kmers = kmers.union(substrings(string, k))
    return kmers

def pattern_in_all_dna_strings(dna, pattern, d):
    """Return True if pattern appears in each string within dna with at most
    d mismatches; otherwise return False"""
    bool_list = []
    for string in dna:
        string_bool_list = []
        for sub in substrings(string, len(pattern)):
            if hamming_distance(sub, pattern) <= d:
                string_bool_list.append(True)
            else:
                string_bool_list.append(False)
        bool_list.append(any(string_bool_list))
    return all(bool_list)

def motif_enumeration(dna, k, d):
    """For collection of strings dna and integers k and d, return all
    (k, d)-motifs in dna"""
    patterns = set([])
    pat_in_dna = patterns_in_dna(dna, k)
    for pattern in pat_in_dna:
        for kmer in neighbors(pattern, d):
            if pattern_in_all_dna_strings(dna, kmer, d):
                patterns = patterns.union(set([kmer]))
    return patterns

#dnas = ["ATTTGGC","TGCCTTA","CGGTATC","GAAAATT"]
#print motif_enumeration(dnas, 3, 1)
#dnas = ["AATGTACCTCACATACGGCCTCGAC","CCCATAGCCAGCAGACGGTAATTGT","TGTCGAATGGTTCGACTACTGACAC","CTGCGTTAGGATTGAAATGACTCTA","GAATGAATGATATTGATTATGCCTG","ATTGTAAATGAAGCGAGTCTACGTT"]
#m = motif_enumeration(dnas, 5, 2)

def listofiterables_to_columns(list_of_iterables):
    """Convert list of iterables (strings, lists, etc.) to column matrix"""
    column_list = []
    for idx in range(len(list_of_iterables[0])):
        column_list.append([row[idx] for row in list_of_iterables])
    return column_list

def frequency_matrix(list_of_strings):
    """Turn a list of DNA strings of equal length into a matrix of
    nucleotide frequencies"""
    nucleotides = "A G C T".split()
    col_matrix = listofiterables_to_columns(list_of_strings)
    freq_dict = {nuc : [] for nuc in nucleotides}
    for col in col_matrix:
        for nuc in nucleotides:
            freq_dict[nuc].append(col.count(nuc)/float(len(col)))
    return freq_dict

def log2_special(num):
    """Take base2 log of num where log(0) is defined to be zero"""
    if float(num) == 0.0:
        return 0.0
    else:
        return math.log(num, 2)

def entropy(frequency_dictionary):
    """For dictionary of frequency of occurrance of nucleotides, return
    Shannon entropy for each column"""
    entropies = []
    for idx in range(len(frequency_dictionary.values()[0])):
        col_entropies = []
        for nuc in frequency_dictionary.keys():
            n = frequency_dictionary[nuc][idx]
            col_entropies.append(n * log2_special(n))
        entropies.append(-1.0*sum(col_entropies))
    #return [-1.0 * sum([n*log2_special(n) for n in frequency_dictionary[nuc][idx]
    #entropy_list = [[-1.0*sum([n * log2_special(n)]) for n in frequency_dictionary[nuc]] for nuc in frequency_dictionary.keys()]
    return entropies

#dna_strings = ["TCGGGGGTTTTT","CCGGTGACTTAC","ACGGGGATTTTC","TTGGGGACTTTT", "AAGGGGACTTCC","TTGGGGACTTCC","TCGGGGATTCAT","TCGGGGATTCCT","TAGGGGAACTAC","TCGGGTATAACC"]
#print entropy(frequency_matrix(dna_strings))

def d(pattern, motifs):
    score = 0
    """For a collection of strings (or a long string) motifs, return sum of hamming distances
    between the pattern and each motif"""
    if type(motifs) == "a":
        subs = substrings(motifs, len(pattern))
        for substring in sums:
            score+=hamming_distance(substring, pattern)
    elif type(motifs) == type([1,2]):
        for string in motifs:
            score += hamming_distance(pattern, string)
    return score

def motif(pattern, text):
    """Return the kmer of length pattern within the longer string text that minimizes
    hamming distance between kmer and pattern"""
    subs = substrings(text, len(pattern))
    min_score = float("inf")
    best_candidate = ""
    for substring in subs:
        if hamming_distance(substring, pattern) < min_score:
            min_score = hamming_distance(substring, pattern)
            best_candidate = substring
    return best_candidate

def min_score(pattern, dna):
    """For a short string pattern and a collection of strings dna,
    return the minimum hamming distance between the pattern and each
    substring in the strings within dna"""
    score = 0
    for string in dna:
        score_list = []
        subs = substrings(string, len(pattern))
        for substring in subs:
            score_list.append(hamming_distance(pattern, substring))
        score += min(score_list)
    return score

##print d("GGC", ["AAG", "AAG", "CAC", "CAA"])
##print min_score("GGC", ["AAG", "AAG", "CAC", "CAA"])
##
##strings = ["GCG","AAG", "AAG", "ACG", "CAA"]
##for idx, string in enumerate(strings):
##    print min_score(string, strings[0:idx]+strings[idx+1::])

def score(motifs):
    """For a collection of strings of equal length motifs, return the sum of the number of mismatches from the
    most frequent base in each column"""
    #find most frequent base in each column
    s = float("inf")
    for idx, string in enumerate(motifs):
        if s > min_score(string, motifs[0:idx]+motifs[idx+1::]):
            s = min_score(string, motifs[0:idx]+motifs[idx+1::])
    return s
    
def most_frequent_nucleotides(dna):
    """Find most frequent nucleotide in each column"""
    nucleotides = "A G C T".split()
    most_frequent_nucleotides = []
    column_matrix = listofiterables_to_columns(dna)
    for col in column_matrix:
        current_count = 0
        for nuc in nucleotides:
            if col.count(nuc) > current_count:
                current_count = col.count(nuc)
                best_nuc = nuc
        most_frequent_nucleotides.append(best_nuc)
    return most_frequent_nucleotides     

def score2(dna):
    """Alternative to score"""
    most_frequent_nuc = most_frequent_nucleotides(dna)
    col_matrix = listofiterables_to_columns(dna)
    scores = []
    for idx, col in enumerate(col_matrix):
        running_score = 0
        for item in col:
            if not item == most_frequent_nuc[idx]:
                running_score += 1
        scores.append(running_score)
    return sum(scores)

def median_string(dna, k):
    """For list of strings dna and integer k, return kmer pattern that minimizes
    min_score(pattern, dna) among all kmers pattern"""
    distance = float("inf")d
    median = ""
    all_kmers_list = [list(substrings(string,k)) for string in dna]
    flat_kmers_list = [item for sublist in all_kmers_list for item in sublist]
    for pattern in flat_kmers_list:
        if distance > min_score(pattern, dna):
            distance = min_score(pattern, dna)
            median = pattern
    return median

def profile_probability(profile_dictionary, kmer):
    """Compute probability of obtaining a given nucleotide string kmer, given a dictionary of probabilities
    of particular nucleotides at given positions."""
    probability = 1.0
    for idx, base in enumerate(kmer):
        probability *= profile_dictionary[base][idx]
    return probability

##profile = {"A":  [float(i) for i in ".2  .2   0   0   0   0  .9  .1  .1  .1  .3   0".split()],          
##"C":  [float(i) for i in ".1  .6   0   0   0   0   0  .4  .1  .2  .4  .6".split()],
##"G":   [float(i) for i in "0   0   1   1  .9  .9  .1   0   0   0   0   0".split()], 
##"T":  [float(i) for i in ".7  .2   0   0  .1  .1   0  .5  .8  .7  .3  .4".split()]}
##
##print profile_probability(profile, "TCGTGGATTTCC")

def profile_most_probable_kmer(profile_dictionary, text, k):
    """Given a dictionary of probabilities of particular nucleotides at given positions profile_dictionary,
    a string text, and an integer k, find the most probable substring of length k within text"""
    most_probable_kmer = ""
    p_kmer = float("-inf")
    possible_subs = redundant_substrings(text, k)
    for substring in possible_subs:
        p_current = profile_probability(profile_dictionary, substring)
        if p_current > p_kmer:
            p_kmer, most_probable_kmer = p_current, substring
    return most_probable_kmer

def four_strings_to_profile(list_of_strings):
    """Formatting function: convert four strings of numbers to profile dictionary"""
    profile_dict = dict()
    profile_dict["A"] = [float(i) for i in list_of_strings[0].split()]
    profile_dict["C"] = [float(i) for i in list_of_strings[1].split()]
    profile_dict["G"] = [float(i) for i in list_of_strings[2].split()]
    profile_dict["T"] = [float(i) for i in list_of_strings[3].split()]
    return profile_dict

##profile = four_strings_to_profile(["0.2 0.2 0.3 0.2 0.3","0.4 0.3 0.1 0.5 0.1","0.3 0.3 0.5 0.2 0.4","0.1 0.2 0.1 0.1 0.2"])
##print profile_most_probable_kmer(profile, "ACCTGTTTATTGCCTAAGTTCCGAACAAACCCAATATAGCCCGAGGGCCT", 5)
##
##profile = four_strings_to_profile(["0.141 0.169 0.282 0.197 0.282 0.239 0.239 0.268 0.268 0.239 0.225 0.155 0.324 0.324",
##"0.211 0.225 0.268 0.197 0.254 0.211 0.254 0.239 0.296 0.197 0.268 0.239 0.268 0.239",
##"0.239 0.352 0.254 0.338 0.239 0.352 0.239 0.254 0.254 0.296 0.338 0.282 0.268 0.211",
##"0.408 0.254 0.197 0.268 0.225 0.197 0.268 0.239 0.183 0.268 0.169 0.324 0.141 0.225"])
##print profile_most_probable_kmer(profile, "TTTATATCTTCTACCCAACCCTTCTCTCGCCCCGTATCCTAAGGGTAGGAAAACCTCCGGCAGCAATACTGCCTGTCAGAATCTAAGAAGCGAATTAAGAAGGCCCCCACAGCAGGCGCCGGAGGCGAAGTCAACAGTCCGCTTTGAGGACCGGTAGAGTGGCACCTTCGGGTGAGACGCTTCAAGAGTTCGGTTTTTGCCTCCTTTCATCAAGTAAGGTTACCAGCTAGTGGTCCGTGGTTGATCCCGTCCCTGAACTCTAAATGAGGACACCTTAGATACTCTATGTCTGGTCGCGAACGAATACCGGCATATTTCGCGAACCGCGAGCAGGGTTCGTTATTCCAGCATGCCAGTGATACTCAGGCTTAAAGGAGAGCCGAATACTCTGTAATGAGAACTCCTAATCCTGACGAGAAGTAAGCGCGGCTTAGCATTGCTATTGTCGTAGTTATGTGAAGGGCCCAAAAACGGTGTCACATAATATTGCGTGGTAATAAGGAACTGCTTACGTTGACGCACGGCTAACGCACACTCAAATATCCACAGTTAGCAAATTGTGCGATCATGTTGTGTATAGCACCCCTTTGTGCCGTCGCCGGCCATGTAGAACGATTTTGTTTTTAATTTGCCGTGCTGATCAACGGAAATGAATGCGTACAGAACTGCGGTCCTTCTACTCTACCTACCGCCCCCCCATTACAGCTTAAATATGTCGACGCCTGCACACAATGTCCAGGAAGGTCCCTTCGGCGAGAGGAATGTATTAATTAGGATTGAAAGCGAGTAAAACCCTATCTTCCCGCACATTCGTGTTGGAGGAGACGAGGGTACGAGACTATCCTATGTGACTTTTTCTTACAGCAAATCTAGCAACCGACGAAGGGGCTCATGACAGTCGGCCTCTAATAAAGTAGTCACCCGGGTCTCTATCCAAATCTCCAGACCCTATGACATCACATTCAGGGATGACCCTATCGATTAAACAGGTTGGACTGGC", 14)

def greedy_motif_search(dna, k, t):
    """Iteratively finds k-mers in the first string from Dna, second string from Dna, third string from Dna, etc.
    After finding i - 1 k-mers Motifs in the first i - 1 strings of Dna, this algorithm constructs Profile(Motifs)
    and selects the Profile-most probable k-mer from the i-th string based on this profile matrix."""
    best_motifs = [line[0:k] for line in dna]
    motifs_list = [list(redundant_substrings(dna[i],k)) for i in range(len(dna))]
    initial_prof_dict = frequency_matrix(best_motifs)
    for idx, kmer in enumerate(motifs_list[0]):
        current_motifs = [kmer]
        current_profile = frequency_matrix(listofiterables_to_columns(kmer))
        for idx2 in range(1,len(dna)):
            current_motifs.append(profile_most_probable_kmer(current_profile, dna[idx2], k))
            current_profile = frequency_matrix(current_motifs)
        if score(current_motifs) < score(best_motifs):
            best_motifs = current_motifs
            
    
    return best_motifs        
    
#print greedy_motif_search("""GGCGTTCAGGCA AAGAATCAGTCA CAAGGAGTTCGC CACGTCAATCAC CAATAATATTCG""".split(),3,5)

def pseudocount(motif_matrix):
    """Add one to every element of a motif matrix and generate a profile matrix."""
    nucleotides = "A G C T".split()
    col_matrix = listofiterables_to_columns(motif_matrix)
    freq_dict = {nuc : [] for nuc in nucleotides}
    for col in col_matrix:
        for nuc in nucleotides:
            freq_dict[nuc].append((col.count(nuc)+1))
    pseudo_dict = {}
    for key in freq_dict.keys():
        pseudo_dict[key] = []
        for idx, col in enumerate(freq_dict[key]):
            pseudo_dict[key].append(freq_dict[key][idx]/float(sum([freq_dict[k][idx] for k in freq_dict.keys()])))
    return pseudo_dict

def greedy_motif_search_pseudocount(dna, k, t):
    """Similar to greedy_motif_search, but add 1 to every element in profile matrices so that
    no probabilities are zero."""
    best_motifs = [line[0:k] for line in dna]
    motifs_list = [list(redundant_substrings(dna[i],k)) for i in range(len(dna))]
    initial_prof_dict = frequency_matrix(best_motifs)
    for idx, kmer in enumerate(motifs_list[0]):
        current_motifs = [kmer]
        current_profile = pseudocount(listofiterables_to_columns(kmer))
        for idx2 in range(1,len(dna)):
            current_motifs.append(profile_most_probable_kmer(current_profile, dna[idx2], k))
            current_profile = pseudocount(current_motifs)
        if score(current_motifs) < score(best_motifs):
            best_motifs = current_motifs
    return best_motifs

#print greedy_motif_search_pseudocount("""GGCGTTCAGGCA AAGAATCAGTCA CAAGGAGTTCGC CACGTCAATCAC CAATAATATTCG""".split(),3,5)

def random_select(dna, k):
    """Randomly choose kmers from collection of strings dna; one per string"""
    motifs = []
    for string in dna:
        start_pos = random.randint(0,len(string)-k)
        motifs.append(string[start_pos:start_pos+k])
    return motifs

def gen_motifs(profile, dna):
    """Take profile most probable kmer from each string within dna, given
    a probability matrix with k columns and 4 rows"""
    return [profile_most_probable_kmer(profile, item, len(profile.values()[0])) for idx, item in enumerate(dna)]

def randomized_motif_search(dna, k):
    current_motifs = random_select(dna, k)
    best_motifs = list(current_motifs)
    #print best_motifs
    while True:
        profile = pseudocount(current_motifs)
        current_motifs = gen_motifs(profile, dna)
        if score2(current_motifs) < score2(best_motifs):
            best_motifs = current_motifs
        else:
            return best_motifs, score2(best_motifs)

def repeat_randomized_motif_search(dna, k, num_trials):
    best_score = float("inf")
    best_motifs = []
    for dummy in range(num_trials):
        motifs, score = randomized_motif_search(dna, k)
        if score < best_score:
            best_score = score
            best_motifs = motifs
    return best_motifs, best_score

##print repeat_randomized_motif_search("""CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA
##     GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG
##     TAGTACCGAGACCGAAAGAAGTATACAGGCGT
##     TAGATCAAGTTTCAGGTGCACGTCGGTGAACC
##     AATCCACCAGCTCCACGTGCAATGTTGGCCTA""".split(), 8,1000)
##

def gibbs_random(probability_list):
    """For non-negative list of probabilities [p1,...,pn] probability_list,
    return integer i with probability pi, even in the case where sum(probability_list)!=1"""
    total = sum(w for w in probability_list)
    r = random.uniform(0, total)
    upto = 0
    for c, w in enumerate(probability_list):
      if upto + w > r:
         return c
      upto += w
    assert False, "Shouldn't get here"

def profile_randomly_generated_kmer(profile, motifs_list, k, i):
    strings = redundant_substrings(motifs_list[i], k)
    probabilities = [profile_probability(profile, string) for string in strings]
    return strings[gibbs_random(probabilities)]
    
def gibbs_sampler(dna, k, t, num_trials):

    current_motifs = random_select(dna, k)
    best_motifs = current_motifs

    for dummy in range(num_trials):
        i = random.randint(0,t-1)
        profile = pseudocount(current_motifs[0:i]+current_motifs[i+1::])
        current_motifs = current_motifs[0:i]+[profile_randomly_generated_kmer(profile, dna, k, i)]+current_motifs[i+1::]

        if score2(current_motifs) < score2(best_motifs):
            best_motifs = current_motifs
    return best_motifs

def gibbs_sampler_multirun(dna, k, t, num_trials, num_meta_trials):
    best_score = float("inf")
    best_motifs = []
    for dummy in range(num_meta_trials):
        new_motifs = gibbs_sampler(dna, k, t, num_trials)
        if score2(new_motifs) < best_score:
            best_score = score2(new_motifs)
            best_motifs = new_motifs
    return best_motifs
