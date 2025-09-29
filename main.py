import os
import pygame
import effects
import main_menu
import assets_list
from tools import *

FPS=30

DEFAULT_FPS=30

VERSION="0.25-indev"

#:---  Органы управления Controller  ---:

#nu(x=True) - (need_update) необходима отрисовка всего экрана заново
#set_fps(x) - количество кадров в секунду
#draw(screen) - отрисовка экрана
#transition(effect, new_scene) - запустить переход с эффектом с одной сцены на другую
#cutscene(fps) - запустить анимацию(катсцену) с возвратом на прежнюю сцену
#terminate() - покончить с этим...

#SCREEN_SIZE - константа - размер окна
#cursor - pygame.Rect курсора
#:---  ---:

class Controller:
    def __init__(self, cursor):
        self.need_update=True #необходима отриисовка всего экрана заново
        self.active=True #отрисовка всего экрана заново, реакция сцены на события
        self.run=True #работа программы
        self.fps=DEFAULT_FPS #количество кадров в секунду
        self.draw=self.draw_normal #отрисовка экрана
        self.scene=None #текущая сцена
        self.cursor=cursor #курсор
        self.effect=None #текущий эффект перехода
        
        self.SCREEN_SIZE=(900, 600)

    def draw_normal(self, screen):
        screen.fill((0,0,0))
        self.scene.draw(dis)
        self.need_update=False

    def draw_transition(self, screen):
        if self.effect.is_end():
            self.effect=None
            pygame.mixer.fadeout(1000)
            self.active=True
            self.fps=DEFAULT_FPS
            self.draw=self.draw_normal
        else:
            self.effect.draw(screen)

    def draw_cutscene(self, screen):
        if self.scene.is_end():
            self.active=True
            self.fps=DEFAULT_FPS
            pygame.mixer.fadeout(100)
            self.draw=self.draw_normal
        else:
            self.scene.draw_cutscene(screen)

    def transition(self, effect, new_scene):
        self.active=False
        self.need_update=True
        self.fps=90
        self.effect=effect
        self.scene=new_scene
        self.draw=self.draw_transition

    def cutscene(self, fps):
        self.need_update=True
        self.active=False
        self.fps=fps
        self.draw=self.draw_cutscene

    def terminate(self):
        self.run=False

    def nu(self, x=True):
        self.need_update=x

    def set_fps(self, x):
        self.fps=int(x)

pygame.init()
clock=pygame.time.Clock()
dis=pygame.display.set_mode((900,600))
pygame.mouse.set_visible(False)
pygame.display.set_caption("BlackJack Mayhem!        ver."+VERSION)
pygame.display.set_icon(load_image(assets_list.GENERAL["icon"])[0])

cursor_image, cursor_image_rect=load_image(assets_list.GENERAL["cursor"])
xoffset=cursor_image_rect.width//2
yoffset=cursor_image_rect.height//2
cursor=pygame.Rect(1000, 1000, 4, 4)

master=Controller(cursor)
master.scene=main_menu.MainMenu(master)

dis.fill((0,0,0))
while master.run:
    for i in pygame.event.get():
        if i.type==pygame.MOUSEMOTION:
            cursor.center=i.pos
            master.nu()
        elif i.type==pygame.QUIT:
            master.run=False
        if master.active:
            master.scene.event_handle(i)
            
    if master.need_update:
        master.draw(dis)
        if master.active:
            dis.blit(cursor_image, (cursor.centerx-xoffset, cursor.centery-yoffset))
        pygame.display.flip()
    clock.tick(master.fps)
        
        
