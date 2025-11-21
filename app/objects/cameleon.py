import pygame

class Block:
    def __init__(self, 
                 w_width:int, 
                 w_height:int,
                 w_hud:int, 
                 height:int = 30, 
                 width:int = 30, 
                 color:tuple = (20, 150, 50),
                 speed:int = 10,
                 x = None,
                 y = None):
        if (x is not None) and (y is not None):
            self.x = x
            self.y = y
        else:
            self.x = float(w_width/2)
            self.y = float(w_height + w_hud - height)
        self.height = height
        self.width = width
        self.color = color
        self.speed = speed
        self.rect = pygame.Rect(self.x, 
                                self.y, 
                                self.width, 
                                self.height)
        self.last_action = 'up'
        
        self.w_h = w_height
        self.w_w = w_width
        self.w_hud = w_hud
    
    def check_collide(self):
        if self.y > self.w_h + self.w_hud - self.height:
            self.y = self.w_h + self.w_hud - self.height
        if self.y < self.w_hud:
            self.y = self.w_hud
        if self.x > self.w_w - self.width:
            self.x = self.w_w - self.width
        if self.x < 0:
            self.x = 0

    def handle_input(self)->None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.last_action = 'left'
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.last_action = 'right'
        if keys[pygame.K_UP]:
            self.y -= self.speed
            self.last_action = 'up'
        if keys[pygame.K_DOWN]:
            self.y += self.speed
            self.last_action = 'down'
        
        self.check_collide()

        self.rect = pygame.Rect(self.x, 
                                self.y, 
                                self.width, 
                                self.height)

    def draw(self, screen)->None:
        pygame.draw.rect(screen, self.color, self.rect)
        #pour un skin en png : screen.blit(self.skin, (self.x, self.y))
    
    def move(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, 
                                self.y, 
                                self.width, 
                                self.height)

class Cameleon:
    def __init__(self,
                 w_width:int, 
                 w_height:int,
                 w_hud:int, 
                 n_blocks:int = 4,
                 height:int = 30, 
                 width:int = 30, 
                 color:tuple = (20, 150, 50),
                 speed:int = 5):
        self.blocks = []

        x = float(w_width/2)
        y = float((w_height + w_hud - height)/2)

        for i in range(n_blocks):
            block = Block(w_width, 
                                w_height,
                                w_hud, 
                                height, 
                                width, 
                                color,
                                speed,
                                x,
                                y)
            y += block.height
            self.blocks.append(block)
  
    def draw(self, screen):
        for block in self.blocks:
            block.draw(screen)

    def handle_input(self):
        head = self.blocks[0]
        old_positions = [(head.x, head.y)]
        head.handle_input()

        for i in range(1, len(self.blocks)):
            block = self.blocks[i]
            prev = self.blocks[i-1]
            old_positions.append((block.x, block.y))
            block.move(old_positions[i-1][0], old_positions[i-1][1])
