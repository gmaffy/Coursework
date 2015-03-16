import random
import itertools

#The Robby's World game determines the fitness of each individual
#Robby's world: 10x10 grid, ~50 treasures, randomly placed

#this class ended up being unused, but I left it in just in case
class Coord(object):
        def __init__(self, x, y):
                self.x = x
                self.y = y
        
        def __str__(self):
                return str(self.x) + ' , ' + str(self.y)
        
        def getX(self):
                return self.x
        
        def getY(self):
                return self.y

#class to represent the world in which Robby operates
class gameBoard(object):
        
        def __init__(self):
                self.treasureCoords = list()
        
        def placeTreasures (self, mean=50, stdev = 5):
                
                numTreasures = int(random.normalvariate(mean, stdev))
                
                treasureCoords = list()
                allCoords = list()
                
                #generate list of all possible coords
                for i in range(9):
                        for n in range(9):
                                allCoords.append(list([i,n]))
                
                treasureCoords = random.sample(allCoords, numTreasures)
                
                self.treasureCoords = treasureCoords
                

def generatePossibilities(possibilities=[0,1,2],r = 5):
		#Robby can face any of 243 situations, represented by the 243 loci in its genome.
		#We now create a list representation of these situations
		#Robby can sense five positions: his current location and those to the North, South, East, and West
		#In each of these positions he could sense a blank space, treasure, or wall
		#Represent these as 0, 1, or 2, respectively
		
		#N.B. some of these situations are impossible, e.g. to be surrounded entirely by walls, or for there to be a wall on the current space
		#We would predict that loci underlying these situations would not undergo selection pressure
		
        situations = itertools.product(possibilities, repeat=r)
        
        sit = list()
        
        for i in situations:
                sit.append(i)
        return sit #list of tuples

possibilities = generatePossibilities()

#Robby's potential actions are defined as methods of the Robby class
class Robby(object):
        
        WALL_PENALTY = -10
        PICK_PENALTY = -5
        REWARD = 10
        
        
        
        def __init__(self, genome, board):
                self.strategy = genome
                self.score = 0
                self.board = board
                
        def place(self):
                self.location = list([random.randint(0,9),random.randint(0,9)]) #initialize in a random location

        def moveNorth(self):
                if self.location[1]==0:
                        self.score+=self.WALL_PENALTY
                else:
                        self.location[1] -= 1
        
        def moveEast(self):
                if self.location[0]==9:
                        self.score+=self.WALL_PENALTY
                else:
                        self.location[0] += 1
        
        def moveSouth(self):
                if self.location[1]==9:
                        self.score+=self.WALL_PENALTY
                else:
                        self.location[1]+=1
        
        def moveWest(self):
                if self.location[0]==0:
                        self.score+=self.WALL_PENALTY
                else:
                        self.location[0] -= 1
        
        def moveRandom(self):
                
                choice= random.choice([self.moveNorth, self.moveSouth, self.moveEast, self.moveWest])
                choice()
        
        def doNothing(self):
                pass
        
        def pickUp(self):
                if self.location in self.board.treasureCoords:
                        self.board.treasureCoords.remove(self.location)
                        self.score += self.REWARD
                else:
                        self.score += self.PICK_PENALTY
        
        #dictionary to allow functions to be easily called
        #the numbers here correspond to the numbers in Robby's genome, stored in class Individual
        actionDict = {0 : doNothing, 1 : moveNorth, 2 : moveEast, 3 : moveSouth, 4 : moveWest, 5 : moveRandom, 6 : pickUp}
        

        #function to determine Robby's current situation so it can be looked up in the list called possibilities
        def getSituation(self):
                #1 = treasure, 0 = nothing, 2 = wall
                #Current location
                if self.location in self.board.treasureCoords:
                        Current = 1
                else: Current = 0
                
                #North
                if self.location[1]-1 in self.board.treasureCoords:
                        North = 1
                elif self.location[1] == 0:
                        North = 2
                else:
                        North = 0
                
                #East
                if self.location[0]+1 in self.board.treasureCoords:
                        East = 1
                elif self.location[0] == 9:
                        East = 2
                else:
                        East = 0
                
                #South
                if self.location[1]+1 in self.board.treasureCoords:
                        South = 1
                elif self.location[1]==9:
                        South = 2
                else:
                        South = 0
                
                #West
                if self.location[0]-1 in self.board.treasureCoords:
                        West = 1
                elif self.location[0]==0:
                        West = 2
                else:
                        West = 0
                
                situation = tuple([Current, North, East, South, West])
                self.situation = situation
         
        #function to take action. Looks at the current situation, matches it to the list of possible situations, then calls the function specified by the genome at that particular locus        
        def act(self):
                self.getSituation()
                sit = possibilities.index(self.situation)
                action = self.strategy[sit]
                
                self.actionDict[action](self)
        
        #tie everything together into one function. Allows Robby to take 200 total actions, places him on the board, then repeatedly calls act()        
        def play(self):
                NUM_ACTIONS = 200
                self.place()
                
                while NUM_ACTIONS>0:
                        
                        self.act()
                        NUM_ACTIONS-=1
                        
                        
                
        
