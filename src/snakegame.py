from random import randint, shuffle
from copy import deepcopy

class SnakeGame:
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1)) # left, right, Up, down, 

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols

        self.score = 0
        self.randomize_snake()
        self.prev_tail = self.snake[-1]

        self.apple = self.snake[0]
        self.randomize_apple()

        self.start = False
        self.game_over = False
        self.win = False
        
    def update(self):
        if self.check_win():
            self.win = True
            return
        elif not self.is_valid():
            self.game_over = True
            return

        self.move()
        self.check_apple()
            

    def change_dir(self, index: int):
        self.dir = SnakeGame.directions[index]

    def move(self):
        self.prev_tail = deepcopy(self.snake[-1])

        self.update_matrix(self.prev_tail, "remove")

        for piece in range(len(self.snake) - 1, 0, -1):
            self.snake[piece][0] = self.snake[piece - 1][0]
            self.snake[piece][1] = self.snake[piece - 1][1]

        self.snake[0][0] += self.dir[0]
        self.snake[0][1] += self.dir[1]

        self.update_matrix(self.snake[0], "add")

    def update_matrix(self, pos, op):
        match op:
            case "add":
                self.matrix[pos[0]][pos[1]] += 1
            case "remove":
                self.matrix[pos[0]][pos[1]] -= 1
    
    def is_valid(self) -> bool:
        # Check out of bounds

        if not self.is_inbounds(self.snake[0]):
            return False

        # Check overlap
        for piece in self.snake:
            if self.matrix[piece[0]][piece[1]] == 2:
                return False
            elif self.matrix[piece[0]][piece[1]] != 0 and self.matrix[piece[0]][piece[1]] != 1:
                raise Exception("Somethings wrong")

        return True
    
    def check_win(self):
        return self.score == self.rows * self.cols
           
    def randomize_apple(self):
        while self.apple in self.snake:
            self.apple = [randint(0, self.rows - 1), randint(0, self.cols - 1)]

    def randomize_snake(self, length = 3):
        head = [randint(0, self.rows - 1), randint(0, self.cols - 1)]
        dir = SnakeGame.directions[randint(0,3)]

        next = [head[0] + dir[0], head[1] + dir[1]]

        # Ensure initial direction does not go out of bounds
        while not self.is_inbounds(next):
            dir = SnakeGame.directions[randint(0, 3)]
            next = [head[0] + dir[0], head[1] + dir[1]]

        snake = [head]
        matrix = [[0 for _ in range(self.cols + 1)] for __ in range(self.rows + 1)]
        matrix[head[0]][head[1]] = 1

        # Uses DFS algorithm to create snake body
        self.create_body(length - 1, snake, next,  matrix)

        self.snake = deepcopy(snake)
        self.matrix = deepcopy(matrix)
        self.dir = dir

    def create_body(self, length, snake, next, matrix):
        if length == 0:
            return True
        
        # Randomly choose a direction to try to move in
        dirs = [x for x in range(4)]
        shuffle(dirs)

        prev = snake[-1]

        for i in dirs:
            d = SnakeGame.directions[i]
            i = prev[0] + d[0]
            j = prev[1] + d[1]
            

            if self.is_inbounds((i, j)) and matrix[i][j] != 1 and i != next[0] and j != next[1]:
                matrix[i][j] = 1
                snake.append([i, j])

                if self.create_body(length - 1, snake, next, matrix):
                    return True
                
                matrix[i][j] = 0
                snake.pop()
                
        return False
             

    def is_inbounds(self, pos):
        return (0 <= pos[0] and pos[0] < self.rows) and (0 <= pos[1] and pos[1] < self.cols)
            

    def check_apple(self):
        if self.snake[0][0] == self.apple[0] and self.snake[0][1] == self.apple[1]:
            self.score += 1
            self.snake.append(self.prev_tail)
            self.update_matrix(self.prev_tail, "add")
            self.randomize_apple()
