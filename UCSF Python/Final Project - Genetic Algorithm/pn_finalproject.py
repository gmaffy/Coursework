#program requires matplotlib.pyplot and numpy
import geneticAlg as gA
import matplotlib.pyplot as plt
import robbyRun
import random

#store loci representing impossible situations, for user's info
#see robbyRun.py for more information
possibilities = robbyRun.generatePossibilities()
impossible=list()
currTreasure=list()
for i in range(len(possibilities)):
        if possibilities[i][0]==2 or (possibilities[i][1]==possibilities[i][3]==2) or (possibilities[i][2]==possibilities[i][4]):
                impossible.append(i)
        elif possibilities[i][0]==1:
                currTreasure.append(i)


#take user inputs

genSize = input('Generation size: ')
genSize = int(genSize)
#need at least four for diversity estimates
if genSize < 4:
        genSize = 4
#ensure that generation size is even, since each mating produces two children
if genSize%2==1:
        genSize+=1

numGen = input ('Number of generations : ')
numGen = int(numGen)

#ensure that there are at least two generations
if numGen < 2:
        numGen = 2

keyGen = input('Return statistics from every nth generation: ')
keyGen = int(keyGen)

f_name = input('Name of file to store your statistics (string; do not include .txt ending): ')
f_name+='.txt'

diver = input('Would you like to estimate genetic diversity of the population? (y/n) (may slow down algorithm considerably)')
if diver=='y':
        diver=True
else:
        diver=False

f = open(f_name, 'w')

#create first generation
def createFirstGeneration(size = 100):
        
        g0 = gA.Population()
        
        while size > 0:
                
                i = gA.createRandomIndividual()
                i.getFitness()
                g0.add_individual(i)
                
                size -= 1
        
        return g0

#mate winners of generation and create next generation
def mateWinners(population, num = 50):
        
        #choose breeders
        population.fitnessHistogram()
        breeders = population.select_breeders(num)
        
        #mate pairs
        nextgen = list()
        
        for index in range(0,len(breeders)-1,2):
                children = breeders[index].mate(breeders[index+1])
                #mate function returns a tuple of individuals; append each individual to the next generation
                nextgen.append(children[0])
                nextgen.append(children[1])
        
        #turn the list of children into a population holding the new generation
        pop = gA.Population()
        for i in nextgen:
                pop.add_individual(i)
        return pop
        

def mateWinners2(population, num=50):
        #special function designed to work with select_breeders3, which returns two separate lists of breeders
        #see geneticAlg.py for code
        
        population.fitnessHistogram()
        breeder_tuple = population.select_breeders3(num)
        
        nextgen = list()
        
        for index in range(len(breeder_tuple[0])):
                children = breeder_tuple[0][index].mate(breeder_tuple[1][index])
                nextgen.append(children[0])
                nextgen.append(children[1])
        pop = gA.Population()
        for i in nextgen:
                pop.add_individual(i)
        return pop


#write relevant data to file
def writeData(population, genNumber, nthGen = 5):
        samplesize = int(len(population.individuals)/5)
        global diver
        if genNumber % nthGen == 0:
                
                #estimate population-wide genetic diversity by randomly selecting pairs and asking how many loci they have in common, if user asked to do this
                if diver:
                
                        #ensure there is at least one pair to compare
                        if samplesize<2:
                                samplesize = 2
                                
                        sample=list()        
                        while len(sample)<samplesize:
                                sample.append(random.choice(population.individuals))
                        
                        
                        diversity = list()
                        
                        for i in range(0,len(sample)-1,2):
                                
                                match = list()
                                
                                for l in range(len(sample[i].genome)):
                                        
                                        match.append(sample[i].genome[l] == sample[i+1].genome[l])
                                
                                diversity.append(sum(match))
                        
                
                
                f.write('Generation '+ str(genNumber))
                f.write('\n')
                population.fitnessHistogram()
                population.get_mean_fitness()
                population.get_stdev_fitness()
                f.write('Max fitness: '+ str(population.get_max_fitness()))
                f.write('\n')
                f.write('Genome of Most Fit Individual:')
                
                fittest = population.fitnessDict[max(population.fitnessDict.keys())][0].genome
                
                f.write(str(fittest))
                f.write('\n')
                f.write('Min fitness: '+ str(population.get_min_fitness()))
                f.write('\n')
                f.write('Mean fitness: ' + str(population.meanFit))
                f.write('\n')
                f.write('Stdev of fitness: '+ str(population.stdevFit))
                f.write('\n')
                if diver:
                        f.write('Mean diversity: '+str(sum(diversity)/float(len(diversity))))
                f.write('\n')
                f.write('=========================================')
                f.write('\n')
                f.write('\n')
                
maxfitness = list()
        
def duplicate_histogram(population, currGen):
        #function to calculate per-locus genetic diversity. Use most fit individual as reference and ask how many others have identical gene at each locus
        #this involves many comparisons so should be used sparingly, e.g. only on first and last generations
        
        
        population.fitnessHistogram()
        maximum = population.get_max_fitness()
        
        #choose highest fitness individual
        
        referenceIndividual = population.fitnessDict[maximum][0]
        
        
        duplicates_per_locus = dict()
        
        for locusIndex in range(len(referenceIndividual.genome)):
                
                numDuplicate = 0
                for indiv in population.individuals:
                        if indiv.genome[locusIndex]==referenceIndividual.genome[locusIndex]:
                                numDuplicate += 1
                
                if numDuplicate in duplicates_per_locus.keys():
                        duplicates_per_locus[numDuplicate].append(locusIndex)
                else:
                        duplicates_per_locus[numDuplicate]=[locusIndex]
        
        return duplicates_per_locus
                                                        
                                                
                        
                        
                

#mutate children
def mutGeneration(population):
        for indiv in population.individuals:
                indiv.mutate()



#start program. create first generation
gen = createFirstGeneration(genSize)


#create subsequent generations, up to the limit imposed by the user
i=1
while i<numGen:
        print 'Current generation: '+ str(i)
        writeData(gen, i, keyGen)
        gen.fitnessHistogram()
        gen.get_mean_fitness()
        gen.get_stdev_fitness()
        maxfitness.append(gen.get_max_fitness())
        gen = mateWinners(gen, genSize)
        mutGeneration(gen)
        i+=1 #end of generation

#calculate per-locus diversity of final generation. Write most and least diverse loci to file
hist = duplicate_histogram(gen, i)
least_diverse = max(hist.keys())
most_diverse = min(hist.keys())
f.write('Most selected loci: '+str(hist[least_diverse]))
f.write('\n')
f.write('Most diverse loci: '+str(hist[most_diverse]))
f.write('\n')
f.write('\n')
f.write('Impossible loci: '+str(impossible))
f.write('\n')
f.write('Loci involving a treasure on the current space: '+str(currTreasure))

f.close()

#plot max fitness of each generation
plt.plot(range(len(maxfitness)),maxfitness)
plt.xlabel('Generation')
plt.ylabel('Max Fitness')
plt.show()

