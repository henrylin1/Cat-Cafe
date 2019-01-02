import random
import copy
import pygame
import obstacles
import pathfinding

class Person(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #construct the parent component
        self.image = pygame.image.load("sprite.png")
        self.image = pygame.transform.scale(self.image,(30, 30))

        self.rect = self.image.get_rect() #loads the rect from the image

        #set the position, direction, and speed of the ball
        self.rect.topleft = (13, 13)
        self.x = 0
        self.y = 0
        self.dir_x = 0
        self.dir_y = 0
        self.speed = 30
        self.internalClock = 0
        self.food = None
        self.path = []

    def update(self, restaurant):
        oldRect = copy.deepcopy(self.rect)
        self.x += self.dir_x
        self.y += self.dir_y
        self.rect.topleft = (self.x*self.speed+13,self.y*self.speed+13)
        if not self.checkBounds(restaurant):
            self.rect = oldRect
            self.x -= self.dir_x
            self.y -= self.dir_y
            
        if not(restaurant.board[self.y][self.x] == 0 or isinstance(restaurant.board[self.y][self.x], obstacles.Chair)):
            self.rect = oldRect
            self.x -= self.dir_x
            self.y -= self.dir_y
            
        self.dir_x = 0
        self.dir_y = 0
        
    def badFindPath(self, x, y, board):
        self.path = []
        visited = [[self.x,self.y]]
        def recurse(currLoc,dest,board, visited, path):

            if currLoc == dest:
                print("reached")
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
        print(x,y, self.x, self.y, self.path)
        
    def goodFindPath(self, x, y, board):
        self.path = pathfinding.findPath(board,(self.x,self.y),(x,y))
        
    def checkBounds(self, restaurant):
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
        
    def adjust_speed(self, delta):
        self.speed += delta

    def isNear(self, restaurant, nearType):
        for i in range(-1,2):
            for j in range(-1,2):
                if self.x + i > 0 and self.x + i < len(restaurant.board):
                    if self.y + j > 0 and self.y + j < len(restaurant.board[0]):
                        if (i != 0 and j ==0) or (j != 0 and i == 0):
                            near = restaurant.board[self.y+j][self.x+i]
                            if type(near) == nearType:
                                return (self.x+i, self.y+j)
        return False, False
        
class Employee(Person):
    
    def __init__(self):
        Person.__init__(self)
        
    def action(self,restaurant):
        pass
    

class SuperEmployee(Employee):

    def takeFood(self, restaurant):
        if self.food != None:
            return
        loc = self.isNear(restaurant, obstacles.Stove)
        if not (loc[0]):
            loc = self.isNear(restaurant, obstacles.Counter)
        if loc[0]:
            print("taking food")
            food = restaurant.board[loc[1]][loc[0]].takeFood()
            if food != None:
                self.food = food
                self.image.blit(self.food.image, (10,10))
            else:
                print("No food!")
            
    def cook(self, restaurant):
        loc = self.isNear(restaurant,obstacles.Stove)
        print(loc)
        if loc[0]:
            restaurant.board[loc[1]][loc[0]].cook()
            
    def placeFood(self, restaurant):
        loc = self.isNear(restaurant, obstacles.Counter)
        print(loc)
        if loc[0] == False:
            loc = self.isNear(restaurant, obstacles.Table)
        if loc[0]:
            if self.food != None:
                restaurant.board[loc[1]][loc[0]].food = self.food
                restaurant.board[loc[1]][loc[0]].image.blit(self.food.image, (10,10))
                self.food = None
                self.image = pygame.image.load("sprite.png")
                self.image = pygame.transform.scale(self.image,(30, 30))
            else:
                print("No food to place!")
        else:
            print("nothing nearby!")
            
class Waiter(Employee):
    
    def __init__(self):
        Employee.__init__(self)
    
    def takeFood(self, restaurant):
        if self.food != None:
            return
        loc = self.isNear(restaurant, obstacles.Stove)
        if not (loc[0]):
            loc = self.isNear(restaurant, obstacles.Counter)
        if loc[0]:
            print("taking food")
            food = restaurant.board[loc[1]][loc[0]].takeFood()
            if food != None:
                self.food = food
                self.image.blit(self.food.image, (10,10))
            else:
                print("No food!")
            
    def placeFood(self, restaurant):
        loc = self.isNear(restaurant, obstacles.Counter)
        print(loc)
        if loc[0] == False:
            loc = self.isNear(restaurant, obstacles.Table)
        if loc[0]:
            if self.food != None:
                restaurant.board[loc[1]][loc[0]].food = self.food
                restaurant.board[loc[1]][loc[0]].image.blit(self.food.image, (10,10))
                self.food = None
                self.image = pygame.image.load("sprite.png")
                self.image = pygame.transform.scale(self.image,(30, 30))
            else:
                print("No food to place!")
        else:
            print("nothing nearby!")
            
    def action(self,restaurant):
        pass
        
class Customer(Person):
    def __init__(self, restaurant):
        Person.__init__(self)
        self.x = restaurant.entrance[0]
        self.y = restaurant.entrance[1]
        self.image.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        self.findingSeat = True
        self.going = False
        self.sitting = False
        self.eating = False
        self.eatCounter = 0
        self.leaving = False
        self.satisfaction = 100
        
    def update(self, restaurant):
        if len(self.path) != 0:
            self.dir_x, self.dir_y = self.path[0]
            self.path.pop(0)
        Person.update(self, restaurant)
            
        self.dir_x = 0
        self.dir_y = 0
        
    def action(self, restaurant):
        
        if self.leaving == True: #probably has to be checked first!!
            if self.going == False:
                self.goodFindPath(restaurant.entrance[0],restaurant.entrance[1],restaurant.board)
                print(self.path, "le path")
                self.going = True
            else:
                print("im going")
                if len(self.path) == 0:
                    print("left!")
                    return "leave"
            
        elif self.satisfaction <= 0:
            self.leaving = True
            self.going = False
            if self.sitting == True:
                restaurant.board[self.y][self.x].occupied = False
                self.sitting = False
            print("me mad im leaving")
        
        elif len(self.path) == 0 and self.findingSeat == True:
            location = restaurant.findChair()
            if location == False:
                self.satisfaction -= 10
            else:
                self.goodFindPath(location[0],location[1],restaurant.board)
                self.findingSeat = False
                self.going = True
        
        elif self.going == True:
            if len(self.path) == 0:
                self.going = False
                self.sitting = True
                self.satisfaction += 50
                
        elif self.sitting == True:
            tableLoc = self.isNear(restaurant, obstacles.Table)
            self.satisfaction -= 1
            
            if tableLoc[0] and restaurant.board[tableLoc[1]][tableLoc[0]].food:
                self.eating = True
                self.sitting = False
                
        elif self.eating == True:
            self.eatCounter += 1
            if self.eatCounter >= 10:
                self.leaving = True
                tableLoc = self.isNear(restaurant, obstacles.Table)
                restaurant.money += restaurant.board[tableLoc[1]][tableLoc[0]].food.cost
                restaurant.money += self.satisfaction / 100 * 5
                restaurant.board[tableLoc[1]][tableLoc[0]].food = None
                restaurant.board[tableLoc[1]][tableLoc[0]].image.fill((150,75,0))
                restaurant.board[self.y][self.x].occupied = False
                self.eating = False
                
        
        
        