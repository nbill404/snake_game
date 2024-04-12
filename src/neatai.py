# https://www.youtube.com/playlist?list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2
# https://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf


import neat
import neat.config
import os
import neat.population
from functools import partial
from math import dist

from snakegame import SnakeGame

class NeatAI:

    def __init__(self) -> None:
        dir = os.path.dirname(__file__)
        file = os.path.join(dir, "neat.config")

        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         file)
        
        self.config = config

        self.population = neat.Population(config)
        self.population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.population.add_reporter(stats)

        self.games = [SnakeGame(18, 24) for _ in range(config.pop_size)]
        self.genomes = self.population.population.items()
        self.networks = []

        for _, genome in self.genomes:
            self.networks.append(neat.nn.FeedForwardNetwork.create(genome, self.config))

    def update(self):
        for game, network in zip(self.games, self.networks):
            if game.start:
                d = network.activate(convert_x(game))
                game.dir = SnakeGame.directions[get_dir(d)]
                game.update()

            # Terminate game if it runs too long without an apple
                if game.distance - game.last_apple >= 500:
                    game.start = False

        if self.ended():
            f = partial(eval_genomes, self.games)
            self.population.run(f, 1) # Reproduce 1 generation

            for game in self.games:
                game.reset()

            # Create new game when population changes
            diff = len(self.population.population.items()) - len(self.genomes)
            
            if abs(diff) > 0:
                for i in range(abs(diff)):
                    if diff > 0:
                        self.games.append(SnakeGame(18, 24))
                    elif diff < 0:
                        self.games.pop()
                
                self.genomes = self.population.population.items()

                self.networks = []
                for _, genome in self.genomes:
                    self.networks.append(neat.nn.FeedForwardNetwork.create(genome, self.config))

    def ended(self):
        for game in self.games:
            if game.start:
                return False

        return True
    
def get_dir(input):
    return input.index(min(input)) # Get index of min value

def eval_genomes(games, genomes, config):
    for game, (_, genome) in zip(games, genomes):
        genome.fitness = game.score
        # genome.fitness += min((game.distance - game.last_apple) / 100, 0.5)
        # genome.fitness -= int(game.hit_self) * 5

def convert_x(game: SnakeGame):
        # Inputs:
        # x, y position of apple
        # 4 surrounding blocks 
        # distance from apple

        x = [0 for _ in range(9)]
        
        # Head
        head = game.snake[0]

        # position relative to apple
        x[0] = game.apple[0] - head[0]
        x[1] = game.apple[1] - head[1]

        offset = 2

        directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

        for idx, d in enumerate(directions):
            i = head[0] + d[0]
            j = head[1] + d[1]

            if game.is_inbounds((i, j)):
                if game.apple[0] == i and game.apple[1] == j:
                    x[offset + idx] = 2
                else:
                    x[offset + idx] = game.matrix[i][j]
            else:
                x[offset + idx] = -1

        offset += 4

        x[offset] = dist(game.apple, head)

        return x


        


if __name__ == "__main__":
    ai = NeatAI()

    games = [SnakeGame(18, 24) for _ in range(100)]
    ai.update()

