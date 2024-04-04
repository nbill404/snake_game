# https://www.youtube.com/watch?v=pauPCy_s0Ok

import numpy as np

class NeuralNetwork:
    def __init__(self, X, Y) -> None:
        self.X = X
        self.Y = Y
        
        self.network = [
            Dense(2, 3),
            Tanh(),
            Dense(3, 2),
            Tanh()
        ]

        self.epochs = 10
        self.learning_rate = 0.1

    def run(self):
        for e in range(self.epochs):
            error = 0
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
        
            error /= len(self.X)
            print('%d/%d, error %f' % (e * 1, self.epochs, error))

    def mse(self, y_true, y_pred):
        print(y_true, y_pred)

        return np.mean(np.power(y_true - y_pred,2))
    
    def mse_prime(self,  y_true, y_pred):
        return 2 * (y_pred - y_true) / np.size(y_true)

class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    def forward(self, input):
        return input

    def backward(self, output_gradient, learning_rate):
        pass

class Dense(Layer):
    def __init__(self, input_size, output_size):
        self.weights = np.random.randn(output_size, input_size) # j * i matrix
        self.bias = np.random.randn(output_size, 1) # j * 1 matrix

    def forward(self, input):
        assert input.shape[0] == self.weights.shape[1] , "Size of matrices do not match"
        self.input = input

        return np.dot(self.weights, input) + self.bias # y = w*x + b
    
    def backward(self, output_gradient, learning_rate):
        output = np.dot(np.transpose(self.weights), output_gradient) # Calculate before updating weights

        self.weights = self.weights - learning_rate * np.dot(output_gradient, np.transpose(self.input)) # w - a(dE/dY)x^T
        self.bias = self.bias - learning_rate * output_gradient # b - a(dE/dY)

        return output # W^T(dE/dY)

class Activation(Layer):
    def __init__(self, activation, activation_prime):
        self.activation = activation
        self.activation_prime = activation_prime

    def forward(self, input):
        self.input = input
        return self.activation(self.input)
    
    def backward(self, output_gradient, learning_rate):
        return np.multiply(output_gradient, self.activation_prime(self.input))
    
class Tanh(Activation): # Hyperbolic tangent function
    def __init__(self):
        tanh = lambda x : np.tanh(x)
        tanh_prime = lambda x: 1 - np.tanh(x) ** 2
        super().__init__(tanh, tanh_prime)

if __name__ == "__main__":
    X = np.reshape([[0,0], [0,1], [1, 0], [1, 1]], (4,2,1)) # Inputs for Xor 
    Y = np.reshape([[0], [1], [1], [0]], (4,1,1)) # Actual outputs for Xor

    xor = NeuralNetwork(X, Y)
    xor.run()