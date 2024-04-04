from random import randint, random
from copy import deepcopy
from math import dist
from snakegame import SnakePredetermined, SnakeGame

class GeneticSnakeSolver:
    encodings = ["00", "01", "10", "11"]


    def __init__(self, num, sequence_length) -> None:
        self.num = num
        self.sequence_length = sequence_length
        self.pop = [0 for _ in range(num)]
        self.fit = [0 for _ in range(num)]
        self.gen = 0
        self.mutation_rate = 0.1
        
        for i in range(num):
            current = ""
            for __ in range(sequence_length):
                current += (GeneticSnakeSolver.encodings[randint(0,3)])

            self.pop[i] = current

    def next_generation(self, longest, snakes, apples, distances, scores):
        self.fitness(snakes, apples, distances, scores)
        self.select()
        self.crossover(longest)
        self.mutate(longest)
        self.gen += 1

        return self.pop


    def fitness(self, snakes, apples, distances, scores):
        # Fitness function uses distance to apple, number of apples collected, distance travelled
        for i in range(self.num):
            score = 0
            # score += max(-3 * (distances[i] ** 2) + 20, 0) # Rewards going further (-3x^2 + 5)
            # score += (scores[i] * 10) / distances[i] # Reward getting to apples quickly
            score += scores[i] * 15 # Reward apples
            score += 15 / abs(dist(apples[i], snakes[i])) # Reward being near apple

            self.fit[i] = score

    def select(self):
        self.pop = [x for _, x in sorted(zip(self.fit, self.pop))] # Sorts based on fitness score
        self.pop.reverse()

    def crossover(self, longest):
        split = randint(0, int(longest - 1 / 2)) * 2 # Crossover point
        copy = deepcopy(self.pop)
        half = int(self.num / 2)

        for i in range(half):
            j = i
            k = half - i

            parent1 = copy[j]
            parent2 = copy[k]
            child = ""

            # single point crossover
            #child = parent1[:split] + parent2[split + 1:]


            # Uniform crossover
            for n in range(self.sequence_length):
                if random() < 0.5:
                    child += parent1[n: n+2]
                else:
                    child += parent2[n: n+2]
            
            self.pop[i] = child 
            self.pop[i + half] = copy[i]
            

    def mutate(self, longest):
        for genome in self.pop:
            if (random() < self.mutation_rate):
                i = randint(0, longest)
                # i = longest - 1

                if genome[i] == '1':
                    genome = genome[0:i] + '0' + genome[i+1:]
                else: 
                    genome = genome[0:i] + '1' + genome[i+1:]

class GeneticAI:

    def __init__(self, rows, cols, pop_size = 10, sequence_length = 1000):
        self.rows = rows
        self.cols = cols
        self.pop_size = pop_size
        self.sequence_length = sequence_length

        self.genetic_ai = GeneticSnakeSolver(self.pop_size, self.sequence_length) 
        self.games = [SnakePredetermined(self.rows, self.cols) for _ in range(self.pop_size)]

        self.reset_games()

    
    def reset_games(self):
        self.step = 0
        self.distances = [0 for _ in range(self.pop_size)]
        self.scores = [0 for _ in range(self.pop_size)]

        for game in self.games:
            game.reset()
            game.start = True


    def update(self):
        over = True

        print("Step:", self.step)

        for i in range(self.pop_size):          
            if self.games[i].start:
                over = False

                d = int(self.genetic_ai.pop[i][self.step * 2: self.step * 2 + 2], 2)

                self.games[i].dir = SnakeGame.directions[d]
                self.games[i].update()

                self.distances[i] += 1
                self.scores[i] = self.games[i].score

        self.step += 1

        # All games have terminated
        if over:
            snakes = []
            apples = []
            for i in range(len(self.games)):
                snakes.append(self.games[i].snake[0])
                apples.append(self.games[i].apple)

            self.genetic_ai.next_generation(self.step, snakes, apples, self.distances, self.scores)
            self.reset_games()

            print("All games terminated")
            print("Starting generation: " + str(self.genetic_ai.gen))
