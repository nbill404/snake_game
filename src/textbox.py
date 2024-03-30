import pygame

class Textbox:

    def __init__(self, rect : tuple[int], text : str = "", colour = None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.colour = colour

        self.font = pygame.font.SysFont("Calibri", 30)
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))

    def draw(self, win):
        if self.colour:
            pygame.draw.rect(win, self.colour, self.rect)

        win.blit(self.text_surface, (self.rect.left, self.rect.top))