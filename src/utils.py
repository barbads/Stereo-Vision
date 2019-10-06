import cv2
import numpy as np
from window import *



def TemplateMatching(img0, aux_x, aux_y, winsize):
    window = np.zeros((winsize,winsize,3), dtype = np.uint8)
    img1 = cv2.imread('Piano1.png') #lendo imagem da esquerda
    img1 = cv2.resize(img1, (1080, 720))

    window = Window(winsize, window, img0)
    window = window.CreateWindow(aux_x, aux_y)

    cv2.imshow("janela", window)
    gray_image = img1.copy()
    gray_template = window.copy()
    gray_image = cv2.cvtColor(gray_image, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(gray_template, cv2.COLOR_BGR2GRAY)

    #funcoes de matching do Open CV.
    res = cv2.matchTemplate(gray_image, gray_template, cv2.TM_CCOEFF_NORMED)
    menorvalor, maiorvalor, localminimo, localmaximo = cv2.minMaxLoc(res)

    #localmaximo = localmaximo[::-1]

    aux = img1.copy()
    coord1 = localmaximo 
    coord2 = (localmaximo[0] + winsize, localmaximo[1] + winsize)  
    print(coord1, coord2)
    aux = cv2.rectangle(aux, coord1, coord2, [0,255,0], 2)
    cv2.imshow("Correspondencia", aux)


def CheckIfOutOfRange(img, x, y, winsize):
    height, width, _ = img.shape

    if y + winsize > height:
        return 1            #o valor 1 significa que o quadro transbordou para baixo.
    elif y - winsize < 0:
        return 2            #o valor 2 significa que o quadro transbordou para cima.
    elif x + winsize > width:
        return 3            #o valor 3 significa que o quadro transbordou para a direita.
    elif x - winsize < 0:
        return 4            #o valor 4 significa que o quadro transbordou para a esquerda.
    else:
        return 0

def BorderCenterPoints(img, winsize):
    height, width, _ = img.shape
    borderp = []
    x = winsize//2
    y = winsize//2
    for i in range (0, width//winsize):
        borderp.append((x,y))
        x = x + winsize
    x = winsize//2
    y = y + winsize
    for i in range (1, height//winsize):
        borderp.append((x,y))
        y = y + winsize
    x = x + winsize
    for i in range (1, width//winsize):
        borderp.append((x,y))
        x = x + winsize
    y = y - winsize
    for i in range (1, height//winsize):
        borderp.append((x,y))
        y = y - winsize   
    print(borderp)

    return borderp
