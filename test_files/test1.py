import pygame,math
import sys
from pygame.locals import *
clock=pygame.time.Clock()
FPS=60

screen = pygame.display.set_mode((1920,1080),FULLSCREEN)
image=pygame.image.load("1.jpg").convert()
position_up=0;
position_left=0;
