import math
import pygame, time, TextureManager, random
from Player import Player
import globals
from level import LevelChunk
import level
from Cursor import Cursor
from TrafficManager import TrafficManager


class Game:
    def __init__(self):
        self.screen =  pygame.display.set_mode((0, 0))
        globals.screen_size = self.screen.get_size()
        self.scaledScreen = pygame.surface.Surface((640,360))
        TextureManager.loadCarTextures()
        TextureManager.loadLevelTextures()
        self.backgroundLayer = CameraGroup(self.scaledScreen)
        self.mainLayer = CameraGroup(self.scaledScreen)


        LevelChunk(self.backgroundLayer)
        temp = LevelChunk(self.backgroundLayer)
        temp.scrollPos = 0

        self.player = Player(self.mainLayer)
        globals.player = self.player
        pygame.mouse.set_visible(False)
        self.cursor = Cursor()

        self.trafficManager = TrafficManager(self.scaledScreen)

        
    def run(self):

        clock = pygame.time.Clock()
        running = True
        while running:
            dt = clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.cursor.update(dt)
            globals.drunkCursorPos = (self.cursor.bottom.x, self.cursor.bottom.y)

            self.backgroundLayer.update(dt)
            self.trafficManager.update(dt)
            self.mainLayer.update(dt)

            self.scaledScreen.fill((0,0,0))
            self.backgroundLayer.cameraDraw()
            self.trafficManager.draw()
            self.mainLayer.cameraDraw()
            self.scaledScreen.blit(self.cursor.image, self.cursor.rect.topleft)
            
            self.screen.blit(pygame.transform.scale(self.scaledScreen, self.screen.get_size()), (0,0))
            
            pygame.display.flip()


class CameraGroup(pygame.sprite.Group):
    def __init__(self, screen, *sprites):
        super().__init__(*sprites)
        self.surface = screen
        self.targetPos = pygame.math.Vector2()
        self.pos = pygame.math.Vector2()
        self.shakeIntensity = 0         # How much the camera shakes
    
    def update(self, dt):
        """Applies a continuous shake effect centered around targetPos."""
        if self.shakeIntensity > 0:
            random.seed(pygame.time.get_ticks())
            offsetX = random.uniform(-1, 1) * self.shakeIntensity
            offsetY = random.uniform(-1, 1) * self.shakeIntensity
            self.pos = self.targetPos + pygame.Vector2(offsetX, offsetY)
        else:
            self.pos = self.targetPos  # No shake, stay at target position
        
        super().update(dt)
    
    def cameraDraw(self):
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.pos
            self.surface.blit(sprite.image, offset_pos)

if __name__ == "__main__":
    pygame.init()

    game = Game()

    game.run()
