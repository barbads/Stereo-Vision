import utils
import sys
import cv2
import os

class Window:

    def __init__(self, winsize, window, img0):
        self.window = window
        self.img0 = img0
        self.winsize = winsize
    
    def CreateWindow(self, x, y):
        x0 = x - self.winsize//2  #fazendo um retangulo com centro no clique do usuario
        y0 = y - self.winsize//2
        
        if utils.CheckIfOutOfRange(self.img0, x, y, self.winsize) == 0:
            for j in range (0, self.winsize):
                for i in range (0, self.winsize):
                    self.window[i,j] = self.img0[y0 + i , x0 + j]
        else:
            print("Tamanho de janela muito grande para um pixel tao proximo à borda!")            
        return self.window
    