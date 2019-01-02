""" 
Sprite version using a Group
"""
import pygame
from pygame.locals import * 
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #construct the parent component
        self.image = pygame.image.load("sprite.png")
        self.image = pygame.transform.scale(self.image,(50, 50))

        self.rect = self.image.get_rect() #loads the rect from the image

        #set the position, direction, and speed of the ball
        self.rect.topleft = (50, 480)
        self.dir_x = 0
        self.dir_y = 0
        self.speed = 5	
        self.slow = False
        self.gravity = 0.2

    def update(self):
        
        if self.slow:
            self.slowdown()
            
        self.dir_y += self.gravity
        self.rect.move_ip(self.speed*self.dir_x, self.speed*self.dir_y)
        #Handle the walls by changing direction(s)
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right >= screen.get_width():
            self.rect.right = screen.get_width()
            
        if self.rect.top < 0 :
            self.rect.top = 0
        elif self.rect.bottom >= screen.get_height():
            self.rect.bottom = screen.get_height()
            
    def check_collision(self, surfaceList):
        self.gravity = 0.2
        for surface in surfaceList:
            print(self.rect.bottom, surface.rect.top)
            if self.rect.colliderect(surface.rect):
                print("collision occured")
                if self.rect.bottom > surface.rect.top:
                    print("yuppppp")
                    self.dir_y = 0
                    self.gravity = 0
        

    def move_left(self):
        self.dir_x = -1
        self.update()

    def move_right(self):
        self.dir_x = 1
        self.update()

    def move_up(self):
        self.dir_y = -3
        self.update()
        
    def slowdown(self):
        if self.dir_x > 0:
            self.dir_x -= 0.1
        if self.dir_x < 0:
            self.dir_x += 0.1

class Platform(pygame.sprite.Sprite):
    
    def __init__(self, x0, y0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 30))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x0, y0)
        
    def update(self):
        pass
        
screen = pygame.display.set_mode((640, 480))
player = Player()
pt1 = Platform(300, 200)
pt2 = Platform(50, 150)
pt3 = Platform(200, 350)
pt4 = Platform(50, 400)
platformList = [pt1,pt2,pt3,pt4]
ball_group = pygame.sprite.Group(player, pt1, pt2, pt3, pt4) #Even though it is only a group of 1, for now

background = pygame.Surface(screen.get_size()).convert()
background.fill((255, 255, 255))
screen.blit(background, (0,0))

clock = pygame.time.Clock()
keep_going = True
while keep_going:
    clock.tick(30)
    
    player.check_collision(platformList)
    
    for ev in pygame.event.get():
        if ev.type == QUIT:
            keep_going = False
        elif ev.type == KEYDOWN:
            player.slow = False
            #Ability to increase/decrease speed
            if ev.key == K_UP:
                player.move_up()
            elif ev.key == K_RIGHT:
                player.move_right()
            elif ev.key == K_LEFT:
                player.move_left() 
            
        elif ev.type == KEYUP:
            player.slow = True


    ball_group.clear(screen, background)
    ball_group.update()
    ball_group.draw(screen)
    pygame.display.flip()
    