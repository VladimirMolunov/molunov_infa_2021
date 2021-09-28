import pygame
import numpy as np
from pygame.draw import *
from pygame import transform

pygame.init()

FPS = 30
size = 1000
screen = pygame.display.set_mode((size, size))

cgreen = (0, 104, 52)
cpink = (255, 176, 129)
cblack = (0, 0, 0)
cwhite = (255, 255, 255)
transparent = (200, 100, 90, 0)

rect(screen, cpink, (0, 0, size, size))

def leaf(surf, xa, ya, xb, yb):
    ellipse(surf, cgreen, (xa, ya, xb, yb))

def grect(xa, ya, width, height, x):
    polygon(screen, cgreen, [(xa, ya), (xa+width*np.cos(x), ya+width*np.sin(x)), (xa+width*np.cos(x)-height*np.sin(x), ya+width*np.sin(x)+height*np.cos(x)), (xa-height*np.sin(x), ya+height*np.cos(x))])

def duga(xa, ya, xb, yb, angle1, angle2):
    arc(screen, cgreen, (xa, ya, xb-xa, yb-ya), angle1, angle2, 2)

x1 = 500
y1 = 600
w1 = 30
h1 = 120
a1 = 0
gap = 20

grect(x1, y1, w1, h1, 0)
grect(x1, y1-gap-h1, w1, h1, 0)
grect(x1+w1-gap/2, y1-gap-2*h1, w1, h1-gap, np.pi/12)
grect(x1+2*w1+2*gap, y1-gap-2.7*h1-5*gap, w1-gap/2, h1+3.5*gap, np.pi/8)

x1 = 300
y1 = 700
w1 = 15
h1 = 60
a1 = 0
gap = 10

grect(x1, y1, w1, h1, 0)
grect(x1, y1-gap-h1, w1, h1, 0)
grect(x1+w1+gap/2, y1-4*gap-2*h1, w1, h1+2*gap, np.pi/12)
grect(x1+2*w1+3*gap, y1-6*gap-2.7*h1-5*gap, w1-gap/2, h1+4.5*gap, np.pi/8)

surface = pygame.Surface((300,300), pygame.SRCALPHA)
rect(surface, transparent, (0, 0, 300, 300))
leaf(surface, 100,100,100,20)
leaf(surface, 120,130,100,20)
leaf(surface, 130,160,100,20)
leaf(surface, 110,200,100,20)
leaf(surface, 115,250,100,20)
surface2 = pygame.transform.rotate(surface, 55)
surface3 = pygame.transform.rotate(surface, -70)
surface3 = pygame.transform.scale(surface3, (300,300))
surface4 = pygame.transform.rotate(surface, 55)
surface4 = pygame.transform.scale(surface4, (220,220))

screen.blit(surface2, (35,50))
screen.blit(surface3, (635,30))
screen.blit(surface4, (120,370))
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()