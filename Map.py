import pygame, sys, copy, math
import pygame.mixer
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

#Main Loop
def playGame():
    width = 1000
    height = 600
    screen = pygame.display.set_mode((width, height))
    car = pygame.image.load('car.png')
    baseImage = car.copy()
    map1 = pygame.image.load('Map.png')
    clock = pygame.time.Clock()
    x = width//2
    y = height//2
    angle = 0
    dx = 0
    dy = 0

    while(True):
        clock.tick(30)
        pygame.display.update()

        #Checks for quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit();
                 sys.exit();

        rad = math.radians(angle - 90)
        x += dx
        y += dy

        dy *= .85
        dx *= .85

        #Takes key input
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: 
            dx += math.cos(-rad) * 3
            dy += math.sin(-rad) * 3
        if pressed[pygame.K_DOWN]:
            dx -= math.cos(-rad)
            dy -= math.sin(-rad)
        if pressed[pygame.K_LEFT]:
            if pressed[pygame.K_DOWN] or pressed[pygame.K_UP]:
                angle += 5
        if pressed[pygame.K_RIGHT]:
            if pressed[pygame.K_DOWN] or pressed[pygame.K_UP]:
                angle -= 5

        car = rot_center(baseImage, angle)
        screen.fill((255, 255, 255))
        screen.blit(map1, (0, 0))
        screen.blit(car, (x, y))        

        pygame.display.flip()

playGame()