import pygame

class PygameGame(object):

    def init(self):
        self.background = pygame.image.load('Map.png')
        self.background = pygame.transform.scale(self.background, (2 *self.width, 2*self.height))
        self.backgroundSize = self.background.get_size()        
        self.x = -self.width
        self.y = -self.height
        self.dx = 5
        self.dy = 5

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y): 
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_UP:
            if self.y + self.dy <= 0:
                self.y += self.dy
        if keyCode == pygame.K_DOWN:
            if self.y - self.dy > -self.height:
                self.y -= self.dy
        if keyCode == pygame.K_RIGHT:
            if self.x - self.dx > -self.width:
                self.x -= self.dx
        if keyCode == pygame.K_LEFT:
            if self.x + self.dx <= 0:
                self.x += self.dx

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        screen.blit(self.background,(self.x, self.y))


    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=600, height=400, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.keyPressed(pygame.K_LEFT, event.mod)
            if key[pygame.K_RIGHT]:
                self.keyPressed(pygame.K_RIGHT, event.mod)
            if key[pygame.K_UP]:
                self.keyPressed(pygame.K_UP, event.mod)            
            if key[pygame.K_DOWN]:
                self.keyPressed(pygame.K_DOWN, event.mod)
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()
