import pygame
import pathfind
from grid import Grid
from snakegame import SnakeGame
from math import sin, cos, atan2
from button import Button

class App:

    def __init__(self, width: int, height: int, bg_colour : tuple[int] = (0,0,0)):
        self.width = width
        self.height = height
        self.bg_colour = bg_colour

    def run(self) -> None:
        win = pygame.display.set_mode((self.width, self.height))
        running = True
        clock = pygame.time.Clock()

        rows = 18
        cols = 24

        grid = Grid(rows, cols, (240, 80, 800, 600))
        game = SnakeGame(rows, cols)

        print(game.snake)

        self.setup_grid(grid)

        font = pygame.font.SysFont("Calibri", 50)
        title_text = font.render("Snake Game", True, (0,0,0))

        font = pygame.font.SysFont("Calibri", 30)
        score_text = font.render("Score: " + str(game.score), True, (0,0,0))

        game_tick = 0
        game_end_text = None

        button = Button((100, 100, 100, 40), "Click", (245, 33, 120))

        ai_running = False

        while running:
            clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if game.start:
                # Game updates every 250ms
                game_tick += clock.tick(60)

                if game_tick >= 250:

                    if ai_running:
                        next = pathfind.get_next(game.matrix, game.snake[0], game.apple)
                        if next:
                            game.dir = (next[0] - game.snake[0][0], next[1] - game.snake[0][1])
                        else:
                            game.dir = (0, 1)


                    game.update()
                    game_tick = 0

                    score_text = font.render("Score: " + str(game.score * 100), True, (0,0,0))
            
            if game.game_over:
                game_end_text = font.render("You lose", True, (0,0,0))
            elif game.win:
                game_end_text = font.render("You win!", True, (0,0,0))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                game.change_dir(0)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                game.change_dir(1)
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                game.change_dir(2)
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                game.change_dir(3)
            elif keys[pygame.K_SPACE]:
                game.start = True
            elif keys[pygame.K_r]:
                game = SnakeGame(rows, cols)
                game_end_text = None

            
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    running = False

                if e.type == pygame.MOUSEBUTTONDOWN:
                    if button.clicked():
                        ai_running = True

                        

            self.draw(win)
            grid.draw(win)
            self.render_game(win, game, grid)
            win.blit(title_text, (540, 20))
            win.blit(score_text, (1050, 100))
            button.draw(win)

            if game_end_text is not None:
                x = 550
                x_offset = 50
                y = 300
                y_offset = 15

                pygame.draw.rect(win, (255,255,255), (x, y, 200, 60))
                win.blit(game_end_text, (x + x_offset, y + y_offset))


            pygame.display.update()

    def setup_grid(self, grid: Grid):
        grid.set_display(vertical=False, horizontal=False)
        grid.set_colour(primary=(19, 133, 13), secondary=(51, 191, 44))

    def draw(self, win : pygame.surface.Surface) -> None:
        win.fill(self.bg_colour)

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

        






if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    app = App(1280, 720, (66, 197, 245))
    app.run()