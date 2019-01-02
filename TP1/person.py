import random
import copy
import pygame
import obstacles

class Person(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #construct the parent component
        self.image = pygame.Surface((27,27))
        self.image.fill((0,255,100))

        self.rect = self.image.get_rect() #loads the rect from the image

        #set the position, direction, and speed of the ball
        self.rect.topleft = (13, 13)
        self.x = 0
        self.y = 0
        self.dir_x = 0
        self.dir_y = 0
        self.speed = 30
        self.internalClock = 0

    def update(self, restaurant):
        oldRect = copy.deepcopy(self.rect)
        self.x += self.dir_x
        self.y += self.dir_y
        self.rect.topleft = (self.x*self.speed+13,self.y*self.speed+13)
        if not self.checkBounds(restaurant):
            self.rect = oldRect
            self.x -= self.dir_x
            self.y -= self.dir_y
            print("reset")
            
        if not(restaurant.board[self.y][self.x] == 0 or isinstance(restaurant.board[self.y][self.x], obstacles.Chair)):
            self.rect = oldRect
            self.x -= self.dir_x
            self.y -= self.dir_y
            print("reset")
            
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
                            
                            print("adding",self.path, (i,j))
                            path += [(i,j)]
                            print(path, currLoc)
                            visited += [newLoc]
                            solution = recurse(newLoc,dest,board,visited,path)
                            if solution:
                                return solution
                        self.path = self.path[-1:]
                        visted = visited[-1:]
                return False
                
        self.path = recurse((self.x,self.y),(x,y),board, visited, self.path)
        print(x,y, self.x, self.y, self.path)
        
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
        
class Employee(Person): pass
    
class Customer(Person):
    def __init__(self, restaurant):
        Person.__init__(self)
        self.x = restaurant.entrance[0]
        self.y = restaurant.entrance[1]
        self.image.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        
    def update(self, restaurant):
        if len(self.path) != 0:
            self.dir_y, self.dir_x = self.path[0]
            self.path.pop(0)
        Person.update(self, restaurant)
            
        self.dir_x = 0
        self.dir_y = 0
        