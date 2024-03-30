import pygame
import pathfind
from grid import Grid
from snakegame import SnakeGame, SnakePredetermined
from math import sin, cos, atan2
from button import Button
from textbox import Textbox
from genetic import GeneticSnakeSolver

class App:

    def __init__(self, width: int, height: int, bg_colour : tuple[int] = (0,0,0)):
        self.width = width
        self.height = height
        self.bg_colour = bg_colour

    def run(self) -> None:
        win = pygame.display.set_mode((self.width, self.height))
        self.running = True
        clock = pygame.time.Clock()
        game_tick = 0

        rows = 18
        cols = 24

        grid = Grid(rows, cols, (240, 80, 800, 600))
        game = SnakeGame(rows, cols)
        self.setup_grid(grid)
        self.game_mode = 2 
        
        button1 = Button((75, 100, 100, 40), "Start", (245, 33, 120))
        button2 = Button((75, 200, 100, 40), "A*", (255, 23, 34)) 
        button3 = Button((75, 300, 100, 40), "Genetic Algorithm", (123, 33, 97))

        buttons = [button1, button2, button3]

        drawables = [button1, button2, button3, Textbox((540, 20, 0, 0), "Snake Game"), Textbox((1050, 100, 0, 0), "Score: " + str(game.score))]
        
        # self.geneticAi = None
        self.geneticAi = self.geneticAi = GeneticAI(game.rows, game.cols, 1000)

        while self.running:
            game_tick += clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
 
            if game_tick >= 250: # Game updates every 1/4th second
                match self.game_mode:
                    case 0:
                        game.update()
                    case 1:
                        game.dir = self.get_ai_move(game)
                        game.update()
                    case 2:
                        self.geneticAi.update()
                        game = self.geneticAi.games[0]
                        
                game_tick = 0

            self.app_controls(game, buttons)

            if self.game_mode == 0:
                self.player_controls(game)
    
                if game.game_over:
                    print("You lose")
                elif game.win:
                    print("You win")

            self.draw(win, drawables)
            grid.draw(win)

            if self.game_mode == 2:
                for game in self.geneticAi.games:
                    if game.start:
                        self.render_game(win, game, grid)
            else:
                self.render_game(win, game, grid)

            pygame.display.update()

    def app_controls(self, game, buttons):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            game.start = True
        elif keys[pygame.K_r]:
            game.reset()

        events = pygame.event.get()

        for e in events:
            if e.type == pygame.QUIT:
                self.running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].clicked():
                    self.game_mode = 0
                    game.start = True
                elif buttons[1].clicked():
                    self.game_mode = 1
                elif buttons[2].clicked():
                    self.game_mode = 2
                    self.geneticAi = GeneticAI(game.rows, game.cols)

    def player_controls(self, game):  
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            game.change_dir(0)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            game.change_dir(1)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            game.change_dir(2)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            game.change_dir(3)


    def get_ai_move(self, game):
        # A* algorithm
        next = pathfind.get_next(game.matrix, game.snake[0], game.apple)
        if next:
            return (next[0] - game.snake[0][0], next[1] - game.snake[0][1])
        else:
            # Picks direction if path is not found 
            return (0 , 1)


    def setup_grid(self, grid: Grid):
        grid.set_display(vertical=False, horizontal=False)
        grid.set_colour(primary=(19, 133, 13), secondary=(51, 191, 44))

    def draw(self, win : pygame.surface.Surface, drawables) -> None:
        win.fill(self.bg_colour)

        for e in drawables:
            e.draw(win)

    def render_game(self, win: pygame.surface.Surface, game: SnakeGame, grid: Grid):
        apple = game.apple
        snake = game.snake
        head = snake[0]

        h = grid.cell_height
        w = grid.cell_width

        x = grid.rect.left + apple[1] * w
        y = grid.rect.top + apple[0] * h

        # Apple
        pygame.draw.rect(win, (219, 46, 20), (x, y, w + 1, h))

        border = (
            ((x, y), (x + w, y)), 
            ((x, y), (x, y + h)),
            ((x + w, y), (x + w, y + h)),
            ((x, y + h), (x + w, y + h))
            )

        # Apple Border
        for (start, end) in border:
            pygame.draw.line(win, (241, 255, 38), start, end, width=2)

        # Snake
        for piece in snake:
            x = grid.rect.left + piece[1] * grid.cell_width
            y = grid.rect.top + piece[0] * grid.cell_height

            pygame.draw.rect(win, (105, 20, 7), (x, y, grid.cell_width + 1, grid.cell_height))

        c = (grid.cell_width - 10) / 2
        x = (grid.rect.left + c) + head[1] * grid.cell_width
        y = (grid.rect.top + c) + head[0] * grid.cell_height
        x += game.dir[1] * c
        y += game.dir[0] * c
        
        pygame.draw.rect(win, (0, 0, 0), (x, y, 10, 10))
        # pygame.draw.rect(win, (0, 0, 0), (x + eye2x, y + eye2y, 10, 10))

    def rotate(self, px, py, cx, cy, angle):
        pass

        
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






if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    app = App(1280, 720, (66, 197, 245))
    app.run()