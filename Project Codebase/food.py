import pygame
import copy
import random
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 8)
class Food:
    def __init__(self, amount, cost, type, time, img):
        self.type = type
        self.amount = amount
        self.amntImg = myfont.render(str(self.amount), False, (0, 0, 0))
        self.origImage = copy.copy(img)
        self.image = copy.copy(img)
        self.cost = cost
        self.time = time
        if self.amount != 1:
            self.image.blit(self.amntImg,(0,0))
        
    def getPortion(self):
        self.amount -= 1
        self.amntImg = myfont.render(str(self.amount), False, (0, 0, 0))
        self.image = copy.copy(self.origImage)
        if self.amount != 1:
            self.image.blit(self.amntImg,(1,0))
            
        if self.amount <=0:
            return Food(1,self.cost,self.type, self.time,self.origImage), False
        return Food(1,self.cost,self.type, self.time,self.origImage), True
        
    def addPortion(self,amnt):
        self.amount += amnt
        self.amntImg = myfont.render(str(self.amount), False, (0, 0, 0))
        self.image = copy.copy(self.origImage)
        if self.amount != 1:
            self.image.blit(self.amntImg,(1,0))
            
def getRandomFood():
    beer = Food(2,10,"beer",100,pygame.image.load("img/food/beer.png"))
    bread = Food(4,7,"bread",150,pygame.image.load("img/food/bread.png"))
    chicken = Food(2,30,"chicken",200,pygame.image.load("img/food/chicken.png"))
    eggs = Food(1,15,"eggs",50,pygame.image.load("img/food/eggs.png"))
    pretzel = Food(3,15,"pretzel",200,pygame.image.load("img/food/pretzel.png"))
    sushi = Food(1,40,"sushi",150,pygame.image.load("img/food/sushi.png"))
    foods = (beer,bread,chicken,eggs,pretzel,sushi)
    randfood = random.sample(foods,1)
    return randfood.pop()