import pygame, time, TextureManager, NotificationManager, globals

class Store:
    def __init__(self, screen):
        self.items = []
        self.screen = screen
        self.scaledScreen = pygame.surface.Surface((1920,1080))
        self.isOpen = False

        self.background = pygame.image.load("assets/store.png").convert()
        self.background = pygame.transform.scale(self.background, (self.background.get_size()[0]*7, self.background.get_size()[1]*7))
        self.lido = pygame.transform.scale(pygame.image.load("assets/drinks/lidu.png"), (104,375)).convert_alpha()

    def openStore(self):
        self.isOpen = True
        # Capture the current screen
        screenCapture = self.screen.copy()
        # Create a blurred version of the capture (adjust amt as needed)
        blurredCapture = globals.blur(pygame.transform.scale(screenCapture, (1920,1080)), 5)
        # Create a dimming overlay (adjust alpha for different dim levels)
        overlay = pygame.Surface(self.scaledScreen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # 128 for half transparency
        pygame.mouse.set_visible(1)

        
        # Main loop for the store
        while self.isOpen:
            dt = globals.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE, pygame.K_e]:
                        self.isOpen = False

            
            self.scaledScreen.blit(blurredCapture, (0, 0))
            self.scaledScreen.blit(overlay, (0, 0))

            self.scaledScreen.blit(self.background, (150,150))
            self.scaledScreen.blit(TextureManager.fontMedium.render("Lidu Beer 2.50$", 0, (255,255,255)), (150,680))

            self.scaledScreen.blit(self.lido, (260,200))

            self.screen.blit(pygame.transform.scale(self.scaledScreen, self.screen.get_size()), (0,0))

            pygame.display.flip()

        pygame.mouse.set_visible(0)