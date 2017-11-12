import pygame, sys, copy, math, Car
from pygame.locals import *
from Car import *

class Racing(object):
    def __init__(self, width=1000, height=600, fps=24, title="Hack112 Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.map1 = pygame.image.load('Map.png')
        self.xOff = 0
        self.yOff = 0
        pygame.init()

    def init(self):
        pass

    def redrawAll(self, screen, car1):
        screen.blit(self.map1, (self.xOff, self.yOff))
        screen.blit(car1.image, (car1.x - self.xOff + 450, car1.y - self.yOff + 250))


    def keyPressed(self, car1):
        #Takes key input
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            car1.dx -= math.cos(-car1.rad) * 3
            car1.dy -= math.sin(-car1.rad) * 3
        if pressed[pygame.K_DOWN]:
            car1.dx += math.cos(-car1.rad)
            car1.dy += math.sin(-car1.rad)
        if pressed[pygame.K_LEFT]:
            if pressed[pygame.K_DOWN] or pressed[pygame.K_UP]:
                car1.angle += 5
        if pressed[pygame.K_RIGHT]:
            if pressed[pygame.K_DOWN] or pressed[pygame.K_UP]:
                car1.angle -= 5

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        screen1 = pygame.Surface((self.width    , self.height))
        pygame.display.set_caption(self.title)
        car1 = Car(self.width//2, self.height//2)

        while(True):
            clock.tick(30)
            pygame.display.update()
            self.keyPressed(car1)
            car1.update()
            self.xOff = car1.x
            self.yOff = car1.y
            
            #Checks for quitting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     pygame.quit();
                     sys.exit();

            screen.fill((255, 255, 255))
            self.redrawAll(screen, car1)
            pygame.display.flip()


def main():
    game = Racing()
    game.run()

if __name__ == '__main__':
    main()