import pygame

class Stove(pygame.sprite.Sprite):
    def __init__(self):
        pass

class Table(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((27,27))
        self.image.fill((150,75,0))
        self.rect = self.image.get_rect()

        
class Chair(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill((150,75,0))
        self.rect = self.image.get_rect()
        self.occupied = False

class Restaurant():
    
    def __init__(self, row, col):
        self.margin = 3
        margin = 3
        self.image = pygame.Surface((row*30+margin, col*30+margin))
        self.rect = self.image.get_rect()
        self.rect.topleft = (10,10)
        self.size = 30
        size = 30
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
                    if isinstance(self.board[i][j], Table):
                        topLeft = (j*self.size+self.margin,i*self.size+self.margin)
                    self.image.blit(self.board[i][j].image,topLeft)
                    
    def findChair(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if isinstance(self.board[i][j], Chair) and self.board[i][j].occupied == False:
                    self.board[i][j].occupied = True
                    return (i,j)