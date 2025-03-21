import random
import pygame, time
pygame.init()
pygame.mixer.init()


from Game import Game

screen =  pygame.display.set_mode((0, 0))
game = Game(screen)

game.run()

run = True

buzzStart = time.time()

while(time.time() - buzzStart < 2 and run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    screen.fill((random.randint(0,255), random.randint(0,255) ,random.randint(0,255)))

    pygame.display.flip()

