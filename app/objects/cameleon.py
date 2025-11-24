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

    def handle_input(self)->str:
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
        return self.last_action

    def draw(self, screen)->None:
        pygame.draw.rect(screen, self.color, self.rect)
        #pour un skin en png : screen.blit(self.skin, (self.x, self.y))
    
    def move(self, x:float = None, y:float = None, action:str = None):
        if action=='left':
            self.x -= self.speed
        if action=='right':
            self.x += self.speed
        if action=='up':
            self.y -= self.speed
        if action=='down':
            self.y += self.speed

        if action is not None:
            self.last_action = action
        elif (x is not None) and (y is not None):
            self.x = x
            self.y = y

        self.check_collide()
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

        decay = 0.95

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
            var = width
            height *= decay
            width *= decay
            y += block.height + 1
            x += (var - width)/2
            self.blocks.append(block)

        self.segment_distance = height + 1

    def draw(self, screen):
        for block in self.blocks:
            block.draw(screen)

    def handle_input(self):
        head = self.blocks[0]
        head.handle_input()

        for i in range(1, len(self.blocks)):
            current_block = self.blocks[i]
            previous_block = self.blocks[i - 1]

            dx = previous_block.x - current_block.x
            dy = previous_block.y - current_block.y

            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance > self.segment_distance:
                ratio = self.segment_distance / distance
                target_x = previous_block.x - dx * ratio
                target_y = previous_block.y - dy * ratio

                current_block.x = target_x
                current_block.y = target_y

                current_block.rect = pygame.Rect(current_block.x,
                                                   current_block.y,
                                                   current_block.width,
                                                   current_block.height)

