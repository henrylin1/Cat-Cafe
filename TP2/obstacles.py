import pygame
import food
import person
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)

class Counter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((27,27))
        self.image.fill((150,150,150))
        self.rect = self.image.get_rect()
        self.food = None

    def placeFood(self, food):
        self.food = food
        self.image.blit(self.food.image, (10,10))
        
    def takeFood(self): #make sure to have food before taking!!!
        if self.food == None:
            return None
        ret = self.food.getPortion()
        self.image = pygame.Surface((27,27))
        self.image.fill((150,150,150))
        if not ret[1]:
            self.food = None
        else:
            self.image.blit(self.food.image,(10,10))
            
        return ret[0]
        
class Stove(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((27,27))
        self.image.fill((150,75,150))
        self.rect = self.image.get_rect()
        self.internalCounter = 0
        self.cooking = False
        self.food = None

    def cook(self):
        print("cookin", self.internalCounter)
        self.internalCounter += 1
        self.cooking = True
        if self.internalCounter > 10:
            self.food = food.Food(5,10)
            self.image.blit(self.food.image,(10,10))
            self.cooking = False
            self.internalCounter = 0
            
    def takeFood(self):
        ret = self.food
        self.food = None
        self.image = pygame.Surface((27,27))
        self.image.fill((150,75,150))
        return ret
        
class Table(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((27,27))
        self.image.fill((150,75,0))
        self.rect = self.image.get_rect()
        self.food = None

    def placeFood(self, food):
        self.food = food
        self.image.blit(self.food.image, (10,10))
        
    def takeFood(self): #make sure to have food before taking!!!
        ret = self.food
        self.food = None
        self.image = pygame.Surface((27,27))
        self.image.fill((150,75,150))
        return ret
        
class Chair(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill((150,75,0))
        self.rect = self.image.get_rect()
        self.occupied = False

class Restaurant():
    
    def __init__(self, row, col):
        self.employees = pygame.sprite.Group()
        self.customers = pygame.sprite.Group()
        self.margin = 3
        margin = 3
        self.image = pygame.Surface((row*30+margin, col*30+margin))
        self.rect = self.image.get_rect()
        self.rect.topleft = (10,10)
        self.size = 30
        size = 30
        self.customerTimer = 0
        self.money = 1000
        self.moneyIndicator = myfont.render("Money: "+str(self.money),False,(0,0,0))
        for i in range(row):
            for j in range(col):
                pygame.draw.rect(self.image,(0,200,200),[size*i+margin,
                                                           size*j+margin,
                                                           size-margin,
                                                           size-margin])
        
        self.entrance = (5,0)
        pygame.draw.rect(self.image,(255,255,255),[size*self.entrance[0]+margin,
                                                    size*self.entrance[1],
                                                    size-margin, margin*2])
        
        self.board = [([0] * col) for row in range(row)]
        
    def displayBoard(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] != 0:
                    if isinstance(self.board[i][j], Chair):
                        topLeft = (j*self.size+4*self.margin,i*self.size+4*self.margin)
                    else:
                        topLeft = (j*self.size+self.margin,i*self.size+self.margin)
                    self.image.blit(self.board[i][j].image,topLeft)
                    
                    
    def findChair(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if isinstance(self.board[i][j], Chair) and self.board[i][j].occupied == False:
                    self.board[i][j].occupied = True
                    print(j,i)
                    return (j,i)
        return False
                    
    def addCustomer(self):
        self.customerTimer += 1
        if self.customerTimer == 10:
            self.customers.add(person.Customer(self))
            self.customerTimer = 0
            
    def displayCash(self):
        self.moneyIndicator = myfont.render("Money: "+str(self.money),False,(0,0,0))
        return self.moneyIndicator