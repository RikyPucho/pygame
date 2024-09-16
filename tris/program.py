import numpy as np
import pygame
import sys
from time import sleep

pygame.font.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("tris")
font = pygame.font.Font(None, 50)
BG = pygame.image.load("assets/game.png")
menuBG = pygame.image.load("assets/menu.png")
winXBG = pygame.image.load("assets/winX.png")
winOBG = pygame.image.load("assets/winO.png")
loseBG = pygame.image.load("assets/lose.png")
drawBG = pygame.image.load("assets/draw.png")
segnoX = pygame.image.load("assets/x.png")
segnoO = pygame.image.load("assets/O.png")
segnoXTurn = pygame.image.load("assets/XTurno.png")
segnoOTurn = pygame.image.load("assets/OTurno.png")
boxWidth = 100

regameBox = pygame.Rect(100, 500, 200, 100)
regameText = font.render("Rigioca", True, (0,0,0))
menuBox = pygame.Rect(400, 500, 200, 100)
menuText = font.render("Menu", True, (0,0,0))

twoPLayerBox = pygame.Rect(100, 500, 200, 100)
twoPLayerText = font.render("2 players", True, (0,0,0))
twoPLayerText2 = font.render("1 pc", True, (0,0,0))
botBox = pygame.Rect(400, 500, 200, 100)
botText = font.render("Bot", True, (0,0,0))
botText2 = font.render("Imbattibile", True, (0,0,0))


player = True
boxes = []
values = []
isBot = False
field = np.array([
                    [2,2,2],
                    [2,2,2],
                    [2,2,2]
                ])


def addValue(val, inde):
    global field, values
    values[inde] = val
    i = 0
    j = inde
    if inde > 2:
        j = inde-3
        i = 1
    if inde > 5:
        j = inde-6
        i = 2
    
    field[i, j]= val
    if isBot:
        draw()
        update()
        sleep(0.3)
        bot()    
    return checkWin()

def index(i, j):
    if i == 1:
        i = 3
    if i == 2:
        i = 6
    return i+j
#gioca con O quindi False
def bot():
    global field, values
    #controllo per non far vincere l'altro o per far vincere il bot
    run = True
    defenseX = False
    defenseY = False
    giri = 0
    while run and giri < 3:
        giri+=1
        for i in range(3):
            #controllo righe
            if (field[i, 0] == field[i, 1] and field[i, 0] != 2) or (field[i, 1] == field[i,2] and field[i,1] != 2) or (field[i,2] == field[i,0] and field[i,2] != 2):

                #controllo se si tratta di difesa o vittoria
                if not field[i,0] or not field[i, 1] or not field[i,2] or defenseX:
                    for j in range(3):
                        if field[i, j] == 2:
                            field[i,j] = False
                            ind = index(i,j)
                            values[ind] = False
                            run=False
                            return
                else:
                    defenseX = True


            #controllo colonne
            if (field[0, i] == field[1,i] and field[0,i] !=2) or (field[1,i] == field[2,i] and field[1,i] !=2) or (field[2,i] == field[0,i] and field[2,i] != 2):

                if not field[0,i] or not field[1,i] or not field[2,i] or defenseY:
                    for j in range(3):
                        if field[j, i] == 2:
                            field[j,i] = False
                            ind = index(j,i)
                            values[ind] = False
                            run = False
                            return
                else:
                    defenseY = True
    if field[0, 0] == field[1,1] and field[0,0] != 2 and field[2,2] == 2:
        field[2,2] = False
        values[8] = False 
        return
    if ((field[0, 0] == field[2,2] and field[0,0] != 2) or (field[0, 2] == field[2,0] and field[2,0] != 2)) and field[1,1] == 2:
        field[1,1] = False
        values[4] = False
        return
    if field[2, 2] == field[1,1] and field[1,1] != 2 and field[0,0] == 2:
        field[0,0] = False
        values[0] = False
        return
    if field[0, 2] == field[1,1] and field[0,2] != 2 and field[2,0] == 2:
        field[2,0] = False
        values[6] = False
        return
    if field[1, 1] == field[2,0] and field[2,0] != 2 and field[0,2] == 2:
        field[0,2] = False
        values[2] = False
        return
    
    #centro se vuoto
    if field[1,1] == 2:
        field[1,1] = False
        values[4] = False
        return
    
    #interni in due casi specifici
    if field[0,0] == field[2,2] and field[0,0] == True:
        botVer()
        return
    if field[0,2] == field[2,0] and field[2,0] == True:
        botVer()
        return
    
    #vertici quando si va liberi
    for i in range(3):
        if i != 1:
            if field[i, i] == 2:
                field[i,i] = False
                ind = index(i,i)
                values[ind] = False
                return 
    if field[0,2] == 2:
        field[0,2] = False
        values[2] = False
        return
    if field[2,0] == 2:
        field[2,0] = False
        values[6] = False
        return
    
    #non spigoli cappppp
def botVer():
    global field, values
    for i in range(2):
        for j in range(1,3):
            if field[i,j] == 2:
                field[i,j] = False
                ind = index(i,j)
                values[ind] = False
                return
            elif field[j,i] == 2:
                field[j,i] = False
                ind = index(j,i)
                values[ind] = False
                return



#ritorna 2 se nessuno vince
#ritorna False quando 'O' vince
#ritorna True quando 'X' vince

def checkWin():
    global field
    for i in range(3):
        #controllo righe
        if field[i, 0] == field[i, 1] and field[i, 1] == field[i,2] and not field[i, 0] == 2:
            return False if field[i,0] == False else True
        #controllo colonne
        if field[0, i] == field[1,i] and field[1,i] == field[2,i] and not field[0,i] == 2:
            return False if field[0,i] == False else True
    if ((field[0,0] == field[1,1] and field[1,1] == field[2,2]) or (field[0,2] == field[1,1] and field[1,1] == field[2,0])) and not field[1,1] == 2:
        return False if field[1,1] == False else True
    return 2


def start():
    global field, boxes, values, player
    field = np.array([
                    [2,2,2],
                    [2,2,2],
                    [2,2,2]
                ])
    boxes = []
    values = []

    player = True

    x= 100
    y = 100
    for i in range(9):
        if i % 3 == 0 and i != 0:
            x= 100
            y+=200
        boxes.append(pygame.Rect(x, y, boxWidth, boxWidth))
        x+=200
        values.append(2)


def end(win):
    if win == True:
        #vinto x
        WIN.blit(winXBG, (0,0))
    elif win == False:
        #vinto O
        WIN.blit(winOBG, (0,0))
    elif win == 4:
        #perso
        WIN.blit(loseBG, (0,0))
    else:
        #pareggio
        WIN.blit(drawBG, (0,0))
    pygame.draw.rect(WIN, "grey", regameBox)
    WIN.blit(regameText, (135, 530))
    pygame.draw.rect(WIN, "grey", menuBox)
    WIN.blit(menuText, (450, 530))
    update()
    restart = False
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menuBox.collidepoint(event.pos):
                    restart = True
                    menu()
                elif regameBox.collidepoint(event.pos):
                    restart = True
                    start()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def update():
    pygame.display.update()
    pygame.time.Clock().tick(20)


def menu():
    global isBot
    play = False
    WIN.blit(menuBG, (0,0))
    pygame.draw.rect(WIN, "grey", twoPLayerBox)
    pygame.draw.rect(WIN, "grey", botBox)
    WIN.blit(twoPLayerText, (120, 510))
    WIN.blit(twoPLayerText2, (170, 550))
    WIN.blit(botText, (470, 510))
    WIN.blit(botText2, (410, 550))
    update()
    while not play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                play = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botBox.collidepoint(event.pos):
                    isBot = True
                    start()
                    return
                if twoPLayerBox.collidepoint(event.pos):
                    isBot = False
                    start()
                    return
    pygame.quit()
    sys.exit() 



def draw():
    WIN.blit(BG, (0,0))
    turn = font.render("turno di", True, (255,255, 255))
    WIN.blit(turn, (30,30))
    if player:
        WIN.blit(segnoXTurn, (180,5))
    else:
        WIN.blit(segnoOTurn, (180,5))
    WIN.blit(turn, (30,30))
    for i in range(9):
        if values[i] == 2:
            pygame.draw.rect(WIN, 'grey', boxes[i])
        elif values[i]:
            WIN.blit(segnoX, (boxes[i].left, boxes[i].top))
        else:
            WIN.blit(segnoO, (boxes[i].left, boxes[i].top))

    pygame.display.update()

def main():
    global boxes, field, values, player
    menu()
    run = True
    player = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(9):
                    if boxes[i].collidepoint(event.pos) and values[i] == 2:
                        win = addValue(player, i)
                        if not isBot:
                            player = not player
                        if win != 2 or not 2 in values:
                            draw()
                            update()
                            if isBot and win != 2:
                                win = 4
                                sleep(0.6)
                            end(win)
        
        draw()
        update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    start()
    main()