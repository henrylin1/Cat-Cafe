"""
by: Henry Lin

_________     ________________ _________     _____  ______________________
\_   ___ \   /  _  \__    ___/ \_   ___ \   /  _  \ \_   _____/\_   _____/
/    \  \/  /  /_\  \|    |    /    \  \/  /  /_\  \ |    __)   |    __)_ 
\     \____/    |    \    |    \     \____/    |    \|     \    |        \
 \______  /\____|__  /____|     \______  /\____|__  /\___  /   /_______  /
        \/         \/                  \/         \/     \/            \/ 

An incremental game that promotes active play. Takes place in a cafe setting. 
Build and upgrade a restaurant and progress from a small cafe to a 
world-famous restaurant.
"""
import pygame
from pygame.locals import * 
import copy
import random
import person
import obstacles
import miscFunctions


####
#Functions
####

def allLeave(restaurant):   #closes the restaurant
    
    for i in range(len(restaurant.board)):  #clear all food
        for j in range(len(restaurant.board)):
            if isinstance(restaurant.board[i][j], obstacles.Chair):
                restaurant.board[i][j].occupied = False
            if isinstance(restaurant.board[i][j], obstacles.Stove):
                restaurant.board[i][j].occupied = False
                restaurant.board[i][j].food = None
            if isinstance(restaurant.board[i][j], obstacles.Table):
                restaurant.board[i][j].food = None
                restaurant.board[i][j].occupied = False
            if isinstance(restaurant.board[i][j], obstacles.Counter):
                restaurant.board[i][j].food = None
    
    for customer in restaurant.customers.sprites(): #clear all customers
        customer.leaving = True
        customer.going = False
        if customer.sitting == True:
            restaurant.board[customer.y][customer.x].occupied = False
            customer.sitting = False
        if (customer.x,customer.y) == restaurant.entrance:
            restaurant.customers.remove(customer)
            
    for employee in restaurant.employees.sprites(): #clear all employees
        employee.leave(restaurant)
        if (employee.x,employee.y) == restaurant.entrance:
            employee.leaving = False
            employee.image = employee.downList[0]
            restaurant.onBreak.add(employee)    #remove from restaurant, but
            restaurant.employees.remove(employee)#keep saved
    
    if len(restaurant.employees.sprites()) == 0:    #if everyone has left
        if len(restaurant.customers.sprites()) == 0:
            
            for employee in restaurant.onBreak.sprites():
                restaurant.money -= employee.cost   #pay salary
                if restaurant.money < 0:
                    restaurant.money = 0
            return True
    return False
    

####
#Initialize game objects
####
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1024, 768))

background = pygame.Surface(screen.get_size()).convert()
background.fill((57, 86, 124))
screen.blit(background, (0,0))

restaurant = obstacles.Restaurant(15,15)
for i in range(5,10):
    restaurant.board[3][i] = obstacles.Table()
for i in range(5,10):
    restaurant.board[4][i] = obstacles.Chair()

restaurant.board[14][14] = obstacles.Stove()
restaurant.stoveLocList += [(14,14)]

restaurant.board[13][14] = obstacles.Stove()
restaurant.stoveLocList += [(14,13)]

restaurant.board[14][12] = obstacles.Counter()
restaurant.counterLocList += [(12,14)]
restaurant.board[13][12] = obstacles.Counter()
restaurant.counterLocList += [(12,13)]

super = person.SuperEmployee(restaurant)
waiter = person.Waiter(restaurant)
chef = person.Chef(restaurant)
restaurant.onBreak.add(super, waiter, chef) 

pygame.mixer.init()
pygame.mixer.music.load("audio\\background.wav")
#pygame.mixer.music.set_volume(1) #to adjust the volume
pygame.mixer.music.play() #to play the loaded song, -1 means repeat



####
#Game states
####

def startGameLoop():
    clock = pygame.time.Clock()
    keep_going = True
    catSize = (200,200)
    down1 = pygame.image.load("img/cat2/2.png") #walking cat in start
    down1 = pygame.transform.scale(down1,catSize)
    down2 = pygame.image.load("img/cat2/3.png")
    down2 = pygame.transform.scale(down2,catSize)
    down3 = pygame.image.load("img/cat2/4.png")
    down3 = pygame.transform.scale(down3,catSize)
    down4 = pygame.image.load("img/cat2/5.png")
    down4 = pygame.transform.scale(down4,catSize)
    downList = [down1,down2,down3,down4,down3,down2]
    background = pygame.image.load("img/background.png")
    font = pygame.font.Font('DTM-Sans.otf', 120)
    title = font.render("CAT CAFE", False, (255,255,255))
    font = pygame.font.Font('DTM-Sans.otf', 60)
    helper = font.render("Press any key to continue", False, (255,255,255))
    timer = 0
    counter = 0 
    while keep_going:
        
        clock.tick(10)
        timer += 1
        if timer >= 600:    #to make cat walk
            timer = 0
        counter = timer%6
        
        for ev in pygame.event.get():   #stop game if quit
            if ev.type == QUIT:
                return False
            elif ev.type == MOUSEBUTTONDOWN or ev.type == KEYDOWN: 
                return True     #move on if user input
        

        screen.blit(background,(0,0))
        screen.blit(downList[counter],(1024/2-catSize[0]/2, 100))  #centered
        screen.blit(title,(1024/2-title.get_width()/2,300))
        screen.blit(helper,(1024/2-helper.get_width()/2,500))  
        
        pygame.display.flip()
        
def tutorialGameLoop():
    clock = pygame.time.Clock()
    keep_going = True
    page = 0
    font = pygame.font.Font('DTM-Sans.otf', 60)
    helper = font.render("Press any key to continue", False, (255,255,255))
    timer = 0
    help = False
    while keep_going:
        clock.tick(10)
        timer += 1
        if timer >= 500:    #continue helper pop up if too long
            help = True
        
        for ev in pygame.event.get():
            if ev.type == QUIT:
                return False
            elif ev.type == MOUSEBUTTONDOWN or ev.type == KEYDOWN: 
                timer = 0
                page += 1   #rotate pages if user input
                if page >= 3:
                    return True
        
        image = pygame.image.load("img/tutorial/"+str(page)+".png")
        screen.blit(image,(0,0))
        
        
        if help == True:
            screen.blit(helper,(1024/2-helper.get_width()/2,500))
            
        pygame.display.flip()

def mainGameLoop(restaurant):
    clock = pygame.time.Clock()
    keep_going = True
    timer = 0
    customerCounter = 0
    board = pygame.image.load("img/board.png")
    while keep_going:
        timer += 1
        customerCounter += 1
        clock.tick(30)
        #add employees back if they were on break
        if len(restaurant.onBreak.sprites()) != 0 and timer < 1440:
            restaurant.employees = restaurant.onBreak.copy()
            restaurant.onBreak.empty()
            for employee in restaurant.employees.sprites():
                employee.x, employee.y = restaurant.entrance
                
        #end day at 9:00pm
        if timer >= 1440:
            timer -= 1
            left = allLeave(restaurant)
            if left:
                keep_going = False

        #customers only come in at specific times
        if timer > 200 and timer < 1200 and customerCounter > restaurant.customerRate:
            restaurant.addCustomer()
            customerCounter = 0
        
        #customer action
        for customer in restaurant.customers.sprites():
            response = customer.action(restaurant)  #perform ai action
            if response == 'leave':     #change customer spawn rate based on-
                if customer.satisfaction > 75:#customer satisfaction
                    restaurant.customerRate *= 0.98
                    if restaurant.customerRate < 1:
                        restaurant.customerRate == 1
                elif customer.satisfaction < 50:
                    restaurant.customerRate += 0.1
                restaurant.customers.remove(customer)
                
        #employee action
        for employee in restaurant.employees.sprites():
            employee.action(restaurant)
            
            
        for ev in pygame.event.get():
            if ev.type == QUIT:
                return False

        keys = pygame.key.get_pressed()     #commands for supercat 
        if not super.inMotion:
            if keys[pygame.K_UP]:
                super.dir_y = -1
            elif keys[pygame.K_DOWN]:
                super.dir_y = 1
            elif keys[pygame.K_LEFT]:
                super.dir_x = -1
            elif keys[pygame.K_RIGHT]:
                super.dir_x = 1
            elif keys[pygame.K_c]:
                super.cook(restaurant)
            elif keys[pygame.K_t]:
                super.takeFood(restaurant)
            elif keys[pygame.K_p]:
                super.placeFood(restaurant)
                    
        #graphics
        screen.blit(background, (0,0))
        screen.blit(board,(480,10))
        restaurant.employees.clear(screen, background)
        restaurant.employees.update(restaurant)
        restaurant.customers.clear(screen, background)
        restaurant.customers.update(restaurant)
        restaurant.update()
        screen.blit(restaurant.image,restaurant.rect.topleft)
        screen.blit(restaurant.displayInfo(timer),(10,480))
        screen.blit(restaurant.showEmployees(),restaurant.showEmpLoc)
        pygame.display.flip()
    return True
            

def editGameLoop(restaurant):
    clock = pygame.time.Clock()
    keep_going = True
    board = pygame.image.load("img/board.png")
    myfont = pygame.font.Font('DTM-Sans.otf', 30)
    
    #menu buttons

    buildButton = miscFunctions.buildButton(530,75, 400, 50, "Build", myfont, (66,134,244))
    deleteButton = miscFunctions.deleteButton(530,150, 400, 50, "Delete", myfont, (66,134,244))
    hireButton = miscFunctions.hireButton(530,225, 400, 50, "Hire", myfont, (66,134,244))
    fireButton = miscFunctions.fireButton(530,300, 400, 50, "Fire", myfont, (66,134,244))
    nextDayButton = miscFunctions.nextDayButton(530,375, 400, 50, "Next Day", myfont, (66,134,244))
    
    #build menu buttons, has its own function because needs to reinitialize
    #every time a purchase is made to update the costs
    cancelButton = miscFunctions.cancelButton(530, 25, 400, 50, "Cancel", myfont, (66,134,244))
    def initBuild():
        chairButton = miscFunctions.chairButton(530,85, 400, 50, "Chair: $"+str(obstacles.Chair.cost), myfont, (66,134,244))
        counterButton = miscFunctions.counterButton(530,145, 400, 50, "Counter: $"+str(obstacles.Counter.cost), myfont, (66,134,244))
        tableButton = miscFunctions.tableButton(530,205, 400, 50, "Table: $"+str(obstacles.Table.cost), myfont, (66,134,244))
        stoveButton = miscFunctions.stoveButton(530,265, 400, 50, "Stove: $"+str(obstacles.Stove.cost), myfont, (66,134,244))
        wallButton = miscFunctions.wallButton(530,325, 400, 50, "Wall: $"+str(obstacles.Wall.cost), myfont, (66,134,244))
        entranceButton = miscFunctions.entranceButton(530,385, 400, 50, "Entrance: $1000", myfont, (66,134,244))
        buildButtons = pygame.sprite.Group(cancelButton,chairButton,counterButton,tableButton,stoveButton,wallButton,entranceButton)
        return buildButtons
        
    buildButtons = initBuild()
    
    #hire menu buttons
    chefButton = miscFunctions.chefButton(530,200, 400, 50, "Chef: $"+str(person.Chef.cost)+"/day", myfont, (66,134,244))
    waiterButton = miscFunctions.waiterButton(530,300, 400, 50, "Waiter: $"+str(person.Waiter.cost)+"/day", myfont, (66,134,244))
    
    buttonList = pygame.sprite.Group()
    mode = "normal"
    buildObject = None
    
    while keep_going:
        screen.blit(background,(0,0))
        screen.blit(board,(480,10))
        for ev in pygame.event.get():
            if ev.type == QUIT:
                return False
            elif ev.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttonList:   #check if buttons were pressed
                    if button != None and button.rect.collidepoint(pos):
                        ret = button.action(restaurant, mode)
                        restaurant, mode = ret[0], ret[1]
                    
                    #decide on action based on current mode
                    if mode == "place" or mode == "delete" or mode == "placeEntrance":
                        
                        #find relative coordinates on restaurant
                        x = int((pos[0] - restaurant.rect.topleft[0])/restaurant.sizex)
                        y = int((pos[1] - restaurant.rect.topleft[1])/restaurant.sizey)
                        if x >= 0 and x < len(restaurant.board[0]):
                            if y >= 0 and y < len(restaurant.board):
                                
                                if mode == "place":
                                    if restaurant.board[y][x] == 0:
                                        restaurant.board[y][x] = buildObject
                                        restaurant.money -= buildObject.cost
                                        
                                        #next purchase is more expensive
                                        obstacleType = type(buildObject)
                                        obstacleType.cost += obstacleType.increment
                                        
                                        #add relevant objects to lists, these
                                        #objects are often used
                                        if isinstance(buildObject,obstacles.Counter):
                                            restaurant.counterLocList += [(x,y)]
                                        elif isinstance(buildObject,obstacles.Stove):
                                            restaurant.stoveLocList += [(x,y)]
                                            
                                        buildObject = None
                                        
                                        #reinitialize price indicators
                                        buildButtons = initBuild()
                                        mode = "build"

                                        
                                elif mode == "placeEntrance":
                                    if restaurant.board[y][x] == 0:
                                        
                                        #entrance must be at edge of restaurant
                                        if y == 0 or y == len(restaurant.board)-1 or x == 0 or x == len(restaurant.board[0])-1:
                                            if board[y][x] == 0:
                                                restaurant.entrance = (x,y)
                                                mode = "build"
                                
                                elif mode == "delete":
                                    if restaurant.board[y][x] != 0:
                                        object = restaurant.board[y][x]
                                        
                                        #remove relevant objects from lists
                                        if isinstance(object,obstacles.Counter):
                                            restaurant.counterLocList.remove((x,y))
                                        elif isinstance(object,obstacles.Stove):
                                            restaurant.stoveLocList.remove((x,y))
                                            
                                        restaurant.board[y][x] = 0
                    
                    if mode == "fire":
                        #find coords relative to employees
                        clickArea = restaurant.showEmpSize+restaurant.spacing
                        x = int((pos[0]-restaurant.showEmpLoc[0])/clickArea)
                        y = int((pos[1]-restaurant.showEmpLoc[1])/clickArea)
                        
                        #convert to clicking on a specific employee
                        spriteLoc = y*6+x
                        if spriteLoc > 0 and spriteLoc < len(restaurant.onBreak.sprites()):
                            sprite = restaurant.onBreak.sprites()[spriteLoc]
                            restaurant.onBreak.remove(sprite)
                            mode == "normal"
                        
        #updates buttons based on modes, as well with graphics
        if mode == "normal":
            buttonList = pygame.sprite.Group(buildButton,deleteButton,hireButton,fireButton,nextDayButton)
            
        if mode == "build":
            buttonList = buildButtons

            
        if mode == "chair":
            if restaurant.money < obstacles.Chair.cost:
                mode = "build"
            else:
                buildObject = obstacles.Chair()
                mode = "place"
                
        if mode == "counter":
            if restaurant.money < obstacles.Counter.cost:
                mode = "build"
            else:
                buildObject = obstacles.Counter()
                mode = "place"
        if mode == "table":
            if restaurant.money < obstacles.Table.cost:
                mode = "build"
            else:
                buildObject = obstacles.Table()
                mode = "place"
        if mode == "stove":
            if restaurant.money < obstacles.Stove.cost:
                mode = "build"
            else:
                buildObject = obstacles.Stove()
                mode = "place"
                
        if mode == "wall":
            if restaurant.money < obstacles.Wall.cost:
                mode = "build"
            else:
                buildObject = obstacles.Wall()
                mode = "place"
        
        if mode == "entrance":
            if restaurant.money < 1000:
                mode = "build"
            else:
                mode = "placeEntrance"
                buttonList = pygame.sprite.Group(cancelButton)
        
        if mode == "place":
            buttonList = pygame.sprite.Group(cancelButton)
            
        if mode == "delete":
            buttonList = pygame.sprite.Group(cancelButton)
            
        if mode == "hire":
            buttonList = pygame.sprite.Group(cancelButton,waiterButton,chefButton)
            
        if mode == "fire":
            buttonList = pygame.sprite.Group(cancelButton)
            text = myfont.render("Click an Employee!! ",False,(255,255,255))
            screen.blit(text, (530, 400))
            
        #graphics
        buttonList.clear(screen, background)
        buttonList.update(restaurant)
        buttonList.draw(screen)
        screen.blit(restaurant.displayInfo(0),(10,480))
        screen.blit(restaurant.showEmployees(),restaurant.showEmpLoc)
        
        #lines for restaurant in build, place, or delete mode
        if mode == "build" or mode == "place" or mode == "placeEntrance" or mode == "delete":
            restaurant.show_tiles = True
        else:
            restaurant.show_tiles = False
        

        restaurant.update()
        screen.blit(restaurant.image,restaurant.rect.topleft)   #just restaurant
        pygame.display.flip()
        
        #move on 
        if mode == "nextDay":
            keep_going = False
        
    #end of while loop
    return True
    
keep_going = startGameLoop()
if keep_going:
    keep_going = tutorialGameLoop()

while keep_going:
    keep_going = editGameLoop(restaurant)
    restaurant.day += 1
    if not keep_going:
        break
    keep_going = mainGameLoop(restaurant)

pygame.quit()
    