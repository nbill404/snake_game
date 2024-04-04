import os
import numpy as np

from neuralnetwork import Dense, Tanh
from snakegame import SnakeGame
from pathfind import get_ai_move


class NeuralAi:
    def __init__(self, X, Y) -> None:
        """
        Inputs:
        - 18 * 24 = 432: Position of apple 
        - 18 * 24 = 432: Position of snake body on grid
        - 4 : Each direction
        Total = 868


        Outputs:
        - 4: Up, down, left, right

        Error function will give results based on A* algorithm
        """
        
        self.X = X
        self.Y = Y
        self.output = (-1, 0)
        
        self.network = [
            Dense(868, 128),
            Tanh(),
            Dense(128, 128),
            Tanh(),
            Dense(128, 4),
            Tanh()
        ]

        self.epochs = 10000
        self.learning_rate = 0.1
        self.error = 0

    def predict(self, x, y):
        self.X = x
        self.Y = y

        for x, y in zip(self.X, self.Y):
            output = x
            
            # Forward for each layer
            for layer in self.network:
                output = layer.forward(output)

            # Calculate error using mean square error function
            error = self.mse(y, output)
            grad = self.mse_prime(y, output)
            
            # Backpropagation
            for layer in reversed(self.network):
                grad = layer.backward(grad, self.learning_rate)

        self.error = error
        self.update_output(output)

    def train(self):
        for e in range(self.epochs):
            for x, y in zip(self.X, self.Y):
                output = x
                
                # Forward for each layer
                for layer in self.network:
                    output = layer.forward(output)

                # Calculate error using mean square error function
                error = self.mse(y, output)
                grad = self.mse_prime(y, output)
                
                # Backpropagation
                for layer in reversed(self.network):
                    grad = layer.backward(grad, self.learning_rate)


            # print('%d/%d, error %f' % (e * 1, self.epochs, error))

        self.error = error
        
    def update_output(self, output):
        m = -100

        for i in range(len(output)):
            if output[i] > m:
                m = output[i][0]
                self.output = SnakeGame.directions[i]


    def mse(self, y_true, y_pred):
        return np.mean(np.power(y_true - y_pred,2))
    
    def mse_prime(self,  y_true, y_pred):
        return 2 * (y_pred - y_true) / np.size(y_true)
    
    def save(self):
        if not os.path.exists('network'):
            os.makedirs('network')

        for i, layer in enumerate(self.network):
            if i % 2 == 0:
                np.save('network/weights{}.npy'.format(i), layer.weights)
                np.save('network/bias{}.npy'.format(i), layer.bias)

    def load(self):
        for i, layer in enumerate(self.network):
            if i % 2 == 0:
                layer.weights = np.load('network/weights{}.npy'.format(i))
                layer.bias = np.load('network/bias{}.npy'.format(i))

    
def convert_x(game: SnakeGame):
        pos = game.apple

        x = np.zeros(868)
        x[pos[0] * game.rows + pos[1]] = 1

        for pos in game.snake:
            x[pos[0] * game.rows + pos[1] + 432] = 1

        x[862 + convert_dir(game.dir)]
        x = np.reshape(x, (1, 868, 1))

        return x

def convert_y(dir):
    output = np.zeros(4)
    output[convert_dir(dir)] = 1
    return np.reshape(output, (1, 4, 1))

def convert_dir(dir):
        i = 0

        match dir:
            case (-1, 0):
                i = 0
            case (1, 0):
                i = 1
            case (0, -1):
                i = 2
            case (0, 1):
                i = 3

        return i


if __name__ == "__main__":
    game = SnakeGame(18, 24)
    neuralAi = NeuralAi(convert_x(game), convert_y(game.dir))
    neuralAi.train()
    # neuralAi.predict(convert_x(game), convert_y(game.dir))
    # neuralAi.save()
    neuralAi.load()
