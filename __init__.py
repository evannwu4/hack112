import pygame, sys, copy, math, Car, calibrate
from pygame.locals import *
from Car import *

class Racing(object):
    def __init__(self, width=1000, height=600, fps=24, title="Driver 112"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.map1 = pygame.image.load('Map.png')
        self.xOff = 0
        self.yOff = 0
        self.time = 0
        pygame.init()
        #calibrate.run()

    def init(self):
        self.__init__()

    def redrawAll(self, screen, car1, text):
        screen.blit(self.map1, (self.xOff, self.yOff))
        screen.blit(car1.image, (car1.x - self.xOff + 450, car1.y - self.yOff + 250))
        screen.blit(text, (20, 20))



    def keyPressed(self, car1):
        #Takes key input
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('accel.wav')
            pygame.mixer.music.play(-1)
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
        if pressed[pygame.K_ESCAPE]:
            pygame.quit();
            sys.exit();

    def reset():
        car1 = Car(self.width//2, self.height//2)

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        screen1 = pygame.Surface((self.width    , self.height))
        pygame.display.set_caption(self.title)
        car1 = Car(self.width//2, self.height//2)
        pygame.mixer.music.load('engine.wav')
        pygame.mixer.music.play(-1)
        while(True):
            fps = 30
            clock.tick(fps)
            pygame.display.update()
            self.keyPressed(car1)
            car1.update()
            self.xOff = car1.x
            self.yOff = car1.y
            font = pygame.font.SysFont("comicsansms", 30)
            self.time += 1/30
            timerS = "LAP TIME : " + str(int(self.time))
            text = font.render(timerS, True, (0, 0, 0))
            
            #Checks for quitting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     pygame.quit();
                     sys.exit();

            screen.fill((0, 255, 0))
            self.redrawAll(screen, car1, text)
            
            pygame.display.flip()
            pygame.mixer.music.load('engine.wav')
            pygame.mixer.music.play(-1)


def main():
    game = Racing()
    game.run()

if __name__ == '__main__':
    main()