import random
import pygame
import TextureManager
import globals

SCREEN_CENTER_X = 320

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.carType = "compact_red"
        self.originalImage = TextureManager.carTextures.get(self.carType) or TextureManager.carTextures.get("compact_red")
        self.realRect = self.originalImage.get_rect()
        self.rect = self.realRect
        self.image = self.originalImage
        self.realRect.center = (SCREEN_CENTER_X, 300)

        self.velocityX = 0
        self.accelerationX = 0
        self.angle = 0

        self.shakeIntensity = 0

        self.drivingSpeed = 0.15

    def update(self, dt):
        self.handleInput(dt)

        maxTilt = 25
        maxVelocity = 0.25  # Ensure it matches the handleInput max velocity

        # Scale velocity to angle range (-25 to 25)
        self.angle = max(-maxTilt, min(maxTilt, (self.velocityX / maxVelocity) * maxTilt))

        # self.realRect.x += self.velocityX * dt

        if (self.realRect.right > 462 or self.realRect.x<177): #highway2x2
            self.shakeIntensity = 3
            globals.scrollSpeed = max(self.drivingSpeed-0.075, globals.scrollSpeed-0.00005*dt)
        else:
            self.shakeIntensity = 0
            globals.scrollSpeed = min(self.drivingSpeed, globals.scrollSpeed+0.00005*dt)

        self.shake(dt)

        self.image = pygame.transform.rotate(self.originalImage, -self.angle)
        self.realRect = self.image.get_rect(center=self.realRect.center)


    def shake(self, dt):
        if self.shakeIntensity > 0:
            random.seed(pygame.time.get_ticks())
            offsetX = random.uniform(-1, 1) * self.shakeIntensity
            offsetY = random.uniform(-1, 1) * self.shakeIntensity
            self.rect.center = self.realRect.center + pygame.Vector2(offsetX, offsetY)
        else:
            self.rect.center = self.realRect.center  # No shake, stay at target position

    def handleInput(self, dt):
        targetX, _ = globals.drunkCursorPos

        # Adjust acceleration factor for smooth response
        acceleration = .00025  # How fast it speeds up
        damping = 0.9       # Slows down oscillations smoothly
        threshold = 0.01    # When to clamp velocity to zero

        # Compute acceleration based on the difference in position
        force = (targetX - self.realRect.centerx) * acceleration

        # Apply force to velocity (inertia effect)
        self.velocityX = max(-0.5, min(0.5, force * dt))

        # Apply damping to gradually settle motion
        self.velocityX *= damping

        # Clamp velocity to zero if it's too small
        if abs(self.velocityX) < threshold:
            self.velocityX = 0

        # Update position using velocity
        self.realRect.centerx += self.velocityX * dt

    def onCrash(self):
        print("crash")
        self.kill()
