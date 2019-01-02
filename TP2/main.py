""" 
Sprite version using a Group
"""
import pygame
from pygame.locals import * 
import copy
import random
import ML
import person
import obstacles
pygame.init()


screen = pygame.display.set_mode((600, 600))

background = pygame.Surface(screen.get_size()).convert()
background.fill((255, 255, 255))
screen.blit(background, (0,0))

restaurant = obstacles.Restaurant(15,15)
for i in range(3,12):
    restaurant.board[3][i] = obstacles.Table()
for i in range(3,12):
    restaurant.board[4][i] = obstacles.Chair()
    
for i in range(3,12):
    restaurant.board[6][i] = obstacles.Table()
for i in range(3,12):
    restaurant.board[7][i] = obstacles.Chair()


restaurant.board[14][14] = obstacles.Stove()

for i in range(10,15):
    restaurant.board[12][i] = obstacles.Counter()

super = person.SuperEmployee()
waiter = person.Waiter()
restaurant.employees.add(super, waiter) 

clock = pygame.time.Clock()
keep_going = True
while keep_going:
    clock.tick(5)
    restaurant.addCustomer()
    for customer in restaurant.customers.sprites():
        response = customer.action(restaurant)
        if response == 'leave':
            restaurant.customers.remove(customer)
            
    for ev in pygame.event.get():
        if ev.type == QUIT:
            keep_going = False
        elif ev.type == KEYDOWN:
            if ev.key == K_UP:
                super.dir_y = -1
            elif ev.key == K_DOWN:
                super.dir_y = 1
            elif ev.key == K_LEFT:
                super.dir_x = -1
            elif ev.key == K_RIGHT:
                super.dir_x = 1
            elif ev.key == K_c:
                super.cook(restaurant)
            elif ev.key == K_t:
                super.takeFood(restaurant)
            elif ev.key == K_p:
                super.placeFood(restaurant)
                
    screen.blit(background, (0,0))
    restaurant.employees.clear(screen, background)
    restaurant.employees.update(restaurant)
    restaurant.customers.clear(screen, background)
    restaurant.customers.update(restaurant)
    screen.blit(restaurant.image,restaurant.rect.topleft)
    screen.blit(restaurant.displayCash(),(300,500))
    restaurant.displayBoard()
    restaurant.customers.draw(screen)
    restaurant.employees.draw(screen)
    pygame.display.flip()
    
    for employee in restaurant.employees.sprites():
        employee.action(restaurant)
pygame.quit()
    