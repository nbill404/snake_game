import pygame

from pathfind import get_ai_move
from grid import Grid
from snakegame import SnakeGame
from button import Button
from textbox import Textbox
from genetic import GeneticAI
from neuralai import NeuralAi, convert_x, convert_y
from neatai import NeatAI
from random import randint

class App:

    def __init__(self, width: int, height: int, bg_colour : tuple[int] = (0,0,0)):
        self.width = width
        self.height = height
        self.bg_colour = bg_colour

        self.rows = 18
        self.cols = 24

        self.running = True


    def run(self) -> None:
        win = pygame.display.set_mode((self.width, self.height))
        clock = pygame.time.Clock()
        game_tick = 0

        grid = Grid(self.rows, self.cols, (240, 80, 800, 600))
        game = SnakeGame(self.rows, self.cols)
        self.setup_grid(grid)
        
        button1 = Button((50, 100, 150, 40), "Play", (245, 33, 120))
        button2 = Button((50, 200, 150, 40), "A*", (255, 23, 34)) 
        button3 = Button((50, 300, 150, 40), "Neural Network", (123, 33, 97))

        buttons = [button1, button2, button3]
        drawables = [grid, button1, button2, button3, Textbox((540, 20, 0, 0), "Snake Game"), Textbox((1050, 100, 0, 0), "Score: " + str(game.score)) , None]
        
        self.game_mode = 0
        self.tick_speed = 0

        match self.game_mode:
            case 0: # Player control
                game.start = False
                self.tick_speed = 250
            case 1: # A* Pathfinding
                pass
            case 2: # Genetic Algorithm
                self.geneticAi = GeneticAI(game.rows, game.cols, 1000)
            case 3: # Neural Network
                self.neuralAi = NeuralAi(convert_x(game), convert_y(game.dir))
                # self.neuralAi.load()
                game.start = True
            case 4: # NEAT Algorithm
                self.neatAi = NeatAI()

        while self.running:
            game_tick += clock.tick(60) # 60 Fps

            # Main game loop
            if game_tick >= self.tick_speed: # Game updates every 1/4th second
                match self.game_mode:
                    case 0:
                        if game.start:
                            game.update()
                    case 1:
                        game.dir = get_ai_move(game)
                        game.update()
                    case 2:
                        self.geneticAi.update()
                        game = self.geneticAi.games[0]
                    case 3: 
                        self.neuralAi.x = convert_x(game)
                        self.neuralAi.y = convert_y(get_ai_move(game))
                        self.neuralAi.train()

                        self.neuralAi.predict(convert_x(game), convert_y(get_ai_move(game)))
                        game.dir = self.neuralAi.output
                        game.update()

                        if not game.start:
                            game.reset()
                            game.start = True
                            print("Game Reset")
                    case 4:
                        self.neatAi.update()
                        
                game_tick = 0

            # Controls
            self.app_controls(game, buttons)

            if self.game_mode == 0:
                self.player_controls(game)

                drawables[5] = Textbox((1050, 100, 0, 0), "Score: " + str(game.score))
    
                if game.game_over:
                    drawables[6] = Textbox((550, 350, 100, 40), "You lose", (255,255,255))
                elif game.win:
                    drawables[6] = Textbox((550, 350, 100, 40), "You Win!", (255,255,255))

                
            # Rendering
            self.draw(win, drawables, game, grid)
            pygame.display.update()

    def app_controls(self, game, buttons):
        events = pygame.event.get()

        for e in events:
            if e.type == pygame.QUIT:
                self.running = False
            
            if e.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].clicked():
                    self.game_mode = 0
                    game.start = True
                    self.tick_speed = 250
                elif buttons[1].clicked():
                    self.game_mode = 1
                    self.tick_speed = 250
                elif buttons[2].clicked():
                    self.game_mode = 4
                    self.neatAi = NeatAI()
                    self.tick_speed = 0
            
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    game.start = not game.start
                elif e.key == pygame.K_r:
                    game.reset()

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
    

    def setup_grid(self, grid: Grid):
        grid.set_display(vertical=False, horizontal=False)
        grid.set_colour(primary=(19, 133, 13), secondary=(51, 191, 44))

    def draw(self, win: pygame.surface.Surface, drawables, game: SnakeGame, grid: Grid) -> None:
        win.fill(self.bg_colour)



        for obj in drawables:
            if obj is not None:
                obj.draw(win)

        if self.game_mode == 2:
            for game in self.geneticAi.games:
                if game.start:
                    self.render_game(win, game, grid)
        elif self.game_mode == 4:
            for game in self.neatAi.games:
                if game.start:
                    self.render_game(win, game, grid)
        else:
            self.render_game(win, game, grid)

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

        








if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    app = App(1280, 720, (66, 197, 245))
    app.run()