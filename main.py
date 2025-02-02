import os
import pygame
import effects
import assets_list
from tools import *

FPS=30

DEFAULT_FPS=30

VERSION="0.2-indev"

class MainMenu:
    def __init__(self):
        self.main=pygame.sprite.Group()
        FILES=assets_list.MAIN_MENU_FILES
        LAYOUT=assets_list.MAIN_MENU_LAYOUT
        ANIMATIONDATA=assets_list.MAIN_MENU_ANIMATIONDATA
        SFX=assets_list.MAIN_MENU_SFX
        self.window=AnimatedSprite(FILES["window"], LAYOUT["window"],ANIMATIONDATA["window"])
        self.main.add(self.window)

        self.enterance_rect=pygame.Rect(LAYOUT["enterance_rect"])

        self.bg=load_image(FILES["background"])[0]
        self.bg_cords=LAYOUT["background"]

        self.walking_sound=load_sound(SFX["walking"])
        self.shot_sound=load_sound(SFX["shot"])
        self.shot_sound.set_volume(0.3)
        
        self.collide_rect_ratio=pygame.sprite.collide_rect_ratio(0.9)
        
    def draw(self,screen):
        screen.blit(self.bg, self.bg_cords)
        self.main.draw(screen)
        
    def event_handle(self, i):
        global need_update
        global act
        if i.type==pygame.MOUSEBUTTONDOWN:
            if self.enterance_rect.collidepoint(i.pos):
                self.walking_sound.play()
                need_update=True
                global FPS
                FPS=90
                global update_class
                update_class=Transition(effects.effect_1(150), Shooter())
                
            elif self.collide_rect_ratio(cursor, self.window):
                i=self.window.frame_count-1
                self.shot_sound.play()
                while i!=0:
                    self.window.next_frame(0,self.window.frame_count-1)
                    dis.fill((0,0,0))
                    scene.draw(dis)
                    pygame.display.flip()
                    clock.tick(FPS)
                    i=i-1
                pygame.time.delay(100)
                act=False


class Shooter:
    def __init__(self):
        self.main=pygame.sprite.Group()
        FILES=assets_list.MAIN_MENU_FILES
        LAYOUT=assets_list.MAIN_MENU_LAYOUT
        ANIMATIONDATA=assets_list.MAIN_MENU_ANIMATIONDATA
        self.window=AnimatedSprite(FILES["window"], LAYOUT["window"],ANIMATIONDATA["window"])
        self.main.add(self.window)

        self.enterance_rect=pygame.Rect(LAYOUT["enterance_rect"])

        self.bg=load_image(FILES["background"])[0]
        self.bg_cords=LAYOUT["background"]
        
        self.collide_rect_ratio=pygame.sprite.collide_rect_ratio(0.9)
        
    def draw(self, screen):
        screen.fill((0,255,0))

    def event_handle(self, i):
        pass
        

class ScreenUpdate:
    def draw(self):
        global need_update
        dis.fill((0,0,0))
        scene.draw(dis)
        general_group.draw(dis)
        pygame.display.flip()
        need_update=False
        
class Transition:
    def __init__(self, effect, new_scene):
        self.effect=effect
        self.new_scene=new_scene
    def draw(self):
        if self.effect.is_end():
            pygame.mixer.fadeout(1000)
            global FPS
            FPS=DEFAULT_FPS
            global scene
            scene=self.new_scene
            global need_update
            need_update=True
            global update_class
            update_class=ScreenUpdate()
        else:
            self.effect.draw(dis)
            pygame.display.flip()
                
    
pygame.init()
clock=pygame.time.Clock()
dis=pygame.display.set_mode((900,600))
pygame.mouse.set_visible(False)
pygame.display.set_caption("BlackJack Mayhem!        ver."+VERSION)
dis.fill((0,0,0))
act=True
need_update=True
general_group=pygame.sprite.Group()
cursor=Sprite(assets_list.GENERAL["cursor"], (1000,1000), colorkey=-1)
general_group.add(cursor)
dis.fill((0,0,0))

scene=MainMenu()
update_class=ScreenUpdate()

while act:    
    for i in pygame.event.get():
        if i.type==pygame.MOUSEMOTION:
            cursor.rect.center=i.pos
            need_update=True
        elif i.type==pygame.QUIT:
            act=False
        scene.event_handle(i)
    if need_update:
        update_class.draw()
    clock.tick(FPS)
        
        
