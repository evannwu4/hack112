import pygame, sys, copy, math
from pygame.locals import *

#CITATION : Code from http://www.pygame.org/wiki/RotateCenter?parent=CookBook
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

class Car(object):
    def __init__(self, x, y):
        self.image = pygame.image.load('car.png')
        self.x = x - 2800
        self.y = y - 1700
        self.baseImage = self.image.copy()
        self.angle = 90
        self.dx = 0
        self.dy = 0

    def update(self):
        self.image = rot_center(self.baseImage, self.angle)
        self.rad = math.radians(self.angle - 90)
        self.x += self.dx
        self.y += self.dy

        self.dy *= .85
        self.dx *= .85