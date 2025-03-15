import pygame, globals

class LevelChunk(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self.road = pygame.image.load("assets/highway2x2.png").convert()
        self.grass = pygame.image.load("assets/grass.png").convert()
        self.image = pygame.surface.Surface((640,360))
        self.rect = pygame.rect.Rect(0,0,640,360)
        self.scrollPos = -360
        super().__init__(*groups)
    
    def update(self, dt):
        if self.scrollPos>360:
            temp = LevelChunk(self.groups()[0]) # TODO: Fix this piece of shit and get rifd of annoying gap. Also WTF... It is 3am and I dont know any more please help me.
            temp.scrollPos = self.scrollPos-360*2
            temp.update(dt)
            self.kill()
            return
        
        self.scrollPos += 0.15*dt

        self.rect.topleft = (0,self.scrollPos)
        self.image.blit(self.grass, (0,0))
        self.image.blit(self.road, (177, 0))
