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


def DrawDot(event,x,y,flags,param):
    global contador
    global img1
    global pixel
    global aux_x
    global aux_y
    if event == cv2.EVENT_LBUTTONDOWN:
        if contador == 1:
            cv2.destroyWindow("fotinha nova")
            contador = 0
            img0[aux_y,aux_x] = pixel
        aux_x = x
        aux_y = y
        utils.SumAbsoluteDiff(img0, aux_x, aux_y, winsize)
        pixel = img0[y,x]        
        clone0 = np.copy(img0)
        contador = 1
        clone0[y,x] = [0,255,0]
  #    cv2.imshow("fotinha nova", clone0)


if __name__ == "__main__":

    img0 = cv2.imread('Piano0.png') #reading left image

    img0 = cv2.resize(img0, (1080, 720))
 #   img1 = cv2.resize(img1, (1080, 720))

    print("Digitar tamanho da janela, em pixels, para algoritmo SAD (numero impar, por favor): ")
    winsize = input()
    winsize = int(winsize)

    cv2.imshow("Imagem 0", img0)

    cv2.setMouseCallback("Imagem 0", DrawDot)

    n = cv2.waitKey()
    if n == 27 & 0xFF:
        cv2.destroyAllWindows()



    



 