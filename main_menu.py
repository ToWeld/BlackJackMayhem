import pygame
import assets_list
import effects
import shooter
from tools import *

class MainMenu:
    def __init__(self, controller):
        self.master = controller

        self.main = pygame.sprite.Group()
        FILES = assets_list.MAIN_MENU_FILES
        LAYOUT = assets_list.MAIN_MENU_LAYOUT
        ANIMATIONDATA = assets_list.MAIN_MENU_ANIMATIONDATA
        SFX = assets_list.MAIN_MENU_SFX
        self.window = AnimatedSprite(FILES["window"], LAYOUT["window"], ANIMATIONDATA["window"])
        self.main.add(self.window)

        self.entrance_rect = pygame.Rect(LAYOUT["entrance_rect"])

        self.bg = load_image(FILES["background"])[0]
        self.bg_cords = LAYOUT["background"]

        self.walking_sound = load_sound(SFX["walking"])
        self.shot_sound = load_sound(SFX["shot"])
        self.shot_sound.set_volume(0.3)

        self.collide_rect_ratio = pygame.sprite.collide_rect_ratio(0.9)

        self.frame=0

        self.draw=self.draw_normal

    def draw_normal(self, screen):
        screen.blit(self.bg, self.bg_cords)
        self.main.draw(screen)

    def draw_cutscene(self, screen):
        self.draw_normal(screen)
        self.frame=self.frame+1
        self.window.next_frame(0,self.window.frame_count-1)
        if self.frame==self.window.frame_count+1:
            pygame.time.delay(500)
            self.master.terminate()

    def event_handle(self, i):
        if i.type == pygame.MOUSEBUTTONDOWN:
            if self.entrance_rect.collidepoint(i.pos):
                self.walking_sound.play()
                self.master.need_update = True
                self.master.fps = 90
                self.master.transition(effects.effect_1(150), shooter.Shooter(self.master))

            elif self.collide_rect_ratio(self.master.cursor, self.window):
                self.shot_sound.play()
                self.draw=self.draw_cutscene
                self.master.cutscene(30)

    def is_end(self):
        return False
