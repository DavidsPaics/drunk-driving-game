import math
import pygame, time, TextureManager, random
from Player import Player
import globals
from level import LevelChunk
import level
from Cursor import Cursor
from TrafficManager import TrafficManager
from Store import Store
from NotificationManager import NotificationManager


class Game:
    def __init__(self, screen):
        self.screen = screen
        globals.screen_size = self.screen.get_size()
        self.scaledScreen = pygame.surface.Surface((640,360))

        globals.notificationManager = NotificationManager(self.screen)

        TextureManager.loadCarTextures()
        TextureManager.loadLevelTextures()
        self.backgroundLayer = CameraGroup(self.scaledScreen)
        self.mainLayer = CameraGroup(self.scaledScreen)

        LevelChunk(self.backgroundLayer)
        temp = LevelChunk(self.backgroundLayer)
        temp.scrollPos = 0

        self.store = Store(self.screen)

        self.player = Player(self.endGame, self.mainLayer)
        globals.player = self.player
        pygame.mouse.set_visible(False)
        self.cursor = Cursor()

        self.trafficManager = TrafficManager(self.scaledScreen)


        
    def run(self):

        globals.clock = pygame.time.Clock()
        self.running = True
        while self.running:
            dt = globals.clock.tick(60)
            if dt==0:
                dt = 0.000001

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F3:
                        globals.DEBUG = not globals.DEBUG
                    
                    if event.key == pygame.K_e:
                        self.store.openStore()


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

            if globals.DEBUG:
                rprect = globals.player.collider
                pygame.draw.rect(self.scaledScreen, (0,255,0), rprect, 1)
                pygame.draw.rect(self.scaledScreen, (255,0,0), self.player.realRect, 1)
                pygame.draw.circle(self.scaledScreen, (255,0,0), self.player.realRect.center, 1)
                pygame.draw.circle(self.scaledScreen, (0,255,0), self.player.collider.center, 1)
            self.screen.blit(pygame.transform.scale(self.scaledScreen, self.screen.get_size()), (0,0))
            text = TextureManager.fontLarge.render(f"{self.player.money/100:.2f}$", 0, (255,255,255))
            textC = TextureManager.fontSmall.render(f"{self.player.caps} CAPS", 0, (255,255,255))
            pygame.draw.rect(self.screen, (64,128,64), (globals.screen_size[0]/2-(text.get_rect().centerx if text.get_size()[0]>textC.get_size()[0] else textC.get_rect().centerx)-5,10, max(text.get_size()[0], textC.get_size()[0])+10, text.get_size()[1]+textC.get_size()[1]+15), border_radius=3)
            self.screen.blit(text, (globals.screen_size[0]/2-text.get_rect().centerx,15))
            self.screen.blit(textC, (globals.screen_size[0]/2-textC.get_rect().centerx,20+text.get_size()[1]))

            globals.notificationManager.update()
            globals.notificationManager.draw()
            
            pygame.display.flip()
    
    def endGame(self):
        self.running = False


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