import random
import pygame
import TextureManager
import globals

SCREEN_CENTER_X = 320

radio = [None]

class Player(pygame.sprite.Sprite):
    def __init__(self, endGameCallback, *groups):
        super().__init__(*groups)
        self.carType = "compact_red"
        self.originalImage = TextureManager.carTextures.get(self.carType) or TextureManager.carTextures.get("compact_red")
        self.realRect = self.originalImage.get_rect()
        self.rect = self.realRect
        self.collider = self.originalImage.get_rect()
        self.collider = pygame.rect.Rect(self.collider.x+10,self.collider.y+10,self.collider.width-10,self.collider.height-10)
        self.image = self.originalImage
        self.realRect.center = (SCREEN_CENTER_X, 300)

        self.endGameCallback = endGameCallback

        self.velocityX = 0
        self.accelerationX = 0
        self.angle = 0

        self.shakeIntensity = 0
        self.drivingSpeed = 0.25

        self.money = 0
        self.caps = 0

        self.fade_time = 1000  # milliseconds
        self.engine_sound = pygame.mixer.Sound("assets/sounds/engine.mp3")
        self.offroad_sound = pygame.mixer.Sound("assets/sounds/offroad.mp3")
        self.engine_channel = pygame.mixer.Channel(0)
        self.offroad_channel = pygame.mixer.Channel(1)
        self.radioChannel = pygame.mixer.Channel(2)
        self.radioChannel.set_volume(1)

        for i in range(1,6):
            radio.append(pygame.mixer.Sound(f"assets/sounds/radio/{i}.mp3"))

        # Select a song based on your condition
        if random.randint(1, 4) == 1:
            song = radio[random.randint(0, 1)]  # adjust index if your list is 0-indexed
        else:
            song = radio[random.randint(2, 5)]  # adjust index accordingly

        # Start playing the selected song
        self.radioChannel.play(song)

        if song not in [radio[0], radio[1]]:
            # Determine a random start time between 0 and the song's duration
            random_start = random.uniform(0, song.duration)
            self.radioChannel.seek(random_start)  # Jump to the random point in the song


    def update(self, dt):
        self.handleInput(dt)

        maxTilt = 25
        maxVelocity = 0.25
        self.angle = max(-maxTilt, min(maxTilt, (self.velocityX / maxVelocity) * maxTilt))

        if not self.radioChannel.get_busy():
            self.radioChannel.play(radio[random.randint(1,6)])

        if (self.realRect.right > 462 or self.realRect.x < 177):  # offroad condition
            self.shakeIntensity = 3
            globals.scrollSpeed = max(self.drivingSpeed - 0.125, globals.scrollSpeed - 0.00005 * dt)
            target_volume = 1.0
        else:
            self.shakeIntensity = 0
            globals.scrollSpeed = min(self.drivingSpeed, globals.scrollSpeed + 0.00005 * dt)
            target_volume = 0.0

        # Gradually adjust the offroad sound volume without restarting the sound.
        current_volume = self.offroad_channel.get_volume()
        fade_rate = dt / self.fade_time
        if current_volume < target_volume:
            new_volume = min(current_volume + fade_rate, target_volume)
        else:
            new_volume = max(current_volume - fade_rate, target_volume)
        self.offroad_channel.set_volume(new_volume)

        self.shake(dt)

        self.image = pygame.transform.rotate(self.originalImage, -self.angle)
        self.realRect = self.image.get_rect(center=self.realRect.center)
        self.collider.center = self.realRect.center

    def shake(self, dt):
        if self.shakeIntensity > 0:
            random.seed(pygame.time.get_ticks())
            offsetX = random.uniform(-1, 1) * self.shakeIntensity
            offsetY = random.uniform(-1, 1) * self.shakeIntensity
            self.rect.center = self.realRect.center + pygame.Vector2(offsetX, offsetY)
        else:
            self.rect.center = self.realRect.center

    def handleInput(self, dt):
        targetX, _ = globals.drunkCursorPos
        acceleration = 0.00025
        damping = 0.9
        threshold = 0.01

        force = (targetX - self.realRect.centerx) * acceleration
        self.velocityX = max(-0.5, min(0.5, force * dt))
        self.velocityX *= damping
        if abs(self.velocityX) < threshold:
            self.velocityX = 0

        self.realRect.centerx += self.velocityX * dt

    def onCrash(self):
        print("crash")
        if not globals.DEBUG:
            self.engine_channel.stop()
            self.rect.topleft = (-50, 1)
            self.realRect.topleft = (-50, 0)
            self.endGameCallback()
            pygame.mixer.Sound("assets/sounds/crash.mp3").play()
            self.kill()
        else:
            pygame.mixer.Sound("assets/sounds/crash.mp3").play()
