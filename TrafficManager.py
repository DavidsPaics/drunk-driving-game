import random
import time
import pygame, globals, TextureManager
import math

import pygame
import random
import globals

class Car(pygame.sprite.Sprite):
    def __init__(self, texture, isGoingUp, speed, laneX, *groups):
        super().__init__(*groups)
        self.image = texture
        self.rect = self.image.get_rect()
        self.isGoingUp = isGoingUp
        self.max_speed = speed
        self.speed = speed
        self.laneX = laneX
        if self.isGoingUp:
            self.rect.center = (laneX, 360)
        else:
            self.rect.center = (laneX, 0 - self.rect.height)


    def update(self, dt):
        if self.isGoingUp:
            new_centery = self.rect.centery - self.speed * dt + globals.scrollSpeed * dt
        else:
            new_centery = self.rect.centery + self.speed * dt + globals.scrollSpeed * dt

        self.rect.center = (self.laneX, new_centery)

            


class TrafficManager:
    def __init__(self, screen):
        self.destinationSurface = screen

        self.traffic = [] 
        self.timerStart = time.time()
        self.timerDuration = random.randint(0,2000)/1000
        self.timer2Start = time.time()
        self.timer2Duration = random.randint(0,2000)/1000
    
    def spawnCar(self, laneChoice=None):
        carBase = pygame.transform.flip(random.choice(list(TextureManager.carTextures.values())), 0, 1)
        goingUp = False
        speed = random.randint(5, 20)/100

        if not goingUp:
            lane = random.choice([210, 280])
        
        if laneChoice != None:
            lane = laneChoice

        newcar = Car(carBase, goingUp, speed, lane)

        self.traffic.append(newcar)
    
    
    def update(self, dt):
        if time.time() - self.timerStart > self.timerDuration:
            self.spawnCar(210)
            self.timerStart = time.time()
            self.timerDuration = random.randint(1000,5000)/1000
        if time.time() - self.timer2Start > self.timer2Duration:
            self.spawnCar(280)
            self.timer2Start = time.time()
            self.timer2Duration = random.randint(1000,5000)/1000

        for car in self.traffic:
            if (not car.isGoingUp and car.rect.y>360):
                self.traffic.remove(car)

            car.update(dt)
    
    def draw(self):
        for car in self.traffic:
            self.destinationSurface.blit(car.image, car.rect.topleft)
