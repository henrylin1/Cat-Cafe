import pygame
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 8)
class Food:
    def __init__(self, amount, cost):
        self.amount = amount
        self.amntImg = myfont.render(str(self.amount), False, (0, 0, 0))
        self.image = pygame.Surface((10,10))
        self.image.fill((255,0,0))
        self.cost = cost
        if self.amount != 1:
            self.image.blit(self.amntImg,(0,0))
        
    def getPortion(self):
        self.amount -= 1
        print(self.amount)
        self.amntImg = myfont.render(str(self.amount), False, (0, 0, 0))
        self.image = pygame.Surface((10,10))
        self.image.fill((255,0,0))
        if self.amount != 1:
            self.image.blit(self.amntImg,(0,0))
            
        if self.amount <=0:
            return Food(1,self.cost), False
        return Food(1,self.cost), True