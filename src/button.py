import pygame

class Button:

    def __init__(self, rect : tuple[int], text : str = "", colour = (0,215,255), font_size: int = 24):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.colour = colour

        self.font = pygame.font.SysFont("Calibri", font_size)
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))

    def clicked(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            return True
        
        return False

    def draw(self, win):
        pygame.draw.rect(win, self.colour, self.rect)
        win.blit(self.text_surface, (self.rect.left, self.rect.top))