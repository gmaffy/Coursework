Week 1: Where in the Genome Does DNA Replication Begin?

These 3 scripts provide tools to solve the problem of finding OriC in bacteria. OriC is the point at which the reverse strand
meets the forward strand, so we expect the region to minimize skew. However, minskew only provides an approximate solution
due to random noise. In order to find OriC within the ballpark of the region defined by minskew, we rely on the fact that
OriC tends to contain many repeats of the same 9-mer. However, this 9-mer can contain slight variations, so we need to allow for this.
frequentwords_fast contains this tool.
