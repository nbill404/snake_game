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
            d = network.activate(convert_x(game))
            game.dir = SnakeGame.directions[get_dir(d)]
            game.update()

            # Terminate game if it runs too long without an apple
            if game.distance - game.last_apple > 500:
                game.start = False

        if self.ended():
            f = partial(eval_genomes, self.games)
            self.population.run(f, 1) # Reproduce 1 generation

            for game in self.games:
                game.reset()

    def ended(self):
        for game in self.games:
            if game.start:
                return False

        return True
    
def get_dir(input):
    return input.index(min(input)) # Get index of min value

def eval_genomes(games, genomes, config):
    for game, (_, genome) in zip(games, genomes):
        # genome.fitness = game.score * 100
        genome.fitness = 0
        genome.fitness += game.distance
        
        # if game.score > 0:
        #     genome.fitness += game.distance / game.score
        # else:
        #     genome.fitness += 2 / abs(dist(game.apple, game.snake[0]))

def convert_x(game: SnakeGame):
        x = [0 for _ in range(9)]

        # Head
        head = game.snake[0]
        offset = 0

        directions = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for i, d in enumerate(directions):
            if game.is_inbounds((head[0] + d[0], head[1] + d[1])):
                x[offset + i] = game.matrix[head[0] + d[0]][head[1] + d[1]]
            else:
                x[offset + i] = -1

        offset += 8

        x[offset] = dist(game.apple, head)

        return x


        


if __name__ == "__main__":
    ai = NeatAI()

    games = [SnakeGame(18, 24) for _ in range(100)]
    ai.update()

