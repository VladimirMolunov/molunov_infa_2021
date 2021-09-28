import pygame
import numpy as np
from pygame.draw import *

pygame.init()

FPS = 30
size = 1000
screen = pygame.display.set_mode((size, size))

cgreen = (0, 104, 52)
cpink = (255, 176, 129)
cblack = (0, 0, 0)
cwhite = (255, 255, 255)

rect(screen, cpink, (0, 0, size, size))

def leaf(xa, ya, xb, yb):
    ellipse(screen, cgreen, (xa, ya, xb-xa, yb-ya))

def grect(xa, ya, width, height, x):
    polygon(screen, cgreen, [(xa, ya), (xa+width*np.cos(x), ya+width*np.sin(x)), (xa+width*np.cos(x)-height*np.sin(x), ya+width*np.sin(x)+height*np.cos(x)), (xa-height*np.sin(x), ya+height*np.cos(x))])

def duga(xa, ya, xb, yb, angle1, angle2):
    arc(screen, cgreen, (xa, ya, xb-xa, yb-ya), angle1, angle2, 2)

grect(500, 600, 30, 120, 0)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()