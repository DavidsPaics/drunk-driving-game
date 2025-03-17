import random
import time
import pygame, globals, TextureManager
import math

import pygame
import random
import globals

class Car(pygame.sprite.Sprite):
    def __init__(self, texture, speed, laneX, *groups):
        super().__init__(*groups)
        self.image = texture
        self.rect = self.image.get_rect()
        self.max_speed = speed
        self.speed = speed
        self.laneX = laneX
        self.rect.center = (laneX, 0 - self.rect.height)


    def update(self, dt):
        new_centery = self.rect.centery + self.speed * dt + globals.scrollSpeed * dt

        self.rect.center = (self.laneX, new_centery)

            


class TrafficManager:
    def __init__(self, screen):
        self.destinationSurface = screen

        self.traffic = [] 
        self.timerStart = time.time()
        self.timerDuration = random.randint(globals.oppositeSpawnMinTime,globals.oppositeSpawnMaxTime)/1000
        self.timer2Start = time.time()
        self.timer2Duration = random.randint(globals.oppositeSpawnMinTime,globals.oppositeSpawnMaxTime)/1000
        self.timer3Start = time.time()
        self.timer3Duration = random.randint(globals.sameSpawnMinTime,globals.sameSpawnMaxTime)/1000
        self.timer4Start = time.time()
        self.timer4Duration = random.randint(globals.sameSpawnMinTime,globals.sameSpawnMaxTime)/1000

        self.lastRoadRageIncident = time.time()
    
    def spawnCar(self, lane):
        carBase = random.choice(list(TextureManager.carTextures.values()))
        speed = random.randint(5, 20)/100

        if lane in [350,420]:
            speed = random.randint(-10, -3)/100
        else:
            carBase = pygame.transform.flip(carBase,0,1)

        newcar = Car(carBase, speed, lane)

        self.traffic.append(newcar)
    
    
    def update(self, dt):
        if time.time() - self.timerStart > self.timerDuration:
            self.spawnCar(210)
            self.timerStart = time.time()
            self.timerDuration = random.randint(globals.oppositeSpawnMinTime,globals.oppositeSpawnMaxTime)/1000
        if time.time() - self.timer2Start > self.timer2Duration:
            self.spawnCar(280)
            self.timer2Start = time.time()
            self.timer2Duration = random.randint(globals.oppositeSpawnMinTime,globals.oppositeSpawnMaxTime)/1000

        if time.time() - self.timer3Start > self.timer3Duration:
            self.spawnCar(350)
            self.timer3Start = time.time()
            self.timer3Duration = random.randint(globals.sameSpawnMinTime,globals.sameSpawnMaxTime)/1000
        if time.time() - self.timer4Start > self.timer4Duration:
            self.spawnCar(420)
            self.timer4Start = time.time()
            self.timer4Duration = random.randint(globals.sameSpawnMinTime,globals.sameSpawnMaxTime)/1000

        rprect = globals.player.collider
        bgrect = pygame.rect.Rect(rprect.x-35,rprect.y-35,rprect.width+35,rprect.height+35)
        for car in self.traffic:

            if bgrect.colliderect(car.rect):
                if time.time() - self.lastRoadRageIncident > 2:
                    globals.notificationManager.showNotification("Near miss: +0.20$")
                    globals.player.money+=20
                    pygame.mixer.Sound(f"assets/sounds/horns/{random.randint(1,6)}.mp3").play()
                    self.lastRoadRageIncident = time.time()

            if rprect.colliderect(car.rect):
                globals.player.onCrash()
            if car.rect.y>360:
                self.traffic.remove(car)

            car.update(dt)
    
    def draw(self):
        for car in self.traffic:
            self.destinationSurface.blit(car.image, car.rect.topleft)
            if globals.DEBUG:
                pygame.draw.rect(self.destinationSurface, (255,0,0), car.rect, 1)
