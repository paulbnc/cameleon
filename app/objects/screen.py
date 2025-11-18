import pygame

class Window:
    def __init__(self, 
                 width:int = 500, 
                 height:int = 500, 
                 hud_height:int = 0, 
                 fps:int = 120,
                 title:str = "CAMELEON",
                 background:tuple = (0, 0, 0)):
        self.width = width
        self.height = height
        self.hud_height = hud_height
        self.fps = fps
        self.title = title
        self.background = background
        self.clock = None
        self.screen = pygame.display.set_mode((width, height + hud_height))
    
    def set_title(self):
        pygame.display.set_caption(self.title)

    def update_clock(self):
        self.clock = pygame.time.Clock()

    def step(self):
        pygame.display.flip()
        self.clock.tick(self.fps)