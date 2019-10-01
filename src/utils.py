import cv2
import numpy as np


#Essa funcao foi feita para preparar as janelas para o algoritmo SAD,
#Cada janela, com tamanho definido pelo usuario na main, é uma colecao
#de triplas que contêm um valor RGB. Essa tripla é reduzida a um inteiro
#que é o módulo do "vetor RGB". Esse valor é utilizado para realizar o SAD.
def SumAbsoluteDiff(img0, aux_x, aux_y, winsize):
    window = np.zeros((winsize,winsize,3), dtype = np.uint8)
    img1 = cv2.imread('Piano1.png') #lendo imagem da esquerda
    img1 = cv2.resize(img1, (1080, 720))
    x0 = aux_x - winsize//2
    y0 = aux_y - winsize//2
    for j in range (0, winsize):
        for i in range (0, winsize):    
            window[i,j] = img0[y0 + i , x0 + j]
    cv2.imshow("janela", window)
    aux = img1[300:winsize+300, 300:winsize+300]
    cv2.imshow("aux", aux)

    absdif1 = np.square(window)
    absdif1 = np.sum(absdif1)
    absdif1 = np.sqrt(absdif1)
    absdif = np.square(aux)
    absdif = np.sum(absdif)
    absdif = np.sqrt(absdif)
    absdif = cv2.absdiff(absdif1, absdif)
    sumabsdif = np.sum(absdif)
 #   sumabsdif = np.sum(sumabsdif)
    print(sumabsdif)
    #cv2.imshow("outra janela", aux)
    