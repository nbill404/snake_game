import pygame
from grid import Grid
from snakegame import SnakeGame

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
        self.setup_grid(grid)

        font = pygame.font.SysFont("Calibri", 50)
        title_text = font.render("Snake Game", True, (0,0,0))

        font = pygame.font.SysFont("Calibri", 30)
        score_text = font.render("Score: " + str(game.score), True, (0,0,0))


        game_tick = 0
        game_end_text = None

        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not game.game_over and not game.win:
                # Game updates every 250ms
                game_tick += clock.tick(60)

                if game_tick >= 250:
                    game.update()
                    game_tick = 0

                    score_text = font.render("Score: " + str(game.score * 100), True, (0,0,0))
            elif game.game_over:
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
            
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r: 
                        game = SnakeGame(rows, cols)
                        game_end_text = None

            self.draw(win)
            grid.draw(win)
            self.render_game(win, game, grid)
            win.blit(title_text, (540, 20))
            win.blit(score_text, (1050, 100))

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

        pygame.draw.rect(win, (219, 46, 20), (x, y, w + 1, h))

        border = (
            ((x, y), (x + w, y)), 
            ((x, y), (x, y + h)),
            ((x + w, y), (x + w, y + h)),
            ((x, y + h), (x + w, y + h))
            )

        for (start, end) in border:
            pygame.draw.line(win, (241, 255, 38), start, end, width=2)

        for piece in snake:
            x = grid.rect.left + piece[1] * grid.cell_width
            y = grid.rect.top + piece[0] * grid.cell_height

            pygame.draw.rect(win, (105, 20, 7), (x, y, grid.cell_width + 1, grid.cell_height))


        






if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    app = App(1280, 720, (66, 197, 245))
    app.run()