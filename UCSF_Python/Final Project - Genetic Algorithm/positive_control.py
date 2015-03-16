import robbyRun
import random
import geneticAlg

possibilities = robbyRun.generatePossibilities()

impossible=list()
currTreasure=list()
wallNorth=list()
wallSouth=list()
wallEast=list()
wallWest=list()
treasureNorth=list()
treasureSouth=list()
treasureEast=list()
treasureWest=list()
other=list()

#categorize possible situations
for i in range(len(possibilities)):
        
        if possibilities[i][0]==1:
                currTreasure.append(i)
        elif possibilities[i][1]==1:
        		treasureNorth.append(i)
        elif possibilities[i][2]==1:
        		treasureEast.append(i)
        elif possibilities[i][3]==1:
        		treasureSouth.append(i)
        elif possibilities[i][4]==1:
        		treasureWest.append(i)
        elif possibilities[i][1]==2:
        		wallNorth.append(i)
        elif possibilities[i][2]==2:
        		wallEast.append(i)
        elif possibilities[i][3]==2:
        		wallSouth.append(i)
        elif possibilities[i][4]==2:
        		wallWest.append(i)
        else:
        		other.append(i)

strategy = list()

#1 = treasure, 0 = nothing, 2 = wall
#order: current, north, east, south, west
#actionDict = {0 : doNothing, 1 : moveNorth, 2 : moveEast, 3 : moveSouth, 4 : moveWest, 5 : moveRandom, 6 : pickUp}

#develop basic control strategy. In this order of priority:
#1. if current space has treasure, pick it up
#2. if neighboring space has treasure, go there
#3. if neighboring space has wall, avoid
#4. otherwise, move randomly

for index in range(len(possibilities)):
	if index in currTreasure:
		strategy.append(6)
	elif index in treasureNorth:
		strategy.append(1)
	elif index in treasureEast:
		strategy.append(2)
	elif index in treasureSouth:
		strategy.append(3)
	elif index in treasureWest:
		strategy.append(4)
	elif index in wallNorth:
		strategy.append(3)
	elif index in wallEast:
		strategy.append(4)
	elif index in wallSouth:
		strategy.append(1)
	elif index in wallWest:
		strategy.append(2)
	else:
		strategy.append(5)

print "Naive strategy:"
print strategy

fitnessList = list()

i=0
while i<200:
        pos_control = geneticAlg.Individual(strategy)
        pos_control.getFitness()
        fitnessList.append(pos_control.fitness)
        i+=1

print "Max fitness over 200 trials: "+str(max(fitnessList))
print "Mean fitness over 200 trials: "+str(sum(fitnessList)/len(fitnessList))



