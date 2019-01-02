import pygame
import math
import random
import person
pygame.font.init()

def blBlit(surface, image, loc):
    rect = image.get_rect()
    bl = rect.bottomleft
    topleft = (loc[0] - bl[0], loc[1] - bl[1])
    surface.blit(image,topleft)
    return surface
    
def round(float, epsilon = 10**-7):
    trunc = int(float)
    if abs(trunc - float) < epsilon:
        return trunc
    if abs(trunc+1-float) < epsilon:
        return trunc+1
    return float
    
def getRandomCatName():
    names = ("Mila","Rocko""Motley","Poptart","Claudia","OdaMae","Kurma")
    names += ("Einstien","Avonlea","Cletis","SirMeowsAlot","Teejay","Hugo")
    names += ("CoCo","Boots","BobbyBoucher","Leon","Phoebe","Smagma","Dog")
    names += ("Chesty","Walnut","Pax","Leon","Cheech","Katy","Tedward")
    names += ("StalkingCat","Haze","Fudge","Cheeks","Starjumper","Lola","Gus")
    names += ("Boress","Zador","Wrath","Smirnoff","Oreo","Cheyanne","Hobbes")
    names += ("Scrumpy","OompaLoompa","Astro","OneWisker","Reaper")
    names += ("JungleShredder","MrFuzzbutt","Gizmo")
    name = random.sample(names,1 )
    return name.pop()

class Button(pygame.sprite.Sprite):
    
    def __init__(self,x1,y1,width,length, title, font,color):
        pygame.sprite.Sprite.__init__(self) #construct the parent component
        self.x1 = x1
        self.y1 = y1
        self.width = width
        self.length = length
        self.title = title
        self.image = pygame.Surface((width,length))
        self.image.fill(color)
        titleimg = font.render(title,False,(0,0,0))
        x = self.image.get_width()/2 - titleimg.get_width()/2
        y = self.image.get_height()/2 - titleimg.get_height()/2
        self.image.blit(titleimg,(x,y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x1,y1)
        
    def action(self,restaurant,mode):
        return restaurant, mode
    
class buildButton(Button):
    def action(self,restaurant,mode):
        return restaurant, "build"
        
class cancelButton(Button):
    def action(self,restaurant,mode):
        return restaurant, "normal"
        
class chairButton(Button):
    def action(self,restaurant,mode):
        return restaurant, "chair"
        
class counterButton(Button):
    def action(self,restaurant,mode):
        return restaurant, "counter"
        
        
class tableButton(Button):
    def action(self,restaurant,mode):
        return restaurant, "table"
    
class stoveButton(Button):
    def action(self,restaurant,mode):
        return restaurant, "stove"
        
class wallButton(Button):
    def action(self,restaurant,mode):
        return restaurant, "wall"
        
class entranceButton(Button):
    def action(self,restaurant,mode):
        return restaurant, "entrance"
        
class deleteButton(Button):
    def action(self,restaurant,mode):
        return restaurant,"delete"
        
class nextDayButton(Button):
    def action(self,restaurant,mode):
        return restaurant, "nextDay"
        
class hireButton(Button):
    def action(self, restaurant, mode):
        return restaurant, "hire"
        
class fireButton(Button):
    def action(self,restaurant,mode):
        return restaurant,"fire"
        
class waiterButton(Button):
    def action(self,restaurant,mode):
        restaurant.onBreak.add(person.Waiter(restaurant))
        return restaurant,"normal"
        
class chefButton(Button):
    def action(self,restaurant,mode):
        restaurant.onBreak.add(person.Chef(restaurant))
        return restaurant,"normal"
        