import pygame
import effects
import assets_list
from random import randint, shuffle
from tools import *

#137 261
class TargetConstructor:
    def __init__(self, name, framedata, scale=1):
        image, rect=load_image(name, scale=scale)
        self.framedata=framedata
        self.frames=AnimatedSprite.strip_sheet(None, image, rect, framedata)

    def construct(self, cost, cords):
        return Target(cost, cords, self.get_frame(cost), self.framedata)

    def moving_construct(self, cost, cords, speed, xmin, xmax):
        return MovingTarget(cost, cords, self.get_frame(cost), self.framedata, speed, xmin, xmax)

    def get_frame(self, cost):
        frame=None
        if cost==10:
            frame=self.frames[4+randint(0,15)]
        elif cost==1:
            frame=self.frames[self.framedata[2]]
        elif cost==11:
            frame=self.frames[randint(0,3)]
        else:
            frame=self.frames[6-cost*4-randint(0,3)]
        return frame
        

class Target(pygame.sprite.Sprite):
    def __init__(self, cost, cords ,frame , framedata):
        super().__init__()
        self.rect=pygame.Rect(cords[0], cords[1],framedata[0],framedata[1])
        self.image=frame
        self.cost=cost
        self.used=False

class MovingTarget(pygame.sprite.Sprite):
    def __init__(self, cost, cords, frame, framedata, speed, xmin, xmax):
        super().__init__()
        self.rect=pygame.Rect(cords[0], cords[1],framedata[0],framedata[1])
        self.speed=speed
        self.xmax=xmax
        self.xmin=xmin
        self.image=frame
        self.cost=cost
        self.used=False

    def update(self):
        if self.rect.x>=self.xmax or self.rect.x<=self.xmin:
            self.speed=-self.speed
        if not self.used:
            self.rect.x=self.rect.x+self.speed

class Shooter:
    def __init__(self, controller):
        self.master=controller
        self.main = pygame.sprite.Group()
        self.FILES = assets_list.SHOOTER_FILES
        self.LAYOUT = assets_list.SHOOTER_LAYOUT
        self.ANIMATIONDATA = assets_list.SHOOTER_ANIMATIONDATA

        self.line_speed=1
        self.rounds=0
        self.cards_show_time=0
        self.card_speed=0

        self.effect=None
        
        self.bg = None
        self.bg_cords = self.LAYOUT["bg"]
        
        self.bush_image=load_image(self.FILES["bush"])[0]
        self.bush_cords=self.LAYOUT["bush"]

        self.shot_tr=[]
        self.score_counter = Counter(2, self.FILES["score"], self.LAYOUT["score"], self.ANIMATIONDATA["score"])

        self.goal_counter = Counter(2, self.FILES["goal"], self.LAYOUT["goal"], self.ANIMATIONDATA["goal"])

        self.timer_counter = Counter(1, self.FILES["timer"], self.LAYOUT["rounds"], self.ANIMATIONDATA["timer"])

        self.targets=pygame.sprite.Group()
        self.tr_constructor=TargetConstructor(self.FILES["target"], self.ANIMATIONDATA["target"])

        self.wounds=[]
        self.wound_image, self.wound_rect=load_image(self.FILES["wound"])
        
        self.timer_event1=pygame.event.Event(1,{})
        self.timer_event2=pygame.event.Event(2, {})
        self.reload_image = load_image(self.FILES["reload"])[0]
        self.reload_cords=self.LAYOUT["reload"]
        self.reload=False

        self.line=TimerLine(self.LAYOUT["line"], self.LAYOUT["line_max"], self.line_speed)

        self.draw=None
        self.event_handle=None

        self.game_reset()

    def draw_wounds(self, screen):
        for i in self.wounds:
            screen.blit(self.wound_image, i)

    def generate_situation(self):
            self.rounds=randint(1,3)
            cards=[]
            cards_cords=[]
            goal=self.goal_counter.get_number()
            while goal>11:
                rnd=randint(2,10)
                goal=goal-rnd
                cards.append(rnd)
                self.rounds=self.rounds+1
            if goal==1:
                cards.append(11)
            else:
                cards.append(goal)
            x=0
            for i in self.LAYOUT["normal_targets"]:
                x=i[0]+randint(0,50)
                while x<i[1]:
                    cards_cords.append((x, i[2]-self.ANIMATIONDATA["target"][1]))
                    x=x+self.ANIMATIONDATA["target"][0]+randint(0,50)
            x=len(cards_cords)-len(cards)+len(self.LAYOUT["moving_targets"])
            while x>0:
                cards.append(randint(2,11))
                x=x-1
            shuffle(cards)
            for i in self.LAYOUT["moving_targets"]:
                self.targets.add(self.tr_constructor.moving_construct(cards[0], (i[0]+randint(0,100), i[2]-self.ANIMATIONDATA["target"][1]), self.card_speed, i[0], i[1]))
                del cards[0]
            while cards!=[]:
                self.targets.add(self.tr_constructor.construct(cards[0], cards_cords[0]))
                del cards[0]
                del cards_cords[0]

        
    def draw_goal_screen(self, screen):
        screen.blit(self.bg, self.bg_cords)
        self.goal_counter.draw(screen)
        self.score_counter.draw(screen)
        self.timer_counter.draw(screen)
        self.master.cursor.center=(1000,1000)

    def event_handle_goal_screen(self, i):
        if i.type==pygame.KEYDOWN or i.type==pygame.MOUSEBUTTONDOWN:
            self.draw=self.draw_cards_show
            self.event_handle=self.event_handle_cards_show
            
            self.bg=load_image(self.FILES["cards_show"])[0]
            pygame.time.set_timer(self.timer_event1, 1000)
            pygame.time.set_timer(self.timer_event2, 10)
            
            self.timer_counter.set_number(self.cards_show_time)
            self.timer_counter.set_pos(self.LAYOUT["timer"])
            self.effect=effects.effect_2(self.master.SCREEN_SIZE[0], self.master.SCREEN_SIZE[1])
            self.master.cutscene(60)
                
            
    def draw_cards_show(self, screen):
        screen.blit(self.bg, self.bg_cords)
        self.targets.draw(screen)
        screen.blit(self.bush_image, self.bush_cords)
        self.timer_counter.draw(screen)
        self.master.cursor.center=(1000, 1000)

    def event_handle_cards_show(self, i):
        if i.type==1:
            if self.timer_counter.get_number()==0:
                self.line.reset()
                self.bg=load_image(self.FILES["shooting"])[0]
                self.draw=self.draw_shooting
                self.event_handle=self.event_handle_shooting
                self.master.nu()
            else:
                self.timer_counter.sub(1)
            self.master.nu()
        elif i.type==2:
            self.targets.update()
            self.master.nu()
            
        elif i.type==pygame.MOUSEBUTTONDOWN or i.type==pygame.KEYDOWN:
            self.line.reset()
            self.bg=load_image(self.FILES["shooting"])[0]
            self.draw=self.draw_shooting
            self.event_handle=self.event_handle_shooting
            self.master.nu()
            

    def draw_shooting(self, screen):
        screen.blit(self.bg, self.bg_cords)
        self.line.draw(screen)
        self.draw_wounds(screen)
        if self.reload:
            screen.blit(self.reload_image, self.reload_cords)

        #self.targets.draw(screen) #remove
        
    def event_handle_shooting(self, i):
        if i.type==pygame.MOUSEBUTTONDOWN:
            if not self.reload and self.rounds>0:
                self.wounds.append((i.pos[0], i.pos[1]))
                self.reload=True
                pygame.time.set_timer(self.timer_event1, 500)
                self.rounds=self.rounds-1
                collieded=[]
                for i in self.targets.sprites():
                    if self.master.cursor.colliderect(i.rect) and not i.used:
                        self.shot_tr.append(i.cost)
                        i.used=True
                        
        elif i.type==2:
            self.line.sub()
            self.targets.update()
            self.master.nu()
            
        elif i.type==1:
            self.reload=False
            pygame.time.set_timer(self.timer_event1, 0)

        elif i.type==pygame.KEYDOWN:
            self.rounds=0
            
        if self.line.is_end() or self.rounds<=0:
            self.shot_tr.sort()
            s=0
            for i in self.shot_tr:
                if i==11:
                    if s+i>self.goal_counter.get_number():
                        s=s+1
                    else:
                        s=s+i
                else:
                    s=s+i
                        
            add_score=1-(abs(s-self.goal_counter.get_number())/self.goal_counter.get_number())
            print(add_score)
            if s!=self.goal_counter.get_number():
                add_score=add_score-0.15
            self.score_counter.add(int(add_score*5))
            pygame.time.set_timer(self.timer_event2, 0)
            self.bg=load_image(self.FILES["cards_show"])[0]
            self.draw=self.draw_results
            self.event_handle=self.event_handle_results
            self.effect=effects.effect_3(self.master.SCREEN_SIZE[0], self.master.SCREEN_SIZE[1])
            self.master.cutscene(60)

    def draw_results(self, screen):
        screen.blit(self.bg, self.bg_cords)
        self.targets.draw(screen)
        self.draw_wounds(screen)
        screen.blit(self.bush_image, self.bush_cords)
        pygame.time.set_timer(self.timer_event1, 3000)

    def event_handle_results(self, i):
        if i.type==1 or i.type==pygame.KEYDOWN or i.type==pygame.MOUSEBUTTONDOWN:
            self.effect=effects.effect_1(150)
            self.master.cutscene(60)
            self.next_round()
        

    def is_end(self):
        return self.effect.is_end()

    def draw_cutscene(self, screen):
        self.effect.draw(screen)

    def next_round(self):
        self.targets.empty()
        self.wounds=[]
        self.goal_counter.set_number(randint(15,30))
        if self.cards_show_time>=5:
            self.cards_show_time=self.cards_show_time-1
        self.card_speed=int(self.card_speed+(5/self.card_speed))
        self.bg = load_image(self.FILES["goal_screen"])[0]
        self.generate_situation()
        self.timer_counter.set_number(self.rounds)
        self.timer_counter.set_pos(self.LAYOUT["rounds"])
        self.draw=self.draw_goal_screen
        self.event_handle=self.event_handle_goal_screen
        self.master.nu()

        
    
    def game_reset(self):
        self.targets.empty()
        self.wounds=[]
        self.goal_counter.set_number(randint(15,30))
        self.score_counter.set_number(0)
        self.cards_show_time=9
        self.card_speed=2
        self.bg = load_image(self.FILES["goal_screen"])[0]
        self.generate_situation()
        self.timer_counter.set_number(self.rounds)
        self.draw=self.draw_goal_screen
        self.event_handle=self.event_handle_goal_screen
        self.master.nu()
