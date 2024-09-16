import numpy as np
import pygame 
import random as ran
import sys

pygame.font.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battaglia navale")
font = pygame.font.SysFont(None, 60)
fontBig = pygame.font.Font(None, 75)
BG = pygame.image.load("assets/sfondoBattagliaNavale.png")

colpiMax = 20

caselleWidth = 50
caselleHeight = 50

piccole = 3
medie = 2
grandi = 1
colpi = 0
campo = np.array([[False,False, False, False, False],
                [False,False, False, False, False],
                [False,False, False, False, False],
                [False,False, False, False, False],
                [False,False, False, False, False],])

view = np.array([['0','0', '0', '0', '0'],
                ['0','0', '0', '0', '0'],
                ['0','0', '0', '0', '0'],
                ['0','0', '0', '0', '0'],
                ['0','0', '0', '0', '0'],])
viewCopia = view.copy()
dis = np.array([['#','#','#','#','#'],
                ['#','#','#','#','#'],
                ['#','#','#','#','#'],
                ['#','#','#','#','#'],
                ['#','#','#','#','#'],])
naviGrandiCoo =np.array([[-1, -1],[-1, -1],[-1,-1]])
naviPiccoleCoo = np.array([[-1,-1],
                        [-1,-1],
                        [-1,-1],
                        ])
naviMedieCoo = np.array([
                            [[-1,-1],[-1,-1]],
                            [[-1,-1],[-1,-1]],
                        ])

text = fontBig.render("", True, (0,0,0))  
colpiText = fontBig.render(str(colpiMax-colpi), True, (0, 0,0))  
piccoleText = font.render(str(piccole), True, (0,0,0))
medieText = font.render(str(medie), True, (0,0,0))
grandiText = font.render(str(grandi), True, (0,0,0))
caselle = []
caselleSoluzione = []


def inizio():
    global campo, view, viewCopia, dis, naviGrandiCoo,naviPiccoleCoo, naviMedieCoo
    global piccole, grandi, medie, colpi, text, caselleSoluzione
    global colpiText, piccoleText, medieText, grandiText
    BG = pygame.image.load("assets/sfondoBattagliaNavale.png")

    text = fontBig.render("", True, (0,0,0))  
    piccole = 3
    medie = 2
    grandi = 1
    colpi = 0
    colpiText = fontBig.render(str(colpiMax-colpi), True, (0, 0,0))  
    piccoleText = font.render(str(piccole), True, (0,0,0))
    medieText = font.render(str(medie), True, (0,0,0))
    grandiText = font.render(str(grandi), True, (0,0,0))
    campo = np.array([[False,False, False, False, False],
                  [False,False, False, False, False],
                  [False,False, False, False, False],
                  [False,False, False, False, False],
                  [False,False, False, False, False],])

    view = np.array([['0','0', '0', '0', '0'],
                    ['0','0', '0', '0', '0'],
                    ['0','0', '0', '0', '0'],
                    ['0','0', '0', '0', '0'],
                    ['0','0', '0', '0', '0'],])
    viewCopia = view.copy()
    dis = np.array([['#','#','#','#','#'],
                    ['#','#','#','#','#'],
                    ['#','#','#','#','#'],
                    ['#','#','#','#','#'],
                    ['#','#','#','#','#'],])
    naviGrandiCoo =np.array([[-1, -1],[-1, -1],[-1,-1]])
    naviPiccoleCoo = np.array([[-1,-1],
                            [-1,-1],
                            [-1,-1],
                            ])
    naviMedieCoo = np.array([
                                [[-1,-1],[-1,-1]],
                                [[-1,-1],[-1,-1]],
                            ])
    caselle.clear()
    caselleSoluzione.clear()
    creaBarche()
    yPos = 165
    xPos = 150
    for i in range(25):
        if i % 5 == 0:
            xPos = 83
            yPos +=80
        caselle.append(pygame.Rect(xPos, yPos, caselleWidth, caselleHeight))
        xPos+=80
    yPos = 165
    xPos = 400
    for i in range(25):
        if i % 5 == 0:
            xPos = 400
            yPos +=80
        caselleSoluzione.append(pygame.Rect(xPos, yPos, caselleWidth, caselleHeight))
        xPos+=80

# 3 navi da 1
# 2 navi da 2
# 1 nave da 3
def controlloAccanto(x, y, ori = True, tripla = False):
    if campo[y,x] and not tripla:
        # print("campo occupato",y, x)
        return 0
    if ori:
        if len(campo[0]) != x+1 and not campo[y, x+1]:
            # print("campo accanto disponibile", y, x+1)
            return 1
    else:
        if len(campo[0]) != y+1 and not campo[y+1,x]:
            # print("campo sotto disponibile", x, y+1)
            return 1
    return 0
        
#generazioni navi da 1
def creaBarche():
    temp = 0
    while temp < 3:
        x = ran.randint(0, 4)
        y = ran.randint(0, 4)
        if not campo[x,y]:
            campo[x, y] = True
            view[x,y]= '='
            fafa = False
            for ind, i in np.ndenumerate(naviPiccoleCoo):
                if fafa:
                    naviPiccoleCoo[ind] = y
                    break
                if i == -1:
                    naviPiccoleCoo[ind] = x
                    fafa = True
                    continue
                fafa = False

                    
            temp+=1
        else:
            continue
    #generazioni navi da 2
    temp = 0
    while temp < 2:
        oriz = ran.randint(0,1)
        x = ran.randint(0,4)
        y = ran.randint(0,4)
        if oriz == 1:
            if controlloAccanto(x,y,ori=True) == 1:
                view[y,x], view[y,x+1] = '-', '-'
                campo[y,x], campo[y,x+1] = True, True
                temp+=1
                fafa = False
                tata = False
                caca = False
                for ind, i in np.ndenumerate(naviMedieCoo):
                    if caca:
                        naviMedieCoo[ind] = x + 1
                        break
                    if fafa:
                        naviMedieCoo[ind] = x
                        fafa = False
                        tata = True
                        continue
                    if i == -1:
                        naviMedieCoo[ind] = y
                        if not tata:
                            fafa = True
                        else:
                            caca = True
                            tata = False
                        continue
        else:
            if controlloAccanto(x,y,ori=False) == 1:
                view[y,x], view[y+1,x] = '|', '|'
                campo[y,x], campo[y+1,x] = True, True
                temp+=1
                fafa = False
                tata = False
                for ind, i in np.ndenumerate(naviMedieCoo):
                    if fafa:
                        if tata:
                            break
                        naviMedieCoo[ind] = x
                        fafa = False
                        tata = True
                        continue
                    if tata:
                        naviMedieCoo[ind] = y+1
                        fafa = True
                        continue                        
                    if i == -1:
                        naviMedieCoo[ind] = y
                        fafa = True
                        continue

    #generazione nave da 3
    temp=0
    while temp<1:
        oriz = ran.randint(0,1)
        x = ran.randint(0,4)
        y = ran.randint(0,4)
        if oriz == 1:
            if controlloAccanto(x,y,ori=True) == 1 and controlloAccanto(x+1,y, ori=True, tripla=True) == 1:
                view[y,x], view[y,x+1], view[y,x+2] = 'Q', 'Q', 'Q'
                campo[y,x], campo[y,x+1], campo[y,x+2] = True, True, True
                temp+=1
                naviGrandiCoo[0, 0] = y
                naviGrandiCoo[0, 1] = x
                naviGrandiCoo[1, 0] = y
                naviGrandiCoo[1, 1] = x+1
                naviGrandiCoo[2, 0] = y
                naviGrandiCoo[2, 1] = x+2
        else:
            if controlloAccanto(x,y,ori=False) == 1 and controlloAccanto(x,y+1, ori=False, tripla=True) == 1:
                view[y,x], view[y+1,x], view[y+2,x] = 'Q', 'Q', 'Q'
                campo[y,x], campo[y+1,x], campo[y+2,x] = True, True, True
                temp+=1
                naviGrandiCoo[0, 0] = y
                naviGrandiCoo[0, 1] = x
                naviGrandiCoo[1, 0] = y+1
                naviGrandiCoo[1, 1] = x
                naviGrandiCoo[2, 0] = y+2
                naviGrandiCoo[2, 1] = x
def calcoloIndice(i):
    if i < 5:
        return 0, i
    if i < 10:
        return 1, i-5
    if i < 15:
        return 2, i-10
    if i <20:
        return 3, i-15
    return 4, i-20

def controlloAffonda():
    barchePiccole =0
    barcheGrandi = 0
    barcheMedie = 0
    oriz = False
    temp = 2
    for i, x in np.ndenumerate(view):
        if oriz:
            oriz = False
            continue
        if x == '=':
            barchePiccole+=1
        if x == '-':
            barcheMedie+=1
            oriz = True
        if x == '|':
            if temp%2==0:
                barcheMedie +=1
            temp+=1
        if x == 'Q':
            barcheGrandi = 1
    return barchePiccole, barcheMedie, barcheGrandi
def fine(vinto):
    global text, BG
    if vinto:
        fine = pygame.image.load("assets/vinto.png")
        WIN.blit(fine, (0,0))
    else:
        drawSoluzione()
    pygame.display.update()
    ricomincia = False
    first = True
    while not ricomincia:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not vinto and first:
                    fine = pygame.image.load("assets/perso.png")
                    WIN.blit(fine, (0,0))
                    pygame.display.update()
                    first = False
                    continue
                ricomincia = True
                inizio()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
def drawSoluzione():
    global colori
    colori = []
    for ind, x in np.ndenumerate(dis):
        if x == '#':
            if campo[ind] == True:
                colori.append('green')
            else:
                colori.append('blue')
        elif x == 'x':
            colori.append("red")
        elif x == '0':
            colori.append("blue")

    i = 0
    while i < len(caselle):
        if colori[i] == "blue":
            pass
        else:
            pygame.draw.rect(WIN, colori[i], caselle[i])
        i+=1
    pygame.display.update
def affondato(tipoNave):
    global text, BG
    if tipoNave == "piccola":
        BG = pygame.image.load("assets/piccola.png")
    elif tipoNave == "media":
        BG = pygame.image.load("assets/media.png")
    elif tipoNave == "grande":
        BG = pygame.image.load("assets/grande.png")
    update()
    draw()

def update():
    pygame.display.update()
    pygame.time.Clock().tick(20)
colori = []
def draw():
    global colori
    WIN.blit(BG, (0 , 0))
    WIN.blit(text, (30,100))
    WIN.blit(piccoleText, (650,330))
    WIN.blit(medieText, (650,460))
    WIN.blit(grandiText, (650,570))
    WIN.blit(colpiText, (700,100))
    # ytemp = 0
    # yPos = 200
    # xPos = 30
    colori = []
    for ind, x in np.ndenumerate(dis):
        if x == '#':
            colori.append("grey")
        elif x == 'x':
            colori.append("red")
        elif x == '0':
            colori.append("blue")

    i = 0
    while i < len(caselle):
        if colori[i] == "blue":
            pass
        else:
        # print(caselle[i])
            pygame.draw.rect(WIN, colori[i], caselle[i])
        i+=1
            
    pygame.display.update()

            

def main():
    global colpi, piccole, medie, grandi, BG
    global text, piccoleText, medieText, grandiText,colpiText
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False
                break   
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(caselle)):
                    if caselle[i].collidepoint(event.pos) and colori[i] != "blue" and colori[i]!="red":
                        BG = pygame.image.load("assets/sfondoBattagliaNavale.png")
                        update()
                        y, x = calcoloIndice(i)
                        dis[y, x]='x' if campo[y, x] else '0'
                        view[y, x]='0'
                        campo[y, x] = False
                        colpi +=1
                        
                        colpiText = fontBig.render(str(colpiMax-colpi), True, (0, 0,0))  
                        text = fontBig.render("", True, (0,0,0)) 
        draw()
        update()
        piccoleTe, medieTe, grandiTe = controlloAffonda()
        if piccoleTe != piccole:
            piccole = piccoleTe
            affondato('piccola')
        if medieTe != medie:
            #hai affondato una media
            medie = medieTe
            affondato('media')
        if grandiTe != grandi:
            #hai affondato la grande
            grandi = grandiTe
            affondato('grande')
        
        piccoleText = font.render(str(piccole), True, (0,0,0))
        medieText = font.render(str(medie), True, (0,0,0))
        grandiText = font.render(str(grandi), True, (0,0,0))
        if piccole == 0 and medie == 0 and grandi ==0:
            #hai vinto
            fine(True)
        if colpi >= colpiMax:
            fine(False)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    inizio()
    main()