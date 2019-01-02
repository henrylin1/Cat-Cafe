import random
import copy
import pygame
import obstacles
import pathfinding
import food
import miscFunctions

class Person(pygame.sprite.Sprite):
    def __init__(self, restaurant):
        pygame.sprite.Sprite.__init__(self) #construct the parent component
        self.image = pygame.image.load("img/cat1/1.png")
        self.image = pygame.transform.scale(self.image,(30, 30))

        self.rect = self.image.get_rect() #loads the rect from the image

        #set the position, direction, and speed of the person
        xLoc = restaurant.entrance[0]*restaurant.sizex + restaurant.margin
        yLoc = restaurant.entrance[1]*restaurant.sizey + restaurant.margin
        
        self.rect.topleft = (xLoc,yLoc)
        self.x = restaurant.entrance[0]
        self.y = restaurant.entrance[1]
        self.dir_x = 0
        self.dir_y = 0
        self.speed = 5
        self.internalClock = 0
        self.movementClock = 0
        self.food = None
        self.path = []
        self.inMotion = False
        self.spriteCounter = 0

    def update(self, restaurant):
        self.spriteCounter += 1
        if self.spriteCounter > 4:       #rotates 1, 2, 3, 4
            self.spriteCounter = 0
        #rotate sprites
        if self.dir_x == 1:
            self.imageList = self.rightList
        elif self.dir_x == -1:
            self.imageList = self.leftList
        elif self.dir_y == 1:
            self.imageList = self.downList
        elif self.dir_y == -1:
            self.imageList = self.upList
        else:
            self.spriteCounter = 0 #idling
        
        #face the table 
        if isinstance(self, Customer) and (self.eating or self.sitting) and self.tableLoc != None:
            relativeLoc = (self.x-self.tableLoc[0],self.y-self.tableLoc[1])
            if relativeLoc[0] == 1:
                self.imageList = self.leftList
            elif relativeLoc[0] == -1:
                self.imageList = self.rightList
            elif relativeLoc[1] == 1:
                self.imageList = self.upList
            elif relativeLoc[1] == -1:
                self.imageList = self.downList

        self.image = copy.copy(self.imageList[self.spriteCounter])
        
        #face the stove 
        if isinstance(self, Chef) and (self.cooking) and self.stoveLoc != None:
            relativeLoc = (self.x-self.stoveLoc[0],self.y-self.stoveLoc[1])
            if relativeLoc[0] == 1:
                self.imageList = self.leftList
            elif relativeLoc[0] == -1:
                self.imageList = self.rightList
            elif relativeLoc[1] == 1:
                self.imageList = self.upList
            elif relativeLoc[1] == -1:
                self.imageList = self.downList

        self.image = copy.copy(self.imageList[self.spriteCounter])
        
        #if is holding food
        
        if self.food != None:
            self.image = miscFunctions.blBlit(self.image, self.food.image, (0,30))
        
        if self.dir_y or self.dir_x: #if in motion
            self.inMotion = True
            goingy = self.y+self.dir_y
            goingx = self.x+self.dir_x
            if goingx >= len(restaurant.board[0]) or goingx < 0 or goingy >= len(restaurant.board) or goingy < 0:
                self.dir_y = 0
                self.dir_x = 0
                self.inMotion = False
            elif not(restaurant.board[goingy][goingx] == 0 or isinstance(restaurant.board[goingy][goingx], obstacles.Chair)):
                self.dir_y = 0
                self.dir_x = 0
                self.inMotion = False
                
            self.movementClock += 1
            newx = self.x+self.dir_x*self.movementClock/self.speed
            newy = self.y+self.dir_y*self.movementClock/self.speed
            self.rect.topleft = (newx*restaurant.sizex,newy*restaurant.sizey)
            if self.movementClock >= self.speed: #to complete movement
                self.movementClock = 0
                self.x += self.dir_x
                self.y += self.dir_y
                self.dir_x = 0
                self.dir_y = 0
                self.inMotion = False
        

        
    def badFindPath(self, x, y, board): #not used in game, but was initially
        self.path = []                  #going to implement, uses recursive 
        visited = [[self.x,self.y]]     #search going through every possible move
        def recurse(currLoc,dest,board, visited, path):

            if currLoc == dest:
                return path
            else:
                for i in range(-1,2):
                    for j in range(-1,2):
                        newLoc = (currLoc[0]+i, currLoc[1]+j)
                        if newLoc[0] < 0 or newLoc[0] >= len(board):
                            continue
                        if newLoc[1] < 0 or newLoc[1] >= len(board[0]):
                            continue
                        if (board[newLoc[0]][newLoc[1]] == 0 or isinstance(board[newLoc[0]][newLoc[1]], obstacles.Chair)) and newLoc not in visited:
                            
                            path += [(i,j)]
                            visited += [newLoc]
                            solution = recurse(newLoc,dest,board,visited,path)
                            if solution:
                                return solution
                        self.path = self.path[-1:]
                        visted = visited[-1:]
                return False
                
        self.path = recurse((self.x,self.y),(x,y),board, visited, self.path)
        
    def goodFindPath(self, x, y, board):  #in pathfinding.py
        self.path = pathfinding.findPath(board,(self.x,self.y),(x,y))
        
    def checkBounds(self, restaurant):  #makes sure no one walks off screen
        if self.rect.left < restaurant.rect.left:
            return False
        elif self.rect.top < restaurant.rect.top:
            return False
        if self.rect.right > restaurant.rect.right:
            return False
        elif self.rect.bottom > restaurant.rect.bottom:
            return False
        return True
        
    def checkCollisions(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def isNear(self, restaurant, nearType): #if person is near a specific object
        for i in range(-1,2):
            for j in range(-1,2):
                if self.x + i > 0 and self.x + i < len(restaurant.board):
                    if self.y + j > 0 and self.y + j < len(restaurant.board[0]):
                        if (i != 0 and j ==0) or (j != 0 and i == 0):
                            near = restaurant.board[self.y+j][self.x+i]
                            if type(near) == nearType:
                                return (self.x+i, self.y+j)
        return False, False
        
####
#Employee Cats
####

class Employee(Person):
    
    def __init__(self, restaurant):
        Person.__init__(self,restaurant)
        self.leaving = False
        self.name = miscFunctions.getRandomCatName()
        
    def takeFood(self, restaurant):
        if self.food != None:
            return
        loc = self.isNear(restaurant, obstacles.Stove)
        if loc[0]:
            food = restaurant.board[loc[1]][loc[0]].takeFood()
            if food != None:
                self.food = food
                return
                
        loc = self.isNear(restaurant, obstacles.Counter)
        if loc[0]:
            food = restaurant.board[loc[1]][loc[0]].takeFood()
            if food != None:
                self.food = food
                
    def cook(self, restaurant):
        loc = self.isNear(restaurant,obstacles.Stove)
        if loc[0]:
            restaurant.board[loc[1]][loc[0]].cook(self)
            
    def placeFood(self, restaurant):
        loc = self.isNear(restaurant, obstacles.Counter)
        if loc[0] == False:
            loc = self.isNear(restaurant, obstacles.Table)
        if loc[0]:
            if self.food != None:
                restaurant.board[loc[1]][loc[0]].placeFood(self.food)
                self.food = None
                
    def leave(self, restaurant):
        self.food = None
        if self.inMotion:
            return
            
        if self.leaving == False:
            self.path = pathfinding.findPath(restaurant.board,(self.x,self.y),restaurant.entrance)
        self.leaving = True
    

class SuperEmployee(Employee):  #aka the player
    
    cost = 0
    
    def __init__(self, restaurant):
        Employee.__init__(self, restaurant)
        downidle = pygame.image.load("img/cat2/1.png")
        down1 = pygame.image.load("img/cat2/2.png")
        down2 = pygame.image.load("img/cat2/3.png")
        down3 = pygame.image.load("img/cat2/4.png")
        down4 = pygame.image.load("img/cat2/5.png")
        upidle = pygame.image.load("img/cat2/6.png")
        up1 = pygame.image.load("img/cat2/7.png")
        up2 = pygame.image.load("img/cat2/8.png")
        up3 = pygame.image.load("img/cat2/9.png")
        up4 = pygame.image.load("img/cat2/10.png")
        leftidle = pygame.image.load("img/cat2/11.png")
        left1 = pygame.image.load("img/cat2/12.png")
        left2 = pygame.image.load("img/cat2/13.png")
        left3 = pygame.image.load("img/cat2/14.png")
        left4 = pygame.image.load("img/cat2/15.png")
        rightidle = pygame.transform.flip(leftidle,True,False)
        right1 = pygame.transform.flip(left1,True,False)
        right2 = pygame.transform.flip(left2,True,False)
        right3 = pygame.transform.flip(left3,True,False)
        right4 = pygame.transform.flip(left4,True,False)
        
        self.downList = [downidle,down1,down2,down3,down4]
        self.upList = [upidle,up1,up2,up3,up4]
        self.leftList = [leftidle,left1,left2,left3,left4]
        self.rightList = [rightidle,right1,right2,right3,right4]
        self.image = self.downList[0]
        self.imageList = self.downList
        self.spriteCounter = 0
        self.recipe = food.getRandomFood()
        
    def __repr__(self):
        return "Supercat "
    
    def action(self,restaurant):
        pass


class Waiter(Employee):
    
    cost = 15
    
    def __init__(self, restaurant):
        Employee.__init__(self, restaurant)
        
        #graphic files
        
        downidle = pygame.image.load("img/cat4/1.png")
        down1 = pygame.image.load("img/cat4/2.png")
        down2 = pygame.image.load("img/cat4/3.png")
        down3 = pygame.image.load("img/cat4/4.png")
        down4 = pygame.image.load("img/cat4/5.png")
        upidle = pygame.image.load("img/cat4/6.png")
        up1 = pygame.image.load("img/cat4/7.png")
        up2 = pygame.image.load("img/cat4/8.png")
        up3 = pygame.image.load("img/cat4/9.png")
        up4 = pygame.image.load("img/cat4/10.png")
        leftidle = pygame.image.load("img/cat4/11.png")
        left1 = pygame.image.load("img/cat4/12.png")
        left2 = pygame.image.load("img/cat4/13.png")
        left3 = pygame.image.load("img/cat4/14.png")
        left4 = pygame.image.load("img/cat4/15.png")
        rightidle = pygame.transform.flip(leftidle,True,False)
        right1 = pygame.transform.flip(left1,True,False)
        right2 = pygame.transform.flip(left2,True,False)
        right3 = pygame.transform.flip(left3,True,False)
        right4 = pygame.transform.flip(left4,True,False)
        
        self.downList = [downidle,down1,down2,down3,down4]
        self.upList = [upidle,up1,up2,up3,up4]
        self.leftList = [leftidle,left1,left2,left3,left4]
        self.rightList = [rightidle,right1,right2,right3,right4]
        self.image = self.downList[0]
        self.imageList = self.downList
        self.spriteCounter = 0
        self.going = False
        self.serving = None
        self.serve = False
        
    def __repr__(self):
        return "Waiter"

    def update(self, restaurant):
        if len(self.path) != 0 and self.dir_x == 0 and self.dir_y == 0:
            self.dir_x, self.dir_y = self.path[0]

            self.path.pop(0)
            
        Person.update(self, restaurant)

    def leave(self,restaurant):
        self.going = False
        self.serving = None
        self.serve = False
        Employee.leave(self, restaurant)

    def action(self,restaurant):
        if self.inMotion:   #in motion, do not perfom actions
            return
            
        if self.leaving:    #leaving, do not perform actions
            if len(self.path) == 0:
                return True
            return
            
        if not self.serving:   #find customer to serve
            for customer in restaurant.customers.sprites(): 
                if customer.sitting == True and customer.waiter == None:
                    self.serving = customer
                    customer.waiter = True
                    self.getFood = True
                    break
                    
        if self.serving and self.serving.leaving == True:   #customer is leaving
            self.serving = None
            self.path = []
        
        if self.serving:    
            if self.food == None:    #getting food
                if self.going != True:    
                    found = False
                    counterLocList = copy.deepcopy(restaurant.counterLocList)
                    while not found:
                        
                        if len(counterLocList) == 0:
                            found = True
                            break
                        #pick a random counter to look for food
                        j,i = random.sample(counterLocList,1).pop()
                        counterLocList.remove((j,i))
                        
                        #path to counter if it has food
                        if restaurant.board[i][j].food != None:
                            self.path = pathfinding.findPathClose(restaurant.board,(self.x,self.y),(j,i))
                            found = True
                            self.going = True
                            
            elif self.food and self.serve == False: #already has food
                self.going = True

        #go to customer and serve food
        if len(self.path) == 0 and self.serving and self.going == True:
            self.takeFood(restaurant)
            self.going = False
            self.getFood = False
            self.serve = True       #serving food
            tableLoc = self.serving.isNear(restaurant, obstacles.Table)
            servingLoc = (2*tableLoc[0]-self.serving.x, 2*tableLoc[1]-self.serving.y)
            self.path = pathfinding.findPath(restaurant.board,(self.x,self.y),servingLoc)
        
        #at right location, place down food on table
        if len(self.path) == 0 and self.serve == True:
            self.serve = False
            self.placeFood(restaurant)
            self.serving = None
            self.going = False

        
class Chef(Employee):
    
    cost = 30
    
    def __init__(self, restaurant):
        Employee.__init__(self, restaurant)
        
        #graphic files
        
        downidle = pygame.image.load("img/cat3/1.png")
        down1 = pygame.image.load("img/cat3/2.png")
        down2 = pygame.image.load("img/cat3/3.png")
        down3 = pygame.image.load("img/cat3/4.png")
        down4 = pygame.image.load("img/cat3/5.png")
        upidle = pygame.image.load("img/cat3/6.png")
        up1 = pygame.image.load("img/cat3/7.png")
        up2 = pygame.image.load("img/cat3/8.png")
        up3 = pygame.image.load("img/cat3/9.png")
        up4 = pygame.image.load("img/cat3/10.png")
        leftidle = pygame.image.load("img/cat3/11.png")
        left1 = pygame.image.load("img/cat3/12.png")
        left2 = pygame.image.load("img/cat3/13.png")
        left3 = pygame.image.load("img/cat3/14.png")
        left4 = pygame.image.load("img/cat3/15.png")
        rightidle = pygame.transform.flip(leftidle,True,False)
        right1 = pygame.transform.flip(left1,True,False)
        right2 = pygame.transform.flip(left2,True,False)
        right3 = pygame.transform.flip(left3,True,False)
        right4 = pygame.transform.flip(left4,True,False)
        
        self.downList = [downidle,down1,down2,down3,down4]
        self.upList = [upidle,up1,up2,up3,up4]
        self.leftList = [leftidle,left1,left2,left3,left4]
        self.rightList = [rightidle,right1,right2,right3,right4]
        self.image = self.downList[0]
        self.imageList = self.downList
        self.spriteCounter = 0
        self.stove = None
        self.stoveLoc = None
        self.goToStove = False
        self.goingToStove = False
        self.cooking = False
        self.goToCounter = False
        self.recipe = food.getRandomFood()
        
    def __repr__(self):
        return "Chef"

    def update(self, restaurant):
        if len(self.path) != 0 and self.dir_x == 0 and self.dir_y == 0:
            self.dir_x, self.dir_y = self.path[0]
            self.path.pop(0)
            
        Person.update(self, restaurant)
            
    def leave(self,restaurant): #turn off stove and reset actions
        if self.stove:
            self.stove.occupied = False
        self.stove = None
        self.stoveLoc = None
        self.goToStove = False
        self.goingToStove = False
        self.cooking = False
        self.goToCounter = False
        Employee.leave(self, restaurant)
            
    def action(self, restaurant):
        
        if self.inMotion:   #in motion, perform no actions
            return
            
        if self.leaving:    #leaving, perform no actions
            if len(self.path) == 0:
                return True
            return
            
            
        if not self.stove:  #find a stove
            for stoveLoc in restaurant.stoveLocList:
                j,i = stoveLoc
                if restaurant.board[i][j].occupied == False:
                    self.stove = restaurant.board[i][j]
                    self.stoveLoc = (j,i)
                    restaurant.board[i][j].occupied = True
                    self.goToStove = True
                    break
        
        if self.goToStove:  #go to stove
            self.path = pathfinding.findPathClose(restaurant.board,(self.x,self.y),self.stoveLoc)
            self.goToStove = False
            self.goingToStove = True
        
        if len(self.path) == 0 and self.goingToStove == True:   #reach stove
            self.cooking = True
        
        if self.cooking:    #start cooking
            if self.stove.food:
                self.cooking = False
                self.takeFood(restaurant)
                self.goToCounter = True
                location = None
                #find counter to place food on
                counterLocList = copy.deepcopy(restaurant.counterLocList)
                bestPath = None
                for counterLoc in counterLocList:   #find closest counter
                    counter = restaurant.board[counterLoc[1]][counterLoc[0]]
                    if not (isinstance(counter.food, food.Food) and counter.food.type != self.food.type):   #make sure counter is placable
                        path = pathfinding.findPathClose(restaurant.board,(self.x,self.y),counterLoc)
                        length = len(path)
                        if bestPath == None or length < len(bestPath):
                            bestPath = path
                            
                if bestPath != None:
                    self.path = bestPath
                    
                        
            else:
                self.cook(restaurant)
            
        if len(self.path) == 0 and self.goToCounter == True:    #place food
            self.placeFood(restaurant)
            self.goToCounter = False
            self.goToStove = True
        
class Customer(Person):
    def __init__(self, restaurant):
        Person.__init__(self, restaurant)
        self.image.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        self.findingSeat = True
        self.going = False
        self.sitting = False
        self.eating = False
        self.eatCounter = 0
        self.leaving = False
        self.satisfaction = 100
        self.waiter = None
        self.tableLoc = None
        
        #graphics
        downidle = pygame.image.load("img/cat1/1.png")
        down1 = pygame.image.load("img/cat1/2.png")
        down2 = pygame.image.load("img/cat1/3.png")
        down3 = pygame.image.load("img/cat1/4.png")
        down4 = pygame.image.load("img/cat1/5.png")
        upidle = pygame.image.load("img/cat1/6.png")
        up1 = pygame.image.load("img/cat1/7.png")
        up2 = pygame.image.load("img/cat1/8.png")
        up3 = pygame.image.load("img/cat1/9.png")
        up4 = pygame.image.load("img/cat1/10.png")
        leftidle = pygame.image.load("img/cat1/11.png")
        left1 = pygame.image.load("img/cat1/12.png")
        left2 = pygame.image.load("img/cat1/13.png")
        left3 = pygame.image.load("img/cat1/14.png")
        left4 = pygame.image.load("img/cat1/15.png")
        rightidle = pygame.transform.flip(leftidle,True,False)
        right1 = pygame.transform.flip(left1,True,False)
        right2 = pygame.transform.flip(left2,True,False)
        right3 = pygame.transform.flip(left3,True,False)
        right4 = pygame.transform.flip(left4,True,False)
        
        self.downList = [downidle,down1,down2,down3,down4]
        self.upList = [upidle,up1,up2,up3,up4]
        self.leftList = [leftidle,left1,left2,left3,left4]
        self.rightList = [rightidle,right1,right2,right3,right4]
        
        self.imageList = self.downList
        self.spriteCounter = 0
        
    def update(self, restaurant):
        if len(self.path) != 0 and self.dir_x==0 and self.dir_y==0:
            self.dir_x, self.dir_y = self.path[0]
            self.path.pop(0)
        Person.update(self, restaurant)
            

        
    def action(self, restaurant):
        
        if self.inMotion:   #in motion, perform no actions
            return
        
        if self.leaving == True: 
            if self.going == False:
                self.goodFindPath(restaurant.entrance[0],restaurant.entrance[1],restaurant.board)
                self.going = True
            else:
                if len(self.path) == 0:
                    return "leave"
            
        elif self.satisfaction <= 0:    #customer is too unhappy, will leave
            self.leaving = True
            self.going = False
            if self.sitting == True:
                #seat and table are no longer occupied
                restaurant.board[self.y][self.x].occupied = False
                if self.tableLoc:
                    restaurant.board[self.tableLoc[1]][self.tableLoc[0]].occupied = False
                self.sitting = False
        
        #looking for a seat
        elif len(self.path) == 0 and self.findingSeat == True:
            location = restaurant.findChair()
            if location == False:
                self.satisfaction -= 5
            else:
                self.goodFindPath(location[0],location[1],restaurant.board)
                self.findingSeat = False
                self.going = True
        
        elif self.going == True:
            if len(self.path) == 0: #at seat
                self.going = False
                self.sitting = True
                self.satisfaction += 200
                
        elif self.sitting == True:  #at seat, locate table and waiting for food
            tableLoc = self.isNear(restaurant, obstacles.Table)
            if tableLoc != None and tableLoc[0] != False: 
                if not restaurant.board[tableLoc[1]][tableLoc[0]].occupied:
                    restaurant.board[tableLoc[1]][tableLoc[0]].occupied = True
                    self.tableLoc = tableLoc

            self.satisfaction -= 1
            
            #start eating if there is food
            if self.tableLoc and restaurant.board[self.tableLoc[1]][self.tableLoc[0]].food:
                self.eating = True
                self.sitting = False
                
        elif self.eating == True:
            self.eatCounter += 1
            
            #finish eating
            if self.eatCounter >= 200:
                self.leaving = True
                tableLoc = self.isNear(restaurant, obstacles.Table)
                restaurant.money += restaurant.board[tableLoc[1]][tableLoc[0]].food.cost
                restaurant.money += self.satisfaction / 100 * 5
                restaurant.money = int(restaurant.money * 100)/100
                restaurant.board[self.tableLoc[1]][self.tableLoc[0]].food = None
                restaurant.board[self.tableLoc[1]][self.tableLoc[0]].image.fill((150,75,0))
                restaurant.board[self.y][self.x].occupied = False
                restaurant.board[tableLoc[1]][tableLoc[0]].occupied = False
                self.eating = False
                
        
        
        