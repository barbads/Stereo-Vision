import sys
import os
import cv2 
import numpy as np
import utils

contador = 0
pixel = 0
aux_x = 0
aux_y = 0
winsize = 0
focal_lenght = 2826.171
baseline = 178.089


def Clicks(event,x,y,flags,param):
    global contador
    global pixel
    global aux_x
    global aux_y
    if event == cv2.EVENT_LBUTTONDOWN:
        if contador == 1:
            contador = 0
            img0[aux_y,aux_x] = pixel
        aux_x = x
        aux_y = y
        coordE = (aux_x, aux_y)
        print("Coordenadas da esquerda: ", coordE)
        coordD = utils.TemplateMatching(img0, aux_x, aux_y, winsize)
        print("Coordenadas da direita: ", coordD)
        WorldC = utils.WorldCoord(coordE, coordD, baseline, focal_lenght)
        print("Coordenadas do mundo X, Y, Z = ", WorldC)
        img1 = cv2.imread("Piano1.png")
        img1 = cv2.resize(img1, (1080, 720))
        pixel = img0[y,x]        
        clone0 = np.copy(img0)
        contador = 1
        clone0[y,x] = [0,255,0]



if __name__ == "__main__":

    img0 = cv2.imread('Piano0.png') #reading left image

    img0 = cv2.resize(img0, (1080, 720))
    #img1 = cv2.resize(img1, (1080, 720))

    print("Digitar tamanho da janela, em pixels, para algoritmo TM_CCOEFF_NORMED (numero impar, por favor): ")
    winsize = input()
    winsize = int(winsize)

    cv2.imshow("Imagem da Esquerda", img0)

    cv2.setMouseCallback("Imagem da Esquerda", Clicks)

    n = cv2.waitKey()
    if n == 27 & 0xFF:
        cv2.destroyAllWindows()



    



 