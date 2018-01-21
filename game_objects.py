import pygame
from spritesheet_functions import *

class Background(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, sprite):
        super().__init__()

        spritesheet = SpriteSheet(sprite)
        self.image = load_sprites(spritesheet,1,1,width,height,False)[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, sprite, sprite_use, sprite_flip):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        if sprite_use == True:
            sprite_sheet = SpriteSheet(sprite)
            if sprite_flip:
                self.image = load_sprites(sprite_sheet,1,1,100,20,True)[0]
            else:
                self.image = load_sprites(sprite_sheet,1,1,100,20,False)[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Passable_Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Breakable_Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, collapsing):
        super().__init__()

        self.color = color

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.w = width
        self.rect.h = height

        self.hits = 30
    
        self.collapsing = collapsing

    def get_position(self):
        return (self.rect.x, self.rect.y, self.rect.w, self.rect.h)

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, item_type, sprite):
        super().__init__()

        self.item_type = item_type

        sprite_sheet = SpriteSheet(sprite)
        self.item_frames = load_sprites(sprite_sheet,5,4,28,22,False)
        
        self.image = self.item_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.w = width
        self.rect.h = height

        self.frame_count = 0
    
    def update(self):
        #if self._x == 0 and self._y == 1:
        self.frame_count += 1
        if self.frame_count == 20:
            self.frame_count = 0                
        self.image = self.item_frames[self.frame_count]


    
