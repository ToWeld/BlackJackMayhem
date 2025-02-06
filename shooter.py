import pygame
import assets_list
from tools import *
class Shooter:
    def __init__(self, controller):
        self.main = pygame.sprite.Group()
        FILES = assets_list.SHOOTER_FILES
        LAYOUT = assets_list.SHOOTER_LAYOUT
        ANIMATIONDATA = assets_list.SHOOTER_ANIMATIONDATA
        self.bg = load_image(FILES["background"])[0]
        self.bg_cords = LAYOUT["background"]

        self.counter = Counter(2, FILES["digit"], (0, 0), ANIMATIONDATA["digit"])

    def draw(self, screen):
        screen.blit(self.bg, self.bg_cords)
        self.counter.draw(screen)

    def event_handle(self, i):
        if i.type == pygame.KEYDOWN:
            self.counter.add(1)