My project was a genetic algorithm to design a control strategy for a virtual robot playing a treasure-collecting game. The robot is randomly placed on a 10x10 board bordered by a wall. On the board are placed treasures (randomly, with a random number drawn from a normal distribution centered on 50 treasures). The robot is only aware of his current position and the four positions above, below, left, and right of himself, and has no memory. In any given situation, the robot can choose one of seven actions: do nothing, attempt to pick up a treasure from the current space, move one space up, right, down, or left, or make a random move.

In order to decide what to do, the robot refers to its 'genome'. The genome is a list of numbers [0,6], 243 digits long. The 243 'loci' correspond to the 243 possible situations the robot can be in (3 possible items [wall, treasure, or blank space] ** 5 positions the robot can sense), and the number in each locus refers to one of the seven possible actions. To make a move, the robot reads its current situation, cross-references it with its genome, then selects the appropriate action.

The 'genetic' aspect of this genetic algorithm is that the robot is not told the rules of the game -- it only knows its final score at the end. The game begins by creating many robots, each with a random genome. The robot's fitness is determined as an average of its score on 20 rounds of the game, where each round consists of 200 actions on the board. Then, based on some procedure, half the robots are chosen to mate with one another. Their genomes are recombined at a random cut point, and the progeny are randomly mutated with low probability. This process continues for many generations.

Now, an explanation of the attached files:
-robbyRun.py is the lowest-level file. It includes classes for the game board and the robot itself
-geneticAlg.py is the mid-level. It contains classes for an individual (corresponding to a particular genome), a population, and methods for mutating individuals or mating them together
-pn_finalproject.py is the highest-level. The other files are imported as modules here. The user can run this file and set various parameters, including the size of each generation, the number of generations, whether to estimate genetic diversity of each generation, and the filename to write statistics to
-the two text files are sample text outputs from this program, each corresponding to runs of 1000 generations with 50 individuals/generation
-the images show the graphical output of this file, plotting maximum fitness in each generation over the generation number

I had originally planned to implement a GUI, but once I finished the core program, I got very interested in the problem of choosing breeding pairs for the next generation. I ended up creating three versions of this algorithm. The final version is simply called select_breeders(), which uses an approach suggested by Conrad. Briefly, the fitness of each individual in the population is determined, and then individuals are sorted into 'bins' based on fitness. All below-average individuals go into one bin. The above-average individuals are segregated into the remaining bins. Since fitness tends to be normally distributed, higher-fitness individuals tend to be less crowded bins. (In addition, individuals with fitness 3 standard deviations over the mean are automatically excluded to avoid bias in early generations) Each bin receives a fixed number of entries into a breeding lottery. Pairs are then randomly drawn from the whole lottery. This helps ensure that higher-fitness individuals breed more, but some low-fitness individuals are virtually guaranteed to breed.

This algorithm replaced an earlier approach in which individuals were simply entered into a lottery with a number of entries based on fitness (this was scrapped due to high bias), a second method called select_breeders2() in which only above-average individuals were allowed to mate (also showed poor performance), and another version called select_breeders3() in which two populations were created, one from the output of select_breeders(), and a second by random draw from the whole population. I hoped this would add more diversity, but it did not perform as well as the original select_breeders(), so was scrapped.

tl;dnr version:
Run the pn_finalproject.py file. Choose a generation size of 50-100, and a generation number of 500-1000. Enter 'y' when prompted if you want statistics on genetic diversity (strangely, the correlation between diversity and fitness was not as strongly inverse as I expected).

Finally, I wanted to see whether my genetic algorithm could outperform a robot coded by me. In positive_control.py, I implemented a somewhat naive strategy. In this order, the robot:
1. picks up a treasure on the current space
2. else, moves to a neighboring space if any contain treasure
3. else, if bordering a wall, moves away
4. else, makes a random move

When I ran this program (see attached screenshot), the robot got an average score of 274 over 200 trials, with a maximum score of 305. When I looked at the output of the genetic algorithm in the attached text file, I found one that had an average performance of 307. I.e., its average performance was higher than the maximum performance obtained by my human-coded algorithm! This was a very exciting result.
