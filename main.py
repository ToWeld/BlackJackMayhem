import os
import pygame
import effects
import sprite_list

FPS=30

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

pygame.init()
clock=pygame.time.Clock()
dis=pygame.display.set_mode((900,600))
dis.fill((0,0,0))

def load_image(name, colorkey=None, scale=1): #функция из примеров pygame
    fullname = os.path.join(data_dir, name)
    image = pygame.image.load(fullname)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

class Sprite(pygame.sprite.Sprite):
    def __init__(self, name, cords, colorkey=None):
        super().__init__()
        self.image, self.rect=load_image(name, colorkey=colorkey)
        self.rect.move_ip(cords[0], cords[1])
        

class MainMenu:
    def __init__(self):
        self.main=pygame.sprite.Group()
        FILES=sprite_list.MAIN_MENU_FILES
        LAYOUT=sprite_list.MAIN_MENU_LAYOUT
        self.start_button=Sprite(FILES["start_button"], LAYOUT["start_button"])
        self.main.add(self.start_button)
        self.window=Sprite(FILES["window"], LAYOUT["window"], colorkey=(255,255,255))
        self.main.add(self.window)
        self.wound=Sprite(FILES["wound"], LAYOUT["wound"], colorkey=(255,255,255))
        self.main.add(self.wound)

        self.bg=load_image(FILES["background"])[0]
        self.bg_cords=LAYOUT["background"]

        self.collide_rect_ratio=pygame.sprite.collide_rect_ratio(0.9)
        
    def draw(self,screen):
        screen.blit(self.bg, self.bg_cords)
        self.main.draw(screen)
        
    def event_handle(self, i):
        if i.type==pygame.MOUSEBUTTONDOWN:
            if self.collide_rect_ratio(cursor, self.start_button):
                self.wound.rect.center=i.pos
                need_update=True
            elif self.collide_rect_ratio(cursor, self.window):
                
                
            
        
        


act=True
need_update=True
general_group=pygame.sprite.Group()
cursor=Sprite(sprite_list.GENERAL["cursor"], (1000,1000), colorkey=-1)
general_group.add(cursor)
dis.fill((0,0,0))

scene=MainMenu()

while act:
    for i in pygame.event.get():
        if i.type==pygame.MOUSEMOTION:
            cursor.rect.center=i.pos
            need_update=True
        elif i.type==pygame.QUIT:
            act=False
        scene.event_handle(i)
    if need_update:
        dis.fill((0,0,0))
        scene.draw(dis)
        general_group.draw(dis)
        pygame.display.flip()
        need_update=False
    clock.tick(FPS)
        
        
