import cv2
import numpy as np
from window import *



def TemplateMatching(img0, aux_x, aux_y, winsize, piano,morpheus):
    window = np.zeros((winsize,winsize,3), dtype = np.uint8)
    
    #lendo imagem da esquerda
    
    if morpheus == 1:
        dir_ = './data/FurukawaPonce'
        img1 = cv2.imread(dir_ + '/warriorR.jpg')
        img1 = cv2.resize(img1, (1080, 720))
    elif piano == 1:
        dir_ = './data/Middleburry' 
        dir_ = dir_ + '/Piano-perfect'
        img1 = cv2.imread(dir_ + '/Piano1.png') 
        img1 = cv2.resize(img1, (1080, 720))
    else:
        dir_ = './data/Middleburry' 
        dir_ = dir_ + '/Playroom-perfect'
        img1 = cv2.imread(dir_ + '/Playroom1.png') 
        img1 = cv2.resize(img1, (1080, 720))

    #Criando um objeto janela a partir do valor W dado pelo usuario.
    window = Window(55, window, img0)
    window = window.CreateWindow(aux_x, aux_y)

    cv2.imshow("janela", window)
    gray_image = img1.copy()
    gray_image0 = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
    gray_template = window.copy()
    gray_image = cv2.cvtColor(gray_image, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(gray_template, cv2.COLOR_BGR2GRAY)

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

def WorldCoord(height, width, focal_length, baseline, disp, piano):
    
    xL = np.arange(np.float32(width))
    xL = np.tile(xL,(height,1))
    yL = np.arange(np.float32(height))
    yL = np.tile(yL,(width,1))
    yR = yL
    xR = xL + disp
    const = baseline/2
    deltaX = xL-xR
    deltaX[deltaX == 0.0] = np.inf
    X = -const*((xL + xR) / deltaX)
    Y = -const*(np.transpose(yL + yR) / deltaX)
    const = baseline * focal_length
    Z = -const / deltaX


    if piano == 1:
        Z[Z>5719] = 5719
    #else:
    #    Z[Z>21] = 21

    Z = cv2.normalize(src=Z, dst=Z, beta=0, alpha=254, norm_type=cv2.NORM_MINMAX)
    Z[Z == 0] = 255

    world_coordinates = cv2.merge((X,Y,Z))

    return world_coordinates

def Disparity(img0, img1):
    #Aqui foi usada a funcao cv2.StereoSGBM. 
    #fonte: http://timosam.com/python_opencv_depthimage
    #adaptado

    window_size = 11 
    stereoE = cv2.StereoSGBM_create(minDisparity = 16, numDisparities = 80, blockSize=11,
                                P1= 968,   
                                P2 = 3872,
                                disp12MaxDiff=1,
                                uniquenessRatio=15,
                                speckleWindowSize=150,
                                speckleRange=2,
                                preFilterCap=63,
                                mode = 1)
    
    stereoD = cv2.ximgproc.createRightMatcher(stereoE)

    # FILTER Parameters
    lmbda = 8000
    sigma = 2
    visual_multiplier = 1.0
    
    wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=stereoE)
    wls_filter.setLambda(lmbda)
    wls_filter.setSigmaColor(sigma)

    displ = stereoE.compute(img0, img1)
    dispr = stereoD.compute(img1, img0) 
    displ = np.int16(displ)
    dispr = np.int16(dispr)

    filteredImg = wls_filter.filter(displ, img0, None, dispr) 
    cv2.filterSpeckles(filteredImg, 16, 4000, 256) 

    filteredImg = cv2.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX)
    filteredImg = np.uint8(filteredImg)

    return filteredImg
