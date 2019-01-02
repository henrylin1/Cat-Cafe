""" 
Sprite version using a Group
"""
import pygame
from pygame.locals import * 
import copy
import random
import person
import obstacles
pygame.init()




        
screen = pygame.display.set_mode((600, 600))
employee = person.Employee()
employee_group = pygame.sprite.Group(employee) #Even though it is only a group of 1, for now

background = pygame.Surface(screen.get_size()).convert()
background.fill((255, 255, 255))
screen.blit(background, (0,0))

restaurant = obstacles.Restaurant(15,15)
restaurant.board[3][5] = obstacles.Table()
restaurant.board[3][6] = obstacles.Table()
restaurant.board[3][7] = obstacles.Table()
restaurant.board[4][5] = obstacles.Chair()
restaurant.board[2][10] = obstacles.Chair()
restaurant.board[4][7] = obstacles.Chair()

customer1 = person.Customer(restaurant)
customer2 = person.Customer(restaurant)
chairLoc1 = restaurant.findChair()
chairLoc2 = restaurant.findChair()
customer1.badFindPath(chairLoc1[0],chairLoc1[1],restaurant.board)
customer2.badFindPath(chairLoc2[0],chairLoc2[1],restaurant.board)
customer2.path = [(0,0)] + customer2.path
customer_group = pygame.sprite.Group(customer1, customer2)
clock = pygame.time.Clock()
keep_going = True
while keep_going:
    clock.tick(5)
    for ev in pygame.event.get():
        if ev.type == QUIT:
            keep_going = False
        elif ev.type == KEYDOWN:
            #Ability to increase/decrease speed
            if ev.key == K_UP:
                employee.dir_y = -1
            elif ev.key == K_DOWN:
                employee.dir_y = 1
            elif ev.key == K_LEFT:
                employee.dir_x = -1
            elif ev.key == K_RIGHT:
                employee.dir_x = 1
                
                
    employee_group.clear(screen, background)
    employee_group.update(restaurant)
    customer_group.clear(screen, background)
    customer_group.update(restaurant)
    screen.blit(restaurant.image,restaurant.rect.topleft)
    restaurant.displayBoard()
    employee_group.draw(screen)
    customer_group.draw(screen)
    pygame.display.flip()
    
pygame.quit()
    