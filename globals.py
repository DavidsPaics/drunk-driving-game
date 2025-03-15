import os
import pygame

screen_size = (0,0)
drunkCursorPos = (0,0)

scrollSpeed = 0.15

def scaleMousePos(pos):
    return (pos[0] * (640/screen_size[0]), pos[1] * (360/screen_size[1]))

def map_value(value, in_min, in_max, out_min, out_max):
    """
    Maps a value from one range to another.
    
    :param value: The input value to map.
    :param in_min: The minimum of the input range.
    :param in_max: The maximum of the input range.
    :param out_min: The minimum of the output range.
    :param out_max: The maximum of the output range.
    :return: The mapped value in the new range.
    """
    # Normalize the input value to a 0-1 range
    normalized = (value - in_min) / (in_max - in_min)
    
    # Scale to the output range
    return out_min + (normalized * (out_max - out_min))
