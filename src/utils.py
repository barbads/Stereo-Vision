import cv2
import numpy as np

def SumAbsoluteDiff(img0, aux_x, aux_y, winsize):
    window = np.zeros((winsize,winsize,3), dtype = np.uint8)
    for i in range (0, winsize):
        for j in range (0, winsize):
            offset_i = i - (winsize%2)
            offset_j = j - (winsize%2)
            window[i,j] += img0[aux_y - j , aux_x - i]
    cv2.imshow("janela", window)
    
    