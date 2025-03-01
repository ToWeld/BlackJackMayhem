import pygame
class effect_1:
    def __init__(self, end_frame):
        self.curr_frame=0
        self.end_frame=end_frame
        
    def draw(self,screen):
        h=self.curr_frame
        for i in range(self.curr_frame+1):
            pygame.draw.rect(screen,(0,0,0), (i*10,h*10,10,10))
            h=h-1
        self.curr_frame=self.curr_frame+1

    def is_end(self):
        return self.curr_frame>=self.end_frame

class effect_2:
    def __init__(self, width, height):
        self.curr_frame=0
        self.height=height
        self.width=width
    def draw(self, screen):
        pygame.draw.rect(screen,(0,0,0), (0, self.height-self.curr_frame*10-10, self.width, 10))
        self.curr_frame=self.curr_frame+1
    def is_end(self):
        return self.curr_frame*10>=self.height

class effect_3:
    def __init__(self, width, height):
        self.curr_frame=0
        self.height=height
        self.width=width
        
    def draw(self, screen):
        pygame.draw.rect(screen,(0,0,0), (self.curr_frame*10, 0,10, self.height,))
        pygame.draw.rect(screen,(0,0,0), (self.width-self.curr_frame*10, 0,10, self.height))
        self.curr_frame=self.curr_frame+1
        
    def is_end(self):
        return self.curr_frame*10>=self.width//2
        
        
    
