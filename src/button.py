import pygame

class Button:

    def __init__(self, rect : tuple[int], text : str = "", colour = (0,215,255)):
        self.rect = pygame.Rect(rect)
        self.colour = colour

    def clicked(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            return True
        
        return False

    def draw(self, win):
        pygame.draw.rect(win, self.colour, self.rect)