import pygame
def transition_1(screen, frame):
    h=frame
    for i in range(frame+1):
        pygame.draw.rect(screen,(197,197,197), (i*10,h*10,10,10))
        h=h-1
    
    
