from pygame.locals import *
from random import randint
import pygame
import time
from Player import Player
from AI import Computer

class Apple:
    x = 0
    y = 0
    step = 44

    def __init__(self, x, y):
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


class Game:
    def isCollision(self, x1, y1, x2, y2, bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False


class App:
    windowWidth = 800
    windowHeight = 600
    player = 0
    apple = 0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        self.player = Player(5)
        self.apple = Apple(8, 5)
        self.computer = Computer(5)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._image_surf = pygame.image.load("snake.png").convert()
        self._apple_surf = pygame.image.load("food.png").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.computer.target(self.apple.x, self.apple.y)
        self.player.update()
        self.computer.update()

        # does snake eat apple?
        for i in range(0, self.player.length):
            if self.game.isCollision(self.apple.x, self.apple.y, self.player.x[i], self.player.y[i], 44):
                self.apple.x = randint(2, 9) * 44
                self.apple.y = randint(2, 9) * 44
                self.player.length = self.player.length + 1

        # does computer eat apple?
        for i in range(0, self.player.length):
            if self.game.isCollision(self.apple.x, self.apple.y, self.computer.x[i], self.computer.y[i], 44):
                self.apple.x = randint(2, 9) * 44
                self.apple.y = randint(2, 9) * 44
                # self.computer.length = self.computer.length + 1

        # does snake collide with itself?
        for i in range(2, self.player.length):
            if self.game.isCollision(self.player.x[0], self.player.y[0], self.player.x[i], self.player.y[i], 40):
                print
                "You lose! Collision: "
                print
                "x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")"
                print
                "x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")"
                exit(0)

        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        self.computer.draw(self._display_surf, self._image_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                self.player.moveRight()

            if (keys[K_LEFT]):
                self.player.moveLeft()

            if (keys[K_UP]):
                self.player.moveUp()

            if (keys[K_DOWN]):
                self.player.moveDown()

            if (keys[K_ESCAPE]):
                self._running = False

            self.on_loop()
            self.on_render()

            time.sleep(50.0 / 1000.0);
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()