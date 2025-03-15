import random
import pygame, globals
import TextureManager


class LevelChunk(pygame.sprite.Sprite):
    def __init__(self, group, lastChunkOptions={"startingTile":True}):
        self.traffic = []
        self.options = self.generateChunk(lastChunkOptions)
        self.image = pygame.surface.Surface((640,360))
        self.rect = pygame.rect.Rect(0,0,640,360)
        self.scrollPos = -360
        self.summonedChunk = False
        super().__init__(group)
    
    def generateChunk(self,lastChunkOptions):
        if lastChunkOptions["startingTile"] == True:
            opts = {
                "startingTile":False,
                "ground": "grass",
                "ground_texture": TextureManager.groundTextures["grass"],
                "road": "highway2x2",
                "road_texture": TextureManager.roadTextures["highway2x2"],
                "groundStreak": 1,
                }
            return opts
        
        for _ in range(random.randint(0,5)):
            if random.randint(0,100)<=50:
                newcartex = TextureManager.carTextures["compact_"+random.choice(["red","blue","orange","red"])]
                newcartex = pygame.transform.scale(newcartex, (newcartex.get_rect().width*1.5, newcartex.get_rect().height*1.5))
                newcartex = pygame.transform.flip(newcartex, 0, 1)
                self.traffic.append({
                    "texture": newcartex,
                    "x": random.choice([190, 265]),
                    "startPoint": random.randint(-360-newcartex.get_rect().height,0-newcartex.get_rect().height)
                })
        
        possibleRoads = list(TextureManager.roadTextures.keys())

        ground = random.choice(self.getPossibleNextGrounds(lastChunkOptions))
        road = random.choice(possibleRoads)
        opts = {
            "startingTile":False,
            "ground": ground,
            "ground_texture": TextureManager.groundTextures[ground],
            "road": road,
            "road_texture": TextureManager.roadTextures[road],
            "groundStreak": (lastChunkOptions["groundStreak"]+1 if lastChunkOptions["ground"] == ground else 1),
        }
        
        return opts

    def update(self, dt):
        if self.scrollPos>0 and not self.summonedChunk:
            temp = LevelChunk(self.groups()[0], self.options) # TODO: Fix this piece of shit and get rifd of annoying gap. Also WTF... It is 3am and I dont know any more please help me.
            temp.scrollPos = self.scrollPos-360 #             BTW, fixed stupid gap here. but still, this ir garbage
            # print(self.scrollPos)
            temp.update(dt)
            self.summonedChunk = True
        
        if self.scrollPos>360:
            self.kill()
            return
        
        self.scrollPos += 0.15*dt

        self.rect.topleft = (0,self.scrollPos)
        self.image.blit(self.options["ground_texture"], (0,0))
        self.image.blit(self.options["road_texture"], (177, 0))

        for car in self.traffic:
            if self.scrollPos>=car["startPoint"]:
                self.image.blit(car["texture"], (car["x"], globals.map_value(self.scrollPos, car["startPoint"], 360, -car["texture"].get_rect().height, 360)))

    def getPossibleNextGrounds(self, lastChunkOptions):
        possibleRoads = list(TextureManager.roadTextures.keys())

        if lastChunkOptions["ground"] == "grass":
            if lastChunkOptions["groundStreak"]<=5:
                possibleGrounds = ["grass"]
            else:
                possibleGrounds = ["grass", "grass-sand"]

        elif lastChunkOptions["ground"] == "sand":
            if lastChunkOptions["groundStreak"]<=5:
                possibleGrounds = ["sand"]
            else:
                possibleGrounds = ["sand", "sand-grass"]

        elif lastChunkOptions["ground"] == "sand-grass":
            possibleGrounds = ["grass", "grass-sand"]

        elif lastChunkOptions["ground"] == "grass-sand":
            possibleGrounds = ["sand", "sand-grass"]

        return possibleGrounds