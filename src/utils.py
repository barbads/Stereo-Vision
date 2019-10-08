import cv2
import numpy as np
from window import *



def TemplateMatching(img0, aux_x, aux_y, winsize):
    window = np.zeros((winsize,winsize,3), dtype = np.uint8)
    img1 = cv2.imread('Piano1.png') #lendo imagem da esquerda
    img1 = cv2.resize(img1, (1080, 720))

    #Criando um objeto janela a partir do valor W dado pelo usuario.
    window = Window(winsize, window, img0)
    window = window.CreateWindow(aux_x, aux_y)

    cv2.imshow("janela", window)
    gray_image = img1.copy()
    gray_image0 = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
    gray_template = window.copy()
    gray_image = cv2.cvtColor(gray_image, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(gray_template, cv2.COLOR_BGR2GRAY)

    Disparity(gray_image0, gray_image)

    #funcoes de matching do Open CV. localminimo e localmaximo sao 
    #os pontos de minimo e maximo. o utilizado aqui eh o maximo por conta
    #do metodo cv2.TM_CCOEFF_NORMED.
    res = cv2.matchTemplate(gray_image, gray_template, cv2.TM_CCOEFF_NORMED)
    menorvalor, maiorvalor, localminimo, localmaximo = cv2.minMaxLoc(res)

    coordD = (localmaximo[0] + winsize//2, localmaximo[1] + winsize//2)

    aux = img1.copy()
    coord1 = localmaximo 
    coord2 = (localmaximo[0] + winsize, localmaximo[1] + winsize)  
    aux = cv2.rectangle(aux, coord1, coord2, [0,255,0], 2)
    cv2.imshow("Correspondencia", aux)

    return coordD


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

def WorldCoord(coordE, coordD, baseline, focal_lenght):
    X = baseline*(coordE[0] + coordD[0])/2*(coordE[0] - coordD[0])
    Y = baseline*(coordE[1] + coordD[1])/2*(coordE[0] - coordD[0])
    Z = baseline*focal_lenght / (coordE[0] - coordD[0])

    return (X, Y, Z)

def Disparity(img0, img1):
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(img0,img1)

    cv2.imshow("disp map",disparity)