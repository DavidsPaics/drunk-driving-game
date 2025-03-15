import pygame, os

carTextures = {}

def loadCarTextures(path="./assets/cars/"):
    print("loadaing car textures")
    """Loads all car textures from a given directory into carTextures dictionary."""
    for filename in os.listdir(path):  # Loop through files in the directory
        if filename.endswith(".png"):  # Ensure it's an image file
            car_name = os.path.splitext(filename)[0]  # Remove file extension
            carTextures[car_name] = pygame.image.load(os.path.join(path, filename)).convert_alpha()
    
    print(carTextures)
