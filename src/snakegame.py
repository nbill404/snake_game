from random import randint, shuffle
from copy import deepcopy

class SnakeGame:
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1)) # Up, down, left, right

    def __init__(self, rows: int, cols: int, length: int = 3):
        self.rows = rows
        self.cols = cols

        self.reset(length)

    def reset(self, length: int = 3):
        self.score = 0
        self.randomize_snake(length)
        self.prev_tail = self.snake[-1]

        self.apple = self.snake[0]
        self.randomize_apple()

        self.start = True
        self.game_over = False
        self.win = False
        self.hit_wall = False
        self.hit_self = False

        self.distance = 0
        self.last_apple = 0
        
        
    def update(self):
        if not self.start:
            return

        if self.check_win():
            self.start = False
            self.win = True
            return
        elif not self.is_valid():
            self.start = False
            self.game_over = True
            return

        self.move()
        self.check_apple()

        self.distance += 1
            

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

        if not self.is_valid():
            self.start = False
            self.game_over = True
            return

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
            self.hit_wall = True
            return False

        # Check overlap
        for piece in self.snake:
            if self.matrix[piece[0]][piece[1]] == 2:
                self.hit_self = True
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
        matrix = [[0 for _ in range(self.cols)] for __ in range(self.rows)]
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

            self.last_apple = self.distance

class SnakePredetermined(SnakeGame):

    def __init__(self, rows: int, cols: int):
        self.apple_num = 0
        self.apples = []

        with open("sequence.txt", "r") as file:
            for line in file:
                txt = line.strip()
                self.apples.append(list(map(int, txt.split(","))))

        super().__init__(rows, cols, 0)


    def reset(self, length = 0):
        self.apple_num = 0
        self.randomize_apple()

        self.score = 0
        self.randomize_snake()
        self.prev_tail = self.snake[-1]

        self.start = False
        self.game_over = False
        self.win = False

    def randomize_snake(self, length=3):
        self.matrix = [[0 for _ in range(self.cols)] for __ in range(self.rows)]
        self.dir = (-1, 0)
        self.snake = [[8,10], [9, 10], [9, 11]]
        self.update_matrix(self.snake[0], "add")
        self.update_matrix(self.snake[1], "add")
        self.update_matrix(self.snake[2], "add")


    def randomize_apple(self):
        self.apple = self.apples[self.apple_num]
        self.apple_num += 1
