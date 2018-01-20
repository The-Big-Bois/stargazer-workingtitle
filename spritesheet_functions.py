"""
This module is used to pull individual sprites from sprite sheets.
"""
import pygame
import os
 
class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
 
    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """
 
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(os.path.join("sprites", file_name)).convert()
 
 
    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """
 
        # Create a new blank image
        image = pygame.Surface([width, height]).convert()
 
        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
 
        # Assuming black works as the transparent color
        image.set_colorkey((0,0,0))
 
        # Return the image
        return image

def load_sprites(sprite_sheet, rows, columns, sprite_width, sprite_height, vertical_flip):
    """ Take images from spritesheet and append into a list. """
    frame_list = [] 
    for y in range(rows):
        for x in range(columns):
            image = sprite_sheet.get_image(x*sprite_width, y*sprite_height, sprite_width, sprite_height)
            if vertical_flip:
                image = pygame.transform.flip(image, True, False)
            frame_list.append(image)        
    return frame_list
