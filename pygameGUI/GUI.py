# import statements
import pygame
import numpy as np

class GUI(object):
    """Stores basic variables of pygame GUI (widht, height and caption of window)"""
    def __init__(self, name, width, height):
        """Constructor of GUI class instance
        
        Args
        ----
        name: string
            string to be displayed in caption of pygame window
        width, height: integer
            resolution of pygame window
        """
        self.width = width
        self.height = height
        pygame.display.set_caption(name)

    def make_surface(self, mu_rgb):
        """Create pygame surface. Swap rows and columns of mu_rgb to move from matrix coordinate space to pygame coordinate space
        
        Args
        ----
        mu_rgb: np.array
            contains RGB color for every single point we evaluated on the complex plane (from class Fractal)

        Returns
        -------
        pygame surface in which we set each pixel to its according color in the pygame coordinate system
        """
        return pygame.surfarray.make_surface(np.transpose(mu_rgb, (1, 0, 2)))

class Button():
    """
    Constructor of button class

    Class based on:
    --------
    https://www.youtube.com/watch?v=4_9twnEduFA
    """
    def __init__(self, color, text_color, x_pos, y_pos, width, height, text=''):
        self.color = color
        self.text_color = text_color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.text = text

    def show(self, screen):
        """Show buttons on pygame screen
        
        Args
        ----
        screen: pygame screen
            the screen on which the game is currently displayed
        """
        pygame.draw.rect(screen, True, (self.x_pos-2, self.y_pos-2, self.width+4, self.height+4), 0) # draw black rectangle
        # draw button on same spot that is slightly smaller (left-over black rectangle creates outline)
        pygame.draw.rect(screen, self.color, (self.x_pos, self.y_pos, self.width,self.height), 0) 
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 22)
            rendered_txt = font.render(self.text, 1, self.text_color)
            screen.blit(rendered_txt, (self.x_pos + (self.width / 2 - rendered_txt.get_width() / 2), self.y_pos + (self.height/2 - rendered_txt.get_height()/2)))

    def isOver(self, point):
        """Detect if given point (as tuple (x,y)) is within the x- and y-limits of the button
        
        Args
        ----
        point: tuple of 2 integer (in pygame coordinates)
        """
        if point[0] > self.x_pos and point[0] < self.x_pos + self.width:
            if point[1] > self.y_pos and point[1] < self.y_pos + self.height:
                return True
        return False