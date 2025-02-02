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
        
        
    
