# Snake Game with AI

This a program that recreates the game of Snake. The game can be played manually with options for AI simulations.

Currently there are three game modes the user can select
1. Player control
2. A* Pathfinding
3. NEAT AI algorithm

### Running the program

Dependencies can be installed using the following command
```
pip install -r requirements.txt
```

Run the project using
```
python main.py
```

### Game Mode 1 - Player Control
Click the "Play" button to start the game and try to achieve as high a score as possible.

Controls
Use WASD to move
Press R to reset the game

### Game Mode 2 - A* algorithm
The AI will use the A* pathfinding algorithm. The AI will determine the direction to move in with the minimal cost according to its heuristics. 

This is determined by the formula h(n) = f(n) + g(n). 
* f(n) is the distance of a tile from the snake head
* g(n) is the distance of a tile from the apple

### Game Mode 3 - NEAT algorithm
This is an algorithm that combines neural networks and genetic algorithms. The implementation was done with the help of the neat-python library.

This algorithm encodes its genetic information as a series of nodes in a neural network. Beginning as a minimal size network, it then mutates by adding connections and nodes in order to find a way to solve the problem. In this case it will play the game snake.

The network contains 7 inputs which are:
* relative x, y position of the snake head from the apple
* 4 sensors detecting objects directly next to the snake head (-1 = Wall, 0 = Nothing, 1 = Snake body, 2 = Apple)
* distance from the apple

There are 4 outputs corresponding to each direction the snake can move.

The fitness function used is the score (number of apples collected).