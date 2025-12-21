import pygame as py
import sys
screenx=1200
screeny=480
me1=None
wall1=None
level=1
angle0="右"
height0="上"
height1="上"
a=0
def events():
    global me1,wall1,level,height0,a
    for event in py.event.get():
        if event.type==py.QUIT:
            sys.exit()
        elif event.type==py.KEYDOWN:
            if event.key==py.K_UP or event.key==py.K_w:
                me1.jump0=True
            if event.key==py.K_LEFT or event.key==py.K_a:
                me1.left0=True
            if event.key==py.K_RIGHT or event.key==py.K_d:
                me1.right0=True
            if event.key==py.K_DOWN or event.key==py.K_s:
                height0="下"
                cs1.turn(angle0,height0)
                me1.new()
            if event.key==py.K_0:
                level+=1
                me1.rect.x=0
                me1.rect.y=300
                wall1.new()
                me1.x=me1.rect.x
                me1.y=me1.rect.y
        elif event.type==py.KEYUP:
            if event.key==py.K_LEFT or event.key==py.K_a:
                me1.left0=False
            if event.key==py.K_RIGHT or event.key==py.K_d:
                me1.right0=False
            if event.key==py.K_UP or event.key==py.K_w:
                me1.jump0=False
            if event.key==py.K_DOWN or event.key==py.K_s:
                height0="上"
                cs1.turn(angle0,height0)
                me1.new()
        if a==1:
            if height0=="上":
                height0="下"
            else:
                height0="上"
            me1.new()
            cs1.turn(angle0,height0)
    me1.left()
    me1.right()
    me1.move()
    me1.jump()
    me1.x=me1.rect.x
    me1.y=me1.rect.y
    if me1.x>1140:
        level+=1
        me1.rect.x=0
        me1.rect.y=300
        wall1.new()
    me1.rect.clamp_ip(py.Rect(0, 0, screenx, screeny))
    if py.sprite.collide_mask(me1,wall1):
        me1.g=0.1
        me1.back2()
class Me(py.sprite.Sprite):
    def __init__(self,x1,y1):
        super().__init__()
        self.x=x1
        self.y=y1
        self.image=py.image.load("碰撞上.png").convert_alpha()
        self.g=0.5
        self.v=0
        self.xv=0
        self.jump0=False
        self.left0=False
        self.right0=False
        self.on=False
        self.rect=self.image.get_rect()
        self.rect.topleft=(self.x,self.y)
        self.mask=py.mask.from_surface(self.image)
    def jump(self):
        self.rect.y+=1
        self.on=py.sprite.collide_mask(wall1,self)
        self.rect.y-=1
        if self.jump0 and self.on:
            self.g=-12
            self.on=False
    def left(self):
        global angle0,height0
        if self.left0:
            self.xv-=1
            cs1.turn("左",height0)
            angle0="左"
    def right(self):
        global angle0,height0
        if self.right0:
            self.xv+=1
            cs1.turn("右",height0)
            angle0="右"
    def move(self):
        self.xv=self.xv*0.9
        self.rect.x=self.rect.x+self.xv
        if py.sprite.collide_mask(wall1,self):
            self.back1()
        self.g=self.g+0.5
        self.rect.y=self.rect.y+self.g
        if py.sprite.collide_mask(wall1,self):
            self.back2()
        self.mask=py.mask.from_surface(self.image)
    def back1(self):
        for i in range(10):
            if py.sprite.collide_mask(wall1,self):
                self.rect.y-=1
        if py.sprite.collide_mask(wall1,self):
            self.rect.y+=10
            if self.jump0:
                if self.xv>0:
                    self.xv=-12
                else:
                    self.xv=12
                while py.sprite.collide_mask(wall1,self):
                    if (self.xv<0):
                        self.rect.x-=1
                    else:
                        self.rect.x+=1
                self.g=-10
            else:
                while py.sprite.collide_mask(wall1,self):
                    if (self.xv>0):
                        self.rect.x-=1
                    else:
                        self.rect.x+=1
                self.xv=0
    def back2(self):
        while py.sprite.collide_mask(wall1,self):
            if (self.g>0):
                self.rect.y-=1
                self.on=True
            else:
                self.rect.y+=1
        self.g=0
    def new(self):
        global height0,height1,a
        if height0!=height1:
            height1=height0
            if (height0=="上"):
                self.rect.y-=28
            else:
                self.rect.y+=26
            self.x=self.rect.x
            self.y=self.rect.y
        self.image=py.image.load(f"碰撞{height0}.png").convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.topleft=(self.x,self.y)
        self.mask=py.mask.from_surface(self.image)
        if py.sprite.collide_mask(wall1,self):
            a=1
            if height0=="上":
                height0="下"
                self.rect.y+=28
            else:
                height0="上"
                self.rect.y-=26
            self.x=self.rect.x
            self.y=self.rect.y
            self.image=py.image.load(f"碰撞{height0}.png").convert_alpha()
            self.rect=self.image.get_rect()
            self.rect.topleft=(self.x,self.y)
            self.mask=py.mask.from_surface(self.image)
            cs1.turn(angle0,height0)
        else:
            a=0
class Wall(py.sprite.Sprite):
    def __init__(self,x2,y2):
        super().__init__()
        self.x=x2
        self.y=y2
        self.image0=py.image.load("墙1.png").convert_alpha()
        self.image=py.transform.scale(self.image0,(1200,480))
        self.rect=self.image.get_rect()
        self.rect.topleft=(self.x,self.y)
        self.mask=py.mask.from_surface(self.image)
    def new(self):
        try:
            self.image0=py.image.load(f"墙{level}.png").convert_alpha()
            self.image=py.transform.scale(self.image0,(1200,480))
            self.rect=self.image.get_rect()
            self.rect.topleft=(self.x,self.y)
            self.mask=py.mask.from_surface(self.image)
        except:
            pass
class Cs:
    def __init__(self,x3,y3):
        self.x=x3
        self.y=y3
        self.image0=py.image.load("CS右上.png").convert_alpha()
        self.image=py.transform.scale(self.image0,(70,77))
    def turn(self,angle,height):
        self.image0=py.image.load(f"CS{angle}{height}.png").convert_alpha()
        if height=="上":
            self.image=py.transform.scale(self.image0,(70,77))
        else:
            self.image=py.transform.scale(self.image0,(70,39))
if __name__=="__main__":
    py.init()
    screen=py.display.set_mode((screenx,screeny))
    py.display.set_caption("优秀小跑酷")
    background=py.image.load("背景.png").convert()
    screen.blit(background,(0,0))
    me1=Me(0,300)
    wall1=Wall(0,0)
    cs1=Cs(0,300)
    clock=py.time.Clock()
    while True:
        clock.tick(60)
        screen.blit(background,(0,0))
        screen.blit(me1.image,(me1.x,me1.y))
        screen.blit(wall1.image,(wall1.x,wall1.y))
        if angle0=="右":
            if height0=="上":
                screen.blit(cs1.image,(me1.x-5,me1.y-15))
            else:
                screen.blit(cs1.image,(me1.x-5,me1.y-8))
        else:
            if height0=="上":
                screen.blit(cs1.image,(me1.x-11,me1.y-15))
            else:
                screen.blit(cs1.image,(me1.x-11,me1.y-8))
        py.display.update()
        events()