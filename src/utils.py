import cv2
import numpy as np
from window import *


#Essa funcao foi feita para preparar as janelas para o algoritmo SAD,
#Cada janela, com tamanho definido pelo usuario na main, é uma colecao
#de triplas que contêm um valor RGB. Essa tripla é reduzida a um inteiro
#que é o módulo do "vetor RGB". Esse valor é utilizado para realizar o SAD.
def SumAbsoluteDiff(img0, aux_x, aux_y, winsize):
    window = np.zeros((winsize,winsize,3), dtype = np.uint8)
    img1 = cv2.imread('Piano1.png') #lendo imagem da esquerda
    img1 = cv2.resize(img1, (1080, 720))

    window = Window(winsize, window, img0, img1)
    window = window.CreateWindow(aux_x, aux_y)

    cv2.imshow("janela", window)
    aux = img1[300:winsize+300, 300:winsize+300]
    cv2.imshow("aux", aux)

#Fazendo com que cada pixel seja representado pelo modulo do vetor RGB
#no espaco cujos eixos sao R, G e B.        
    absdif1 = np.square(window)
    absdif1 = np.sum(absdif1)
    absdif1 = np.sqrt(absdif1)
    absdif = np.square(aux)
    absdif = np.sum(absdif)
    absdif = np.sqrt(absdif)
    absdif = cv2.absdiff(absdif1, absdif)
    sumabsdif = np.sum(absdif)
 #  sumabsdif = np.sum(sumabsdif)
    print(sumabsdif)
    #cv2.imshow("outra janela", aux)

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
