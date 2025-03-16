import pygame, os

carTextures = {}
groundTextures = {}
roadTextures = {}

def loadLevelTextures():
    global groundTextures, roadTextures
    groundTextures = loadTextureDictFromFolder("assets/ground/")
    roadTextures = loadTextureDictFromFolder("assets/road/")

def loadCarTextures(path="./assets/cars/"):
    """Loads all car textures from a given directory into carTextures dictionary."""
    for filename in os.listdir(path):  # Loop through files in the directory
        if filename.endswith(".png"):  # Ensure it's an image file
            car_name = os.path.splitext(filename)[0]  # Remove file extension
            carTextures[car_name] = pygame.image.load(os.path.join(path, filename)).convert_alpha()
            carTextures[car_name] = pygame.transform.scale(carTextures[car_name], (carTextures[car_name].get_rect().width*1.5, carTextures[car_name].get_rect().height*1.5))


def loadTextureDictFromFolder(path):
    """Loads all images from a folder into a dictionary as pygame surfaces."""
    texture_dict = {}

    # Ensure the folder exists
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Folder not found: {path}")

    # Loop through all files in the directory
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)

        # Only load valid image files
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            # Load the texture and store it in the dictionary
            texture_name = os.path.splitext(filename)[0]  # Remove extension
            texture_dict[texture_name] = pygame.image.load(file_path).convert_alpha()

    return texture_dict
