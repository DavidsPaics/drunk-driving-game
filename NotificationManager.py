import time
import pygame
import TextureManager
import globals

class NotificationManager:
    def __init__(self, screen):
        self.screen = screen
        self.notifications = []
        self.notificationLength = 3  # seconds
        self.fadeLength = 0.5       # seconds
    
    def showNotification(self, text):
        self.notifications.append([text, time.time()])
    
    def update(self):
        # Remove notifications after the full notificationLength
        self.notifications = [n for n in self.notifications if time.time() - n[1] < self.notificationLength]
    
    def draw(self):
        yctr = 5
        current_time = time.time()
        for notification in self.notifications if not globals.DEBUG else [[f"FPS: {globals.clock.get_fps():.2f}", time.time()]] + self.notifications:
            elapsed = current_time - notification[1]
            if elapsed >= self.notificationLength - self.fadeLength:
                fade = (self.notificationLength - elapsed) / self.fadeLength
            else:
                fade = 1.0
            alpha = int(fade * 255)
            
            text = TextureManager.fontSmall.render(notification[0], True, (32, 32, 32))
            text.set_alpha(alpha)
            bg_width, bg_height = text.get_width() + 10, text.get_height() + 10
            
            # Create a background surface with per-pixel alpha for fading
            bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
            bg_surface.fill((128, 128, 128, alpha))
            self.screen.blit(bg_surface, (5, yctr))
            self.screen.blit(text, (10, yctr + 5))
            
            yctr += bg_height + 5
