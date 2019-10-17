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
piano = 0
morpheus = 0

def Clicks(event,x,y,flags,param):
    global piano
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
        coordD = utils.TemplateMatching(img0, aux_x, aux_y, winsize, piano)
        print("Coordenadas da direita: ", coordD)

        pixel = img0[y,x]        
        clone0 = img0.copy()
        contador = 1
        clone0 = cv2.rectangle(clone0, (x - winsize//2, y-winsize//2), (x+winsize//2,y+winsize//2), [0,255,0], 2)
        cv2.imshow("Imagem da Esquerda", clone0)

        height, width, _ = img0.shape

        dir_ = './data/Middleburry' 

        if sys.argv[2] == 'piano':
            dir_ = dir_ + '/Piano-perfect'
            img1 = cv2.imread(dir_ + '/Piano1.png')
            img1 = cv2.resize(img1, (1080, 720))
            baseline=178.089
            focal_lenght = 2826.171
            piano = 1
        elif sys.argv[2] == 'playroom':
            dir_ = dir_ + '/Playroom-perfect'
            img1 = cv2.imread(dir_ + '/Playroom1.png')
            img1 = cv2.resize(img1, (1080, 720))
            baseline=342.789
            focal_lenght = 4029.299
            piano = 0

        gray_image1 = img1.copy()
        gray_image1 = cv2.cvtColor(gray_image1, cv2.COLOR_BGR2GRAY)
        gray_image = img0.copy()
        gray_image0 = cv2.cvtColor(gray_image, cv2.COLOR_BGR2GRAY)
        
        disp = utils.Disparity(gray_image0, gray_image1)
        #cv2.imshow("disp map",disp)            

        WorldC = utils.WorldCoord(height, width, focal_lenght, baseline, disp, piano)
        print("Coordenadas do mundo (em mm): ", WorldC[y][x])

        _,_,depth = cv2.split(WorldC)
        depth = np.uint8(depth)
        #cv2.imshow("depth", depth)

        dir_ = './data/Middleburry' 

        if piano == 1:
            cv2.imwrite(dir_ + '/Piano-perfect/disparidade.pgm', disp)
            cv2.imwrite(dir_ + '/Piano-perfect/profundidade.png', depth)
        else:
            cv2.imwrite(dir_ + '/Playroom-perfect/disparidade.pgm', disp)
            cv2.imwrite(dir_ + '/Playroom-perfect/profundidade.png', depth)

def Clicks2(event,x,y,flags,param):
    global aux_x
    global aux_y
    global contador
    global morpheus
    global pixel
    global contador

    morpheus = 1
    if event == cv2.EVENT_LBUTTONDOWN:
        if contador == 1:
            contador = 0
            img0[aux_y,aux_x] = pixel
        aux_x = x
        aux_y = y
        coordE = (aux_x, aux_y)
        print("Coordenadas da esquerda: ", coordE)
        coordD = utils.TemplateMatching(img0, aux_x, aux_y, 55, piano, morpheus)
        print("Coordenadas da direita: ", coordD)

        pixel = img0[y,x]        
        clone0 = img0.copy()
        contador = 1
        clone0 = cv2.rectangle(clone0, (x - winsize//2, y-winsize//2), (x+winsize//2,y+winsize//2), [0,255,0], 2)
        cv2.imshow("Imagem da Esquerda", clone0)

if __name__ == "__main__":

    if sys.argv[1] == '-r1':

        dir_ = './data/Middleburry' 

        if sys.argv[2] == 'piano':
            dir_ = dir_ + '/Piano-perfect'
            img0 = cv2.imread(dir_ + '/Piano0.png') #reading left image
            img0 = cv2.resize(img0, (1080, 720))
            IntrinsicCam0= np.array([[2826.171, 0, 1292.2], [0, 2826.171, 965.806],[0, 0, 1]])
            IntrinsicCam1= np.array([[2826.171, 0, 1415.97],[0, 2826.171, 965.806], [0 ,0 ,1]])
            piano = 1

        elif sys.argv[2] == 'playroom':
            dir_ = dir_ + '/Playroom-perfect'
            img0 = cv2.imread(dir_ + '/Playroom0.png') #reading left image
            img0 = cv2.resize(img0, (1080, 720))
            cam0= np.array([[4029.299, 0, 1213.198], [0, 4029.299, 975.964], [0, 0, 1]])
            cam1= np.array([[4029.299, 0, 1484.019], [0, 4029.299, 975.964], [0, 0, 1]])

        print("Digitar tamanho da janela (sugestão: 55): ")
        winsize = input()
        winsize = int(winsize)

        cv2.imshow("Imagem da Esquerda", img0)

        cv2.setMouseCallback("Imagem da Esquerda", Clicks)

        n = cv2.waitKey()
        if n == 27 & 0xFF:
            cv2.destroyAllWindows()
