from typing import Any
import pygame

class Grid:


    def __init__(self, rows : int, cols: int, rect : tuple[int]):
        self.rows = rows
        self.cols = cols
        self.rect = pygame.Rect(rect)
        self.line_colour = (0,0,0)
        self.cell_width = rect[2] / cols
        self.cell_height =  rect[3] / rows 

    def set_display(self, vertical : bool = True, horizontal : bool = True, border : bool = True):
        self.display_vertical = vertical
        self.display_horizontal = horizontal 
        self.display_border = border

    def set_colour(self, primary = None, secondary = None):
        self.primary_cell_colour = primary
        self.secondary_cell_colour = secondary

    def get_index(self, pos: tuple[int]) -> tuple[int]:
        i = 0
        j = 0

        return (i, j)
        

    def colour_cells(self, win : pygame.surface.Surface):
        if self.primary_cell_colour:
            for i in range(self.rows):
                for j in range(self.cols):
                    left = j * self.cell_width + self.rect.left
                    top = i * self.cell_height + self.rect.top

                    colour = self.primary_cell_colour

                    if (i + j) % 2 == 0 and self.secondary_cell_colour:
                        colour = self.secondary_cell_colour
                    
                    pygame.draw.rect(win, colour, (left, top, self.cell_width + 1, self.cell_height + 1))
    
    def draw(self, win : pygame.surface.Surface):
        self.colour_cells(win)

        # Border 
        if self.display_border:
            x = self.rect.left
            pygame.draw.line(win, self.line_colour, (x, self.rect.top), (x, self.rect.bottom))
            x += self.cols * self.cell_width
            pygame.draw.line(win, self.line_colour, (x, self.rect.top), (x, self.rect.bottom))

            y = self.rect.top
            pygame.draw.line(win, self.line_colour, (self.rect.left, y), (self.rect.right, y))
            y += self.rows * self.cell_height
            pygame.draw.line(win, self.line_colour, (self.rect.left, y), (self.rect.right, y))

        # Inner lines
        for i in range(1, self.rows):
            for j in range(1, self.cols):
                x = j * self.cell_width + self.rect.left
                y = i * self.cell_height + self.rect.top

                if self.display_vertical:
                    pygame.draw.line(win, self.line_colour, (int(x), self.rect.top), (int(x), self.rect.bottom)) # Draw vertical
                
                if self.display_horizontal:
                    pygame.draw.line(win, self.line_colour, (self.rect.left, int(y)), (self.rect.right, int(y)))

        

