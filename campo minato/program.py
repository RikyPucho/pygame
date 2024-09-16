import random
import sys
import pygame
import numpy as np
import time

pygame.font.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("campo minato")
font = pygame.font.Font(None, 50)
BG = pygame.image.load("assets/game.png")
winBg = pygame.image.load("assets/win.png")
loseBg = pygame.image.load("assets/lose.png")
menuBg = pygame.image.load("assets/menu.png")
clock = pygame.time.Clock()
startTicks = pygame.time.get_ticks()
seconds = 0

fontGame = pygame.font.Font(None, 35)
fontDigit = pygame.font.Font(None, 50)
regameBox = pygame.Rect(750, 500, 120 , 60)
menuBox = pygame.Rect(750, 600, 120 , 60)
menuText = fontGame.render("Menu", True, (0,0,0))
regameText = fontGame.render("Rigioca", True , (0,0,0))

backgroundColor = (126,217,87)
cellColor = (87, 150, 60)


width = 22
nbombe = 99
flag = nbombe
boxWidth = (HEIGHT / width -4)
boxes = []

#bomba = 50
field = np.zeros(width**2)
#0 = scoperto 
#1 = coperto
#2 = bandierina
view = np.ones(width**2)


first = True

def generaCampo(xNo):
    global field
    field = np.zeros(width**2)
    for i in range(nbombe):
        while True:
            x = random.randint(0, width**2-1)
            #controllo che 
            # 1 non ci sia già una bomba
            # 2 non sia dove ha cliccato 
            # 3 non sia attorno a dove ha cliccato
            if field[x] == 0 and x != xNo and x != xNo-1 and x!= xNo+1 and x != xNo - width and x != xNo - width-1  and x != xNo - width+1  and x != xNo + width and x != xNo + width +1  and x != xNo + width -1:
                field[x] = 50
                break
            else:
                continue
    field = field.reshape(width, width)
    
    for i in range(width):
        for j in range(width):
            if field[i,j] >= 50:
                if j != 0:
                    field[i,j-1]+=1     #1,0
                    if i !=0:
                        field[i-1,j-1]+=1   #0, 0
                    if i != (width -1):
                        field[i+1,j-1]+=1   #2,0
                if i !=0:
                    field[i-1,j]+=1     #0,1
                    if j != (width -1):
                        field[i-1,j+1]+=1   #0,2
                if i != (width -1):
                    field[i+1,j]+=1     #2,1
                    if j != (width -1):
                        field[i+1,j+1]+=1   #2,2
                if j != (width -1):
                    field[i,j+1]+=1     #1,2

def checkWin():
    tempField = field.reshape(width**2)
    tempView = view.reshape(width**2)
    win = 0
    for i,x in enumerate(tempField):
        if x >= 50:
            if tempView[i] == 2:
                win +=1
    if win == nbombe and not 1 in view:
        return True
    else:
        return False

def checkZero(x):
    global view, field
    indi = getAttorno(x)
    for i in indi:
        if (i == x+1 and i %width ==0) or (i == x-1 and x % width == 0):
            pass
        elif (i == x+width+1 and i % width == 0) or (i == x-width+1 and i %width ==0) or (i==(x+width-1) and (i+1) % width==0) or (i == (x-width-1) and (i+1) %width ==0):
            pass
        elif view[i] != 0 and field[i] < 50:
            if field[i] != 0:
                view[i] = 0
            elif i != x+width+1 and i != x+width-1 and i != x-width-1 and i != x-width+1:
                view[i] = 0
                checkZero(i)

    

def getAttorno(x):
    indi = []    
    if x-width-1 >= 0:
        indi.append(x-width-1)
    if x-width >= 0:
        indi.append(x-width)
    if x-width+1 >= 0:
        indi.append(x-width+1)
    if x-1 >=0:
        indi.append(x-1)
    if x+1 < width**2:
        indi.append(x+1)
    if x+1 < width**2:
        indi.append(x+1)
    if x+width-1 < width**2:
        indi.append(x+width-1)
    if x+width < width**2:
        indi.append(x+width)
    if x+width+1 < width**2:
        indi.append(x+width+1)
    return indi



def start():
    global boxes, boxWidth, view,first, field, flag, startTicks
    startTicks = pygame.time.get_ticks()
    flag = nbombe
    first = True 
    view = np.ones(width**2)
    field = np.zeros(width**2)
    view = view.reshape(width, width)
    boxWidth = ((HEIGHT- (2*(width+1))) / width) 
    x = 2
    y = 2
    boxes = []
    for i in range(width**2):
        if i % width == 0 and i != 0:
            y+= 2 + boxWidth
            x = 2
        boxes.append(pygame.Rect(x,y, boxWidth, boxWidth))
        x+=2+boxWidth
def menu():
    global width, nbombe, font
    WIN.blit(menuBg, (0,0))

    easyBox = pygame.Rect((WIDTH-200)/2, 260,200,80)
    mediumBox = pygame.Rect((WIDTH-200)/2, 370,200,80)
    hardBox = pygame.Rect((WIDTH-200)/2, 500,200,80)
    fontMenu = pygame.font.Font(None, 50)
    easyText = fontMenu.render("Facile", True, (0,0,0))
    mediumText = fontMenu.render("Intermedio", True, (0,0,0))
    hardText = fontMenu.render("Difficile", True, (0,0,0))
    pygame.draw.rect(WIN, cellColor, easyBox, border_radius=15)
    pygame.draw.rect(WIN, (0,0,0), easyBox, border_radius=15, width=3)
    pygame.draw.rect(WIN, cellColor, mediumBox,border_radius=15)
    pygame.draw.rect(WIN, (0,0,0), mediumBox,border_radius=15, width=3)
    pygame.draw.rect(WIN, cellColor, hardBox, border_radius=15)
    pygame.draw.rect(WIN, (0,0,0), hardBox, border_radius=15, width=3)
    WIN.blit(easyText, (easyBox.left + 50, easyBox.top +25))
    WIN.blit(mediumText, (mediumBox.left+16, mediumBox.top+25))
    WIN.blit(hardText, (hardBox.left+35, hardBox.top+25))
    update()
    #facile width = 12 e nbombe = 25
    #intermedio width = 16 e nbombe = 40
    #difficile width = 22 e nbombe = 99   font 50

    play = False
    while not play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easyBox.collidepoint(event.pos):
                    width = 12
                    nbombe = 25
                    font = pygame.font.Font(None, 70)
                    start()
                    return
                if mediumBox.collidepoint(event.pos):
                    width = 16
                    nbombe = 40
                    font = pygame.font.Font(None, 60)
                    start()
                    return
                if hardBox.collidepoint(event.pos):
                    width = 22
                    nbombe = 99
                    font = pygame.font.Font(None, 50)
                    start()
                    return
        update()
    pygame.quit()
    sys.exit()

def end(win):
    if win:
        #win
        WIN.blit(winBg, (0,0))
    else:
        #perso
        WIN.blit(loseBg, (0,0))
    restart = False
    solution()
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menuBox.collidepoint(event.pos):
                    restart = True
                    menu()
                else:
                    restart = True
                    start()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        update()


def solution():
    global flag
    tempField = field.reshape(width**2)
    tempView = view.reshape(width**2)
    flag = 0
    for i, x in enumerate(tempField):
        if view[i] == 2:
            pygame.draw.rect(WIN, 'red', boxes[i])
        if x >=50:
            if view[i] == 2:
                pygame.draw.rect(WIN, 'blue', boxes[i])
                flag+=1
            else:
                pygame.draw.rect(WIN, 'black', boxes[i])
        elif tempView[i] == 0:

            #scoperto
            if x != 0:                
                pygame.draw.rect(WIN, backgroundColor, boxes[i])
                text = font.render(str(int(x)), True, (0,0,0))
                WIN.blit(text, (boxes[i].left, boxes[i].top))
            # else: 
            #     pygame.draw.rect(WIN, 'white', boxes[i])

        elif tempView[i] == 1:
            #coperto
            pygame.draw.rect(WIN, cellColor, boxes[i])
    drawGameInfo(end=True)
    update()

def drawGameInfo(end = False):
    pygame.draw.rect(WIN, cellColor, menuBox, border_radius=10)
    pygame.draw.rect(WIN, (0,0,0), menuBox, border_radius=10, width=3)
    WIN.blit(menuText, (menuBox.left+20, menuBox.top+15))
    pygame.draw.rect(WIN, cellColor, regameBox, border_radius= 10)
    pygame.draw.rect(WIN, (0,0,0), regameBox, border_radius= 10, width=3)
    WIN.blit(regameText, (regameBox.left+15, regameBox.top+15))
    timerText = fontDigit.render(str(seconds), True, (0,0,0))
    if not end:
        flagText = fontDigit.render(str(int(flag)), True, (0, 0,0))
        WIN.blit(flagText, (regameBox.left, 335))
        WIN.blit(timerText, (regameBox.left, 130))
    else:
        flagText = fontDigit.render(f"{flag}/{nbombe}", True, (0, 0,0))
        WIN.blit(flagText, (regameBox.left, 340))
        WIN.blit(timerText, (regameBox.left, 250))


def draw():
    WIN.blit(BG, (0,0))

    tempField = field.reshape(width**2)
    tempView = view.reshape(width**2)

    drawGameInfo()

    for i, x in enumerate(tempField):
        if tempView[i] == 1:
            #coperto
            pygame.draw.rect(WIN, (113,194,78), boxes[i])
        elif tempView[i] == 2:
            #bandierina
            pygame.draw.rect(WIN, 'red', boxes[i])
        else:
            #scoperto
            if x != 0:                
                pygame.draw.rect(WIN, backgroundColor, boxes[i])
                text = font.render(str(int(x)), True, (0,0,0))
                WIN.blit(text, (boxes[i].left + 3, boxes[i].top))
            # else: 
            #     pygame.draw.rect(WIN, , boxes[i])



    pygame.display.update()

def update():
    pygame.display.update()
    pygame.time.Clock().tick(20)

def main():
    global width, boxes, field, view, first, flag, seconds
    menu()
    run = True
    while run:

        seconds = (pygame.time.get_ticks() - startTicks) // 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menuBox.collidepoint(event.pos):
                    menu()
                if regameBox.collidepoint(event.pos):
                    start()
                view = view.reshape(width**2) 
                for i, x in enumerate(boxes):
                    if x.collidepoint(event.pos) and view[i] != 0:
                        if first:
                            generaCampo(i)
                            field = field.reshape(width**2) 
                            indi = getAttorno(i)
                            view[i] = 0
                            for j in indi:
                                view[j] = 0
                                if field[j]==0:
                                    checkZero(j)
                            first = False
                        view = view.reshape(width**2) 
                        field = field.reshape(width**2) 

                        if event.button == 1:
                            #left clcik
                            if view[i] == 2:
                                continue
                            elif field[i] >=50:
                                #perso
                                end(False)
                            elif field[i] == 0:
                                view[i] = 0
                                checkZero(i)
                            else:
                                view[i] = 0
                        elif event.button == 3:
                            if view[i] != 2:
                                flag-=1
                                view[i] = 2
                            else:
                                flag+=1
                                view[i] = 1
                        if checkWin():
                            end(True)
        draw()   
        update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()