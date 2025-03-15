screen_size = (0,0)
drunkCursorPos = (0,0)

def scaleMousePos(pos):
    return (pos[0] * (640/screen_size[0]), pos[1] * (360/screen_size[1]))
