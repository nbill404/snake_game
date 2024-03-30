from random import randint, random
from copy import deepcopy
from math import dist

class GeneticSnakeSolver:
    encodings = ["00", "01", "10", "11"]


    def __init__(self, num, sequence_length) -> None:
        self.num = num
        self.pop = [0 for _ in range(num)]
        self.fit = [0 for _ in range(num)]
        self.gen = 0
        self.mutatation_rate = 0.2
        
        for i in range(num):
            current = ""
            for __ in range(sequence_length):
                current += (GeneticSnakeSolver.encodings[randint(0,3)])

            self.pop[i] = current

    def next_generation(self, longest, snakes, apples, distances, scores):
        self.fitness(snakes, apples, distances, scores)
        self.select()
        self.crossover(longest)
        self.mutate()
        self.gen += 1

        return self.pop


    def fitness(self, snakes, apples, distances, scores):
        # Fitness function uses distance to apple, number of apples collected, distance travelled
        for i in range(self.num):
            score = 0
            score += distances[i]
            score += scores[i] * 15
            score += 10 / abs(dist(apples[i], snakes[i]))

            self.fit[i] = 0

    def select(self):
        self.pop = [x for _, x in sorted(zip(self.fit, self.pop))] # Sorts based on fitness score

    def crossover(self, longest):
        split = randint(0, int(longest - 1 / 2)) * 2 # Crossover point
        copy = deepcopy(self.pop)

        for i in range(self.num):
            if i <= split: # Parent 1 - first half, Parent 2 - second half
                j = i
                k = split - i
            else: # Parent 2 - first half, Parent 1 - second half
                j = i - split
                k = (2 * split) - i
            
            self.pop[i] = copy[j][:split] + copy[k][split:] 
            

    def mutate(self):
        for genome in self.pop:
            if (random() < self.mutatation_rate):
                i = randint(0, len(genome) - 1)

                if genome[i] == '1':
                    genome = genome[0:i] + '0' + genome[i+1:]
                else: 
                    genome = genome[0:i] + '1' + genome[i+1:]
