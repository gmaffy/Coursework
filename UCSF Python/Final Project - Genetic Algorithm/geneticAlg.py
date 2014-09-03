import random
import robbyRun
import numpy

def repeat_append(lst, item, n):        
        #helper function used for lottery when choosing breeding pairs
        i = 0
        
        while i < n:
                lst.append(item)
                i+=1
        
        return lst
        

class Individual(object):
        
        '''Represent a single individual in the population, with a genome representing a strategy'''
        
        def __init__(self, genome):
                self.genome = genome
                self.fitness = None
        
        def getFitness(self):
        #fitness is considered the average performance on 20 games of Robby's Run (see robbyRun.py)
        #Maximum fitness will be 500 on average (since a mean of 50 treasures are placed and each is worth 10 points)
        #Minimum fitness is exactly -2000, since Robby is allowed 200 actions per game and each wall collision is worth -10 points        

                NUM_RUNS = 20
                
                fitnessList = list()
                
                
                while NUM_RUNS>0:
                        
                        board = robbyRun.gameBoard()
                        board.placeTreasures()
                        robot = robbyRun.Robby(self.genome, board)
                        robot.play()
                        
                        fitnessList.append(robot.score)
                        NUM_RUNS -= 1

                fitness = int(sum(fitnessList)/len(fitnessList))
                self.fitness = fitness
                        
                
        def mate(self, other):
        #recombine genome with another at a random cutoff to create two new individuals
                
                STDEV = 50
                
                cutOff = 0
                while cutOff == 0 or cutOff > len(self.genome):
                        cutOff = int(random.normalvariate(len(self.genome),STDEV))

                gen1 = self.genome[0:cutOff]
                gen1.extend(other.genome[cutOff::])
                
                gen2 = other.genome[0:cutOff]
                gen2.extend(self.genome[cutOff::])
                
                
                return (Individual(gen1),Individual(gen2))

        def mutate(self, mutationRate = 0.03, numActions = 7):
                for i, s in enumerate(self.genome):
                        if random.random()>1-mutationRate:
                                self.genome[i] = random.randint(0,numActions-1)
                        else:
                                self.genome[i] = s
                                
def createRandomIndividual(genomeLength = 243, numActions = 7):
        
        
        gen = list()
        
        while len(gen)<genomeLength:
                gen.append(random.randint(0,numActions-1))
        
        return Individual(gen)

class Population(object):
        
        '''Represents a group of individuals'''
        
        def __init__(self):
                self.individuals = list()
        
        def add_individual(self, indiv):
                self.individuals.append(indiv)
        
        def fitnessHistogram(self):
                fitnessDict = dict()
                
                for indiv in self.individuals:
                        
                        if indiv.fitness == None:
                                indiv.getFitness()

                        if indiv.fitness in fitnessDict.keys():
                                fitnessDict[indiv.fitness].append(indiv)
                        else:
                                fitnessDict[indiv.fitness]=[indiv]
                
                self.fitnessDict = fitnessDict
        
        def get_mean_fitness(self):
                cumFit = 0
                leng = 0
                self.fitnessList = list()
                for k in self.fitnessDict.keys():
                        repeat_append(self.fitnessList, k, len(self.fitnessDict[k]))
                        cumFit += k*len(self.fitnessDict[k])
                        leng += len(self.fitnessDict[k])
                meanFit = float(cumFit)/leng
                self.meanFit = meanFit
                return meanFit
                
        def get_stdev_fitness(self):
                self.stdevFit = numpy.std(self.fitnessList)
                
        
        def get_min_fitness(self):
                
                return min(self.fitnessDict.keys())
        
        def get_max_fitness(self):
                return max(self.fitnessDict.keys())
        
        def select_breeders(self, num_breeders, num_bins = 10, votes_per_bin = 50):
        #method to select breeding pairs. Uses the fitness histogram to put individuals in bins, based on their fitness
        #each bin is given an equivalent number of entries into the breeding lottery
        #one bin is devoted to all individuals with below-average fitness, so these still have some chance of mating
        #remaining bins are given to all above-average individuals
                #create desired number of bins
                bins = list()
                
                while len(bins)<num_bins:
                        bins.append(list())
                
                #assign individuals to bins, based on fitness
                #exclude those with fitness > mean fitness + 3* standard deviation in order to limit bias in early generations
                #each bin receives given number of 'votes' in mating lottery
                #all individuals below mean go into one bin
                
                #determine cutoff points for upper bins
                maxAllowedFit = self.meanFit + 3*self.stdevFit
                
                fitRange = maxAllowedFit - self.meanFit
                
                cutoffs = list()
                
                binsize = float(fitRange)/(num_bins - 1)
                
                index = 1
                while len(cutoffs)<num_bins - 1:
                        cutoffs.append(self.meanFit + (binsize*index))
                        index+=1
                
                
                for fit in self.fitnessDict.keys():
                        
                        #fill bottom bin w/ below-average individuals
                        if fit < self.meanFit:
                                
                                for indiv in self.fitnessDict[fit]:
                                        bins[0].append(indiv)
                        
                        #fill next bins based on cutoffs
                        #should use a generator for this but I am lazy
                        else:
                                if fit<maxAllowedFit:
                                        for cutIndex in range(1,len(cutoffs)):
                                                if fit < cutoffs[cutIndex-1]:
                                                        for indiv in self.fitnessDict[fit]:
                                                                bins[cutIndex].append(indiv)
                                
                                                else:
                                                        for indiv in self.fitnessDict[fit]:
                                                                bins[-1].append(indiv)
                
                breeders = list()
                
                for i in bins:
                        
                        if len(i) > 0:
                                
                                index = 0
                                while index < votes_per_bin:
                                        breeders.append(random.choice(i))
                                        index+=1
                                
                        
                
                if len(breeders)>num_breeders:
                        
                        limited_breeders = list()

                        #ensure that highest fitness individual gets in at least once
                        fittest = self.get_max_fitness()
                        limited_breeders.append(self.fitnessDict[fittest][0])
                        
                                                
                        while len(limited_breeders)<num_breeders:
                                limited_breeders.append(random.choice(breeders))
                        return limited_breeders
                        
                return breeders         
          
          
        def select_breeders2(self, num_breeders):
          	#alternative algorithm. Cut off everything below 1 SD above mean and choose randomly from remaining
          	#not used since it tends to create bias
          	breeders = list()
                self.get_stdev_fitness()
                self.get_mean_fitness()
          	
          	candidates = list()
          	
          	for fit in self.fitnessDict.keys():
                        
                        
                        if fit > self.meanFit + self.stdevFit > 0:
                                
                                for indiv in self.fitnessDict[fit]:
                                        candidates.append(indiv)
                        

                while len(candidates)<num_breeders/2:
                        candidates.append(random.choice(self.fitnessDict.values())[0])
                                                
                
                while len(breeders)<num_breeders:
                        breeders.append(random.choice(candidates))
            
                return breeders
                        
        def select_breeders3(self,num_breeders):
                #second alternative algorithm developed in response to the observation that using the select_breeders() method, fitness tends to increase to around 300 by generation 400, then drop.
                #I speculated that this may be due to a loss of diversity
                #This algorithm seeks to preserve diversity by using the binning approach used in select_breeders(), but only to choose *one* of the two parents
                #The second parent in each couple is chosen randomly from the whole population, allowing lower-fitness individuals to contribute to the next generation, in the hopes that they may carry some genes that could become favorable if put into a different genomic context
                
                selected_breeders = self.select_breeders(num_breeders//2)
                candidates = list()
                
                random_breeders = list()
                for fit in self.fitnessDict.keys():
                                for indiv in self.fitnessDict[fit]:
                                        candidates.append(indiv)
                while len(random_breeders)<len(selected_breeders):
                        random_breeders.append(random.choice(candidates))
                
                return (random_breeders, selected_breeders)
                

                  	                    
                
#test code
test = False                
if test:                
	ind1 = createRandomIndividual()
	ind2 = createRandomIndividual()
	ind3 = createRandomIndividual()
	ind1.fitness = 1
	ind2.fitness = 2
	ind3.fitness = 2
	pop = Population()
	pop.add_individual(ind1)
	pop.add_individual(ind2)
	pop.add_individual(ind3)
	pop.fitnessHistogram()
	pop.get_min_fitness()
	pop.get_max_fitness()
	pop.get_mean_fitness()
	pop.get_stdev_fitness()
	print pop.stdevFit
