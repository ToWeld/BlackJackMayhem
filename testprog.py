import pygame
from tools import AnimatedSprite
pygame.init()
dis=pygame.display.set_mode((900,600))
sprite=AnimatedSprite("testanimation.png", (0,0), (93,75,15))
main=pygame.sprite.Group()
main.add(sprite)
clock=pygame.time.Clock()
while True:
    dis.fill((0,0,0))
    sprite.next_frame(0,15)
    main.draw(dis)
    clock.tick(10)
    pygame.display.flip()
                
    
    
    
