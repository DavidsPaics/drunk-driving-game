import pygame
import math
import globals

class Cursor(pygame.sprite.Sprite):
    def __init__(self, glue_top=False):
        super().__init__()
        # Load the original image (with the bottle cap at (w/2, 0))
        original = pygame.image.load("assets/alcohol.png").convert_alpha()
        w, h = original.get_size()
        self.bottle_length = h  # Physical bottle length

        # Create a new surface double the size so that the bottle cap becomes the center.
        new_size = (2 * w, 2 * h)
        centered_image = pygame.Surface(new_size, pygame.SRCALPHA)
        centered_image.fill((0, 0, 0, 0))
        # The original cap is at (w/2, 0). We want it at the new surface's center (w, h).
        blit_pos = (w - (w / 2), h - 0)  # equals (w/2, h)
        centered_image.blit(original, (int(blit_pos[0]), int(blit_pos[1])))
        
        # Use this centered image as our new texture.
        self.original_image = centered_image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()

        # Option: if True, the top will be glued exactly to the cursor.
        self.glue_top = glue_top

        # --- Top (pivot) dynamics ---
        # Our pivot now is at the center of the new image (which is the bottle cap).
        self.top = pygame.Vector2(320, 180)  # Starting at center of 640x360.
        self.top_velocity = pygame.Vector2(0, 0)
        self.top_mass = 1
        self.top_stiffness = 50  # Adjust for responsiveness.
        self.top_damping = 0.9   # Damping to settle quickly.

        # --- Bottom (pendulum) dynamics ---
        # The bottom is free to swing with gravity.
        # Note: The physical bottle length remains the height of the original texture.
        self.length = self.bottle_length
        self.bottom = self.top + pygame.Vector2(0, self.length)
        self.bottom_velocity = pygame.Vector2(0, 0)
        self.gravity = 950         # Gravity in pixels/sec^2. 
        self.bottom_damping = 0.99 # Damping to simulate air resistance.

    def update(self, dt):
        # Convert dt from milliseconds to seconds.
        dt = dt / 1000.0

        # --- Update the top (pivot) dynamics ---
        target = pygame.Vector2(globals.scaleMousePos(pygame.mouse.get_pos()))
        if self.glue_top:
            self.top = target
            self.top_velocity = pygame.Vector2(0, 0)
        else:
            # Spring force: F = k*(target - current)
            force = (target - self.top) * self.top_stiffness
            acceleration = force / self.top_mass
            self.top_velocity += acceleration * dt
            self.top_velocity *= self.top_damping
            self.top += self.top_velocity * dt

        # --- Update the bottom (free swing) dynamics ---
        self.bottom_velocity.y += self.gravity * dt
        self.bottom += self.bottom_velocity * dt

        # Enforce the rod constraint: the distance from top to bottom equals self.length.
        diff = self.bottom - self.top
        current_length = diff.length()
        if current_length != 0:
            correction = (current_length - self.length) * (diff / current_length)
            self.bottom -= correction
            self.bottom_velocity -= correction / dt
        self.bottom_velocity *= self.bottom_damping
        # Snap to zero if very low to avoid jittery rotation.
        if self.bottom_velocity.length() < 0.05:
            self.bottom_velocity = pygame.Vector2(0, 0)

        # --- Determine the rotation ---
        # The bottle should point from the top (cap) to the bottom.
        diff = self.bottom - self.top
        angle = 90 - math.degrees(math.atan2(diff.y, diff.x))

        # --- Rotate the image about its center (the bottle cap) ---
        if abs(angle)>1:
            rotated_image = pygame.transform.rotate(self.original_image, angle)
            # With the bottle cap centered in our texture, we simply set the rotated image's center to self.top.
            rotated_rect = rotated_image.get_rect(center=(int(self.top.x), int(self.top.y)))
            self.image = rotated_image
            self.rect = rotated_rect
        else:
            self.image = self.original_image
            self.rect = self.original_image.get_rect(center=(int(self.top.x), int(self.top.y)))
