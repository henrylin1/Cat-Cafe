import pygame
import food
import person
import miscFunctions
import copy
pygame.font.init()
myfont = pygame.font.Font("DTM-Sans.otf", 30)

"""All obstacles have a cost and increment. Cost is the price to build the obstacle
increment is how much more expensive the next obstacle of the same type will be."""

class Wall(pygame.sprite.Sprite):   #simply a barrier, holds no function
    
    cost = 100
    increment = 0
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.regular = pygame.image.load("img/obstacles/wall.png")
        self.image = copy.copy(self.regular)
        self.rect = self.image.get_rect()
        self.food = None

class Counter(pygame.sprite.Sprite):    #to keep food on
    
    cost = 500
    increment = 100
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.regular = pygame.image.load("img/obstacles/counter.png")
        self.image = copy.copy(self.regular)
        self.rect = self.image.get_rect()
        self.food = None

    def placeFood(self, addingFood):

        #can stack food if same food type
        if isinstance(self.food, food.Food) and self.food.type == addingFood.type:
            self.food.addPortion(addingFood.amount)
        else:
            self.food = addingFood

            
    def takeFood(self): #make sure to have food before taking!!!
        if self.food == None:
            return None
        ret = self.food.getPortion()
        if not ret[1]:
            self.food = None
            
        return ret[0]
        
class Stove(pygame.sprite.Sprite):  #to make food on
    
    cost = 1000
    increment = 200
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.regular = pygame.image.load("img/obstacles/stove.png")
        self.image = copy.copy(self.regular)
        self.rect = self.image.get_rect()
        self.internalCounter = 0
        self.cooking = False
        self.food = None
        self.occupied = False

    def cook(self, chef):   #food made is based on recipe from chef
        self.internalCounter += 1
        self.cooking = copy.copy(chef.recipe)
        if self.internalCounter > self.cooking.time:
            self.food = self.cooking
            self.cooking = False
            self.internalCounter = 0
            
    def takeFood(self):
        ret = self.food
        self.food = None
        self.image = copy.copy(self.regular)
        return ret
        
class Table(pygame.sprite.Sprite):
    
    cost = 100
    increment = 10
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.regular = pygame.image.load("img/obstacles/table.png").convert_alpha()
        self.image = copy.copy(self.regular)
        self.rect = self.image.get_rect()
        self.food = None
        self.occupied = False

    def placeFood(self, food):
        self.food = food
        self.image = miscFunctions.blBlit(self.image, self.food.image, (0,30))
        
    def takeFood(self): #make sure to have food before taking!!!
        ret = self.food
        self.food = None
        return ret
        
class Chair(pygame.sprite.Sprite):
    
    cost = 50
    increment = 5
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.regular = pygame.image.load("img/obstacles/chair.png").convert_alpha()
        self.image = copy.copy(self.regular)
        self.rect = self.image.get_rect()
        self.occupied = False

class Restaurant(): #restaurant contains all relevant data structures
    
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.employees = pygame.sprite.Group()  #to keep employees in
        self.onBreak = pygame.sprite.Group()    #to keep employees on break in
        self.customers = pygame.sprite.Group()  #to keep customers in
        self.margin = 3                         #margin for whole restaurant
        self.sizex = 30                         #width of one block
        self.sizey = 30                         #length of one block
        self.customerTimer = 0                  #to spawn customers
        self.money = 500
        self.moneyIndicator = myfont.render("Money: "+str(self.money),False,(0,0,0))
        self.customerRate = 50                  #ticks per customer
        self.entrance = (5,0)                   #entrance location
        self.entranceMat = pygame.image.load("img/obstacles/mat.png")
        self.redrawBackground()     
        self.day = 0
        self.show_tiles = False
        self.showEmpLoc = (480,480) #location of show employees UI
        self.showEmpSize = 0 #size of employees in UI, simply initalize
        self.backgroundCol = (57, 86, 124)
        self.counterLocList = []
        self.stoveLocList = []
        self.board = [([0] * col) for row in range(row)]

        
    def redrawBackground(self):
        self.image = pygame.Surface((self.row*self.sizex+2*self.margin, self.col*self.sizey+2*self.margin))
        tile = pygame.image.load("img/obstacles/tile.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (10,10)
        for i in range(self.row):
            for j in range(self.col):
                self.image.blit(tile,(self.sizex*i+self.margin, self.sizey*j+self.margin))
    
    def update(self):
        self.redrawBackground()
        
        #entrance
        matLoc = (self.entrance[0]*self.sizex+self.margin,self.entrance[1]*self.sizey+self.margin)
        self.image.blit(self.entranceMat, matLoc)
        
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] != 0:
                    
                    #update image if there is food
                    if self.board[i][j] != None and not isinstance(self.board[i][j], Chair):
                        self.board[i][j].image = copy.copy(self.board[i][j].regular)
                        if isinstance(self.board[i][j].food, food.Food):
                            self.board[i][j].image = miscFunctions.blBlit(self.board[i][j].image, self.board[i][j].food.image,(0,30))
                    
                    
                    #position the image properly
                    bottomLeft = (j*self.sizex+self.margin,(i+1)*self.sizey+self.margin)
                    self.image = miscFunctions.blBlit(self.image, self.board[i][j].image,bottomLeft)
                    
                for character in (self.customers.sprites()+self.employees.sprites()):
                    if character.x == j and character.y == i:
                        self.image.blit(character.image,character.rect.topleft)

        if self.show_tiles == True:
            self.showTiles()
            
    def findChair(self):    #get empty chair for customer to sit on
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if isinstance(self.board[i][j], Chair) and self.board[i][j].occupied == False:
                    self.board[i][j].occupied = True
                    return (j,i)
        return False
                    
    def addCustomer(self):
        self.customers.add(person.Customer(self))
        
    def displayInfo(self, ticks):
        dimensions = (450,278)
        ret = pygame.Surface(dimensions)
        ret.fill(self.backgroundCol)
        scroll = pygame.image.load("img/scroll.png")
        ret.blit(scroll,(0,0))
        self.display = pygame.Surface((len(self.board)*self.sizex,300))
        moneyAmnt = "%.2f" %(self.money)
        moneyIndicator = myfont.render("Money: "+moneyAmnt,False,(0,0,0))
        moneyx = scroll.get_width()/2 - moneyIndicator.get_width()/2
        moneyy = scroll.get_height()/3 - moneyIndicator.get_height()/2
        ret.blit(moneyIndicator, (moneyx,moneyy))
        hours = 9 + int(ticks/120)
        minutes =10*int((ticks%120)/20)
        time = "day "+str(self.day)+", "+str(hours)+":"+str(minutes)
        timeIndicator = myfont.render(time,False,(0,0,0))
        timex = scroll.get_width()/2 - timeIndicator.get_width()/2
        timey = scroll.get_height()*2/3 - timeIndicator.get_height()/2
        ret.blit(timeIndicator, (timex,timey))
        return ret
        
    def showTiles(self):
        margin = 1
        for i in range(1,len(self.board)):
            left = self.margin
            top = self.margin + i*self.sizey
            width = len(self.board[0])*self.sizex
            height = margin
            pygame.draw.rect(self.image,(0,0,0),[left,top,width,height])
            
        for j in range(1,len(self.board[0])):
            left = self.margin+ j*self.sizex
            top = self.margin
            width = margin
            height = len(self.board)*self.sizey
            pygame.draw.rect(self.image,(0,0,0),[left,top,width,height])
            
    def showEmployees(self):
        dimensions = (534,278)
        ret = pygame.Surface(dimensions,pygame.SRCALPHA).convert_alpha()
        self.spacing = 10
        spacing = self.spacing
        self.showEmpSize = int((534-spacing)/6 - spacing)
        size = self.showEmpSize
        allEmployees = self.employees.sprites() + self.onBreak.sprites()
        for i in range (len(allEmployees)):
            row = i // 6
            col = i % 6
            employee = allEmployees[i]
            newImage = pygame.transform.scale(employee.image, (size, size))
            ret.blit(newImage, (spacing+col*(size+spacing),spacing+row*(size+spacing)))
            font = pygame.font.Font("DTM-Sans.otf", 10)
            title = font.render(str(employee),False,(255,255,255))
            name = font.render(employee.name,False,(255,255,255))
            titlex = size//2-title.get_width()//2
            namex = size//2-name.get_width()//2
            ret.blit(title, (spacing+titlex+col*(size+spacing),spacing+size+row*(size+spacing)))
            ret.blit(name, (spacing+namex+col*(size+spacing),spacing+size+10+row*(size+spacing)))
        return ret