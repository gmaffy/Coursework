"""Skew is the running tally of #G - #C on a string of DNA, starting from an
arbitrary position. Since forward strands spend more time single-stranded than
reverse strands (due to the fact that DNA polymerase can only traverse the reverse
strand), C is more infrequent on this strand due to its tendency to mutate to T
in single-stranded DNA. Since the origin of replication occurs at the point where
the reverse half-strand ends and the forward half-strand begins, the position
of minimum skew tends to be OriC."""

def find_minimum_skew(genome):
    """Input string representing genome; output integer positions minimizing skew"""
    #slide through genome and count skew
    skew_list = list()
    skew_codes = {'A' : 0, 'T' : 0, 'G' : 1, 'C' : -1}
    min_skew_position = set([])
    current_skew = 0
    for base in genome:
        skew_list.append(current_skew)
        current_skew += skew_codes[base]
    min_skew = min(skew_list)
    for index in range(len(skew_list)):
        if skew_list[index] == min_skew:
            min_skew_position = min_skew_position.union(set([index]))
    return (min_skew_position, min_skew)


            
#print find_minimum_skew("CATGGGCATCGGCCATACGCC")
