from random import randint
from copy import deepcopy

class SnakeGame:
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1)) # left, right, Up, down, 

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.matrix = [[0 for _ in range(self.cols + 1)] for __ in range(self.rows + 1)]

        self.score = 0
        self.snake = [[-1, -1] for _ in range(3)]
        self.prev_tail = self.snake[-1]
        self.dir = [0, -1]
        self.randomize_snake()

        self.apple = self.snake[0]
        self.randomize_apple()

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
        i = self.snake[0][0]
        j = self.snake[0][1]

        if not ((0 <= i and i < self.rows) and (0 <= j and j < self.cols)):
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

    def randomize_snake(self):
        valid = False

        while not valid:
            valid = True

            self.dir = SnakeGame.directions[randint(0,3)]
            self.snake[0] = [randint(0, self.rows), randint(0, self.cols)]

            # Generate the rest of the pieces
            for n in range(1, 3):
                d = SnakeGame.directions[randint(0,3)]
                i = self.snake[n - 1][0] + d[0]
                j = self.snake[n - 1][1] + d[1]
                new_piece = [i,j]
                

                if ((0 <= new_piece[0] and new_piece[0] < self.rows) and (0 <= new_piece[1] and new_piece[1] < self.cols)):
                    if new_piece not in self.snake:
                        self.snake[n] = [i, j]
                else:
                    valid = False
                    break
            
            # Ensure intial movement is valid
            i = self.snake[0][0] + self.dir[0]
            j = self.snake[0][1] + self.dir[1]
            new_piece = [i, j]

            if not ((0 <= new_piece[0] and new_piece[0] < self.rows) and (0 <= new_piece[1] and new_piece[1] < self.cols)):
                valid = False
            elif new_piece in self.snake:
                valid = False

        self.snake = deepcopy(self.snake)
        
        for piece in self.snake:
            self.update_matrix(piece, "add")
            

    def check_apple(self):
        if self.snake[0][0] == self.apple[0] and self.snake[0][1] == self.apple[1]:
            self.score += 1
            self.snake.append(self.prev_tail)
            self.update_matrix(self.prev_tail, "add")
            self.randomize_apple()
