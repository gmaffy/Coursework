CODON_TABLE = dict()
RNA_TABLE = {'A' : 'A', 'G' : 'G', 'C' : 'C', 'T' : 'U'}
DNA_TABLE = {'A' : 'A', 'G' : 'G', 'C' : 'C', 'U' : 'T'}

import bioin_patterncount as pc

def codon_load():
    global CODON_TABLE
    with open("Codon_table.txt") as f:
        data = f.read().split()
        for idx, item in enumerate(data):
            if not idx % 2:
                CODON_TABLE[item] = data[idx + 1]
    return CODON_TABLE

def translate(rna_string):
    iter_range = range(len(rna_string))
    peptide = ""
    if len(CODON_TABLE.keys()) == 0:
        codon_load()
    for idx in iter_range[::3]:
        try:
            if not CODON_TABLE[rna_string[idx:idx+3]] == "*":
                peptide += CODON_TABLE[rna_string[idx:idx+3]]
            else:
                return peptide
        except IndexError:
            return peptide
    return peptide

def transcribe(dna_string):
    return ''.join([RNA_TABLE[base] for base in dna_string])

def reverse_transcribe(rna_string):
    return ''.join([DNA_TABLE[base] for base in rna_string])

def peptide_check(rna, peptide):
    for idx, aa in enumerate(peptide):
        if aa == CODON_TABLE[rna[idx * 3 : (idx * 3)+3]]:
            if idx == len(peptide) - 1:
                return True
            else:
                pass
        else:
            return False
                
def peptide_encoding(dna_forward, peptide):
    if len(CODON_TABLE.keys()) == 0:
        codon_load()
    dna_list = []
    #transcribe both dna strings
    rna_forward = transcribe(dna_forward)
    #go through each and compare to peptide
    for idx in range(len(rna_forward)-(3*len(peptide))+1):
        strand = rna_forward[idx:idx + (3*len(peptide))]
        #print strand, translate(strand), peptide_check(strand, peptide)
        if peptide_check(strand, peptide):
            dna_list.append(reverse_transcribe(strand))
        else:
            pass
    return dna_list

def peptide_encoding_bidirection(dna_forward, peptide):
    return peptide_encoding(dna_forward, peptide)+[pc.reverse_complement(i) for i in peptide_encoding(pc.reverse_complement(dna_forward), peptide)]

with open("B_brevis.txt") as f:
    brevis = f.read().replace('\n', '')

tyrocidine_b1 = "VKLFPWFNQY"

x = peptide_encoding_bidirection(brevis, tyrocidine_b1)  
