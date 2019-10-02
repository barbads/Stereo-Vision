import utils
import sys
import cv2
import os

class Window:

    def __init__(self, winsize, window, img0, img1):
        self.window = window
        self.img0 = img0
        self.img1 = img1
        self.winsize = winsize
    
    def CreateWindow(self, x, y):
        x0 = x - self.winsize//2  #fazendo um retangulo com centro no clique do usuario
        y0 = y - self.winsize//2
        
        if utils.CheckIfOutOfRange(self.img0, x, y, self.winsize) == 0:
            for j in range (0, self.winsize):
                for i in range (0, self.winsize):
                    self.window[i,j] = self.img0[y0 + i , x0 + j]
        else:
            border = utils.BorderCenterPoints(self.img0, self.winsize)
            for p in border:
                self.img0[p] = [0,255,0]
            cv2.imshow("pontinhos", self.img0)
        return self.window
    