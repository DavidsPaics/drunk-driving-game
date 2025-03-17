import pygame, time, TextureManager, NotificationManager, globals

class Store:
    def __init__(self, screen):
        self.items = []
        self.screen = screen
        self.isOpen = False

    def openStore(self):
        self.isOpen = True
        # Capture the current screen
        screenCapture = self.screen.copy()
        # Create a blurred version of the capture (adjust amt as needed)
        blurredCapture = globals.blur(screenCapture, 5)
        # Create a dimming overlay (adjust alpha for different dim levels)
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # 128 for half transparency
        pygame.mouse.set_visible(1)

        # Main loop for the store
        while self.isOpen:
            dt = globals.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.isOpen = False

            
            self.screen.blit(blurredCapture, (0, 0))
            self.screen.blit(overlay, (0, 0))

            pygame.draw.rect(self.screen, (128,128,128), (150,150,self.screen.get_size()[0]-300, self.screen.get_size()[1]-300), border_radius=5)

            pygame.display.flip()

        pygame.mouse.set_visible(0)