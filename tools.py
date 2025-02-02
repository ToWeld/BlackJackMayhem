import os
import pygame

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

def load_image(name, colorkey=None, scale=1):
    try:
        fullname = os.path.join(data_dir, name)
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
    except Exception:
        print("Ошибка загрузки файла:", fullname)
        return

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    try:
        fullname = os.path.join(data_dir, name)
        sound = pygame.mixer.Sound(fullname)
    except Exception:
        print("Ошибка загрузки файла:", fullname)
        return

    return sound

class Sprite(pygame.sprite.Sprite):
    def __init__(self, name, cords, colorkey=None, scale=1):
        super().__init__()
        self.image, self.rect=load_image(name, colorkey=colorkey, scale=scale)
        self.rect.center=cords

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, name, cords, framedata, colorkey=None, scale=1):
        super().__init__()
        image, rect=load_image(name, colorkey=colorkey ,scale=scale)
        self.rect=pygame.Rect(cords[0], cords[1],framedata[0],framedata[1])
        self.curr_frame=0
        self.frame_count=framedata[2]
        self.frames=[]
        for i in range(int(rect.h/framedata[1])):
            for j in range(int(rect.w/framedata[0])):
                self.frames.append(image.subsurface(pygame.Rect(j*framedata[0], i*framedata[1], self.rect.w, self.rect.h)))
        self.set_frame(0)

    def set_frame(self, i):
        self.image=self.frames[i]

    def next_frame(self, start, end):
        if self.curr_frame>=end or self.curr_frame<start:
            self.curr_frame=start
            self.image=self.frames[start]
        else:
            self.curr_frame=self.curr_frame+1
            self.image=self.frames[self.curr_frame]
