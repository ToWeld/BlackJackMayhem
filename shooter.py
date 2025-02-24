import pygame
import assets_list
from random import randint, shuffle
from tools import *

#137 261

class Target(AnimatedSprite):
    def __init__(self, cost, image, rect, cords, framedata, *groups):
        pygame.sprite.Sprite.__init__(self)
        self.rect=pygame.Rect(cords[0], cords[1],framedata[0],framedata[1])
        self.curr_frame=0
        self.frame_count=framedata[2]
        self.frames=[]
        self.strip_sheet(image, rect, framedata)
        self.set_frame(0)
        if cost==10:
            self.set_frame(4+randint(0,15))
        elif cost==1:
            self.set_frame(53)
        elif cost==11:
            self.set_frame(randint(0,3))
        else:
            self.set_frame(6-cost*4-randint(0,3))
        self.cost=cost

class Shooter:
    def __init__(self, controller):
        self.master=controller
        self.main = pygame.sprite.Group()
        self.FILES = assets_list.SHOOTER_FILES
        self.LAYOUT = assets_list.SHOOTER_LAYOUT
        self.ANIMATIONDATA = assets_list.SHOOTER_ANIMATIONDATA
        
        self.bg = load_image(self.FILES["goal_screen"])[0]
        self.bg_cords = self.LAYOUT["goal_screen"]

        self.score_counter = Counter(2, self.FILES["digit"], self.LAYOUT["score"], self.ANIMATIONDATA["digit"])
        self.score=0

        self.goal_counter = Counter(2, self.FILES["digit"], self.LAYOUT["goal"], self.ANIMATIONDATA["digit"])
        self.goal=0

        self.timer_counter = Counter(1, self.FILES["digit"], self.LAYOUT["timer_counter"], self.ANIMATIONDATA["digit"])

        self.target_image, self.target_rect=load_image(self.FILES["target"])
        self.targets=pygame.sprite.Group()

        self.timer_event=pygame.event.Event(1,{})

        self.line=TimerLine((0,0), (900,50), 1)

        self.draw=None
        self.event_handle=None

        self.game_reset()

        
    def draw_goal_screen(self, screen):
        screen.blit(self.bg, self.bg_cords)
        self.goal_counter.draw(screen)
        self.score_counter.draw(screen)
        self.master.cursor.rect.centerx=1000
        self.master.cursor.rect.centery=1000

    def event_handle_goal_screen(self, i):
        if i.type==pygame.KEYDOWN or i.type==pygame.MOUSEBUTTONDOWN:
            cards=[]
            goal=randint(1,5)
            while goal!=0:
                cards.append(randint(2,11))
                goal=goal-1
            goal=self.goal
            while goal>11:
                rnd=randint(2,10)
                goal=goal-rnd
                cards.append(rnd)
            if goal==1:
                cards.append(11)
            else:
                cards.append(goal)

            shuffle(cards)
            in_row=len(cards)//2
            space=(self.master.SCREEN_SIZE[0]-(self.ANIMATIONDATA["target"][0]*in_row))//(in_row+1)
            self.targets.empty()
            for i in range(in_row):
                self.targets.add(Target(cards[0], self.target_image, self.target_rect, (i*self.ANIMATIONDATA["target"][0]+space*(i+1), self.LAYOUT["targets_row"][0]), self.ANIMATIONDATA["target"]))
                del cards[0]
            in_row=len(cards)
            space=(self.master.SCREEN_SIZE[0]-(self.ANIMATIONDATA["target"][0]*in_row))//(in_row+1)
            for i in range(in_row):
                self.targets.add(Target(cards[0], self.target_image, self.target_rect, (i*self.ANIMATIONDATA["target"][0]+space*(i+1), self.LAYOUT["targets_row"][1]), self.ANIMATIONDATA["target"]))
                del cards[0]

            self.draw=self.draw_cards_show
            self.event_handle=self.event_handle_cards_show
            self.bg=load_image(self.FILES["cards_show"])[0]
            pygame.time.set_timer(self.timer_event, 1000)
            self.timer_counter.set_number(5)
            self.master.nu()
                
            
    def draw_cards_show(self, screen):
        screen.blit(self.bg, self.bg_cords)
        self.targets.draw(screen)
        self.timer_counter.draw(screen)
        self.master.cursor.rect.centerx=1000
        self.master.cursor.rect.centery=1000

    def event_handle_cards_show(self, i):
        if i.type==1:
            if self.timer_counter.get_number()==0:
                print(1)
            else:
                self.timer_counter.sub(1)
            self.master.nu()
    
    def game_reset(self):
        self.score=0
        self.goal=randint(15,30)
        self.score_counter.set_number(0)
        self.goal_counter.set_number(self.goal)
        self.draw=self.draw_goal_screen
        self.event_handle=self.event_handle_goal_screen
        self.bg = load_image(self.FILES["goal_screen"])[0]
        self.master.nu()
