import pygame
from spritesheet_functions import *
from game_globals import *

class Game_Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, sprite, sprite_use, sprite_flip):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        if sprite_use == True:
            sprite_sheet = SpriteSheet(sprite)
            if sprite_flip:
                self.image = load_sprites(sprite_sheet,1,1,width,height,True)[0]
            else:
                self.image = load_sprites(sprite_sheet,1,1,width,height,False)[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Background(Game_Object):
    def __init__(self, x, y, width, height, color, sprite, sprite_use, sprite_flip):
        super().__init__(x, y, width, height, color, sprite, sprite_use, sprite_flip)


class Obstacle(Game_Object):
    def __init__(self, x, y, width, height, color, sprite, sprite_use, sprite_flip):
        super().__init__(x, y, width, height, color, sprite, sprite_use, sprite_flip)


class Passable_Object(Game_Object):
    def __init__(self, x, y, width, height, color, sprite, sprite_use, sprite_flip):
        super().__init__(x, y, width, height, color, sprite, sprite_use, sprite_flip)


class Breakable_Object(Game_Object):
    def __init__(self, x, y, width, height, color, sprite, sprite_use, sprite_flip, collapsing):
        super().__init__(x, y, width, height, color, sprite, sprite_use, sprite_flip)

        self.hits = 30
    
        self.collapsing = collapsing

    def get_position(self):
        return (self.rect.x, self.rect.y, self.rect.w, self.rect.h)


class Item(Game_Object):
    def __init__(self, x, y, width, height, color, sprite, sprite_use, sprite_flip, item_type):
        super().__init__(x, y, width, height, color, sprite, sprite_use, sprite_flip)

        self.item_type = item_type

        sprite_sheet = SpriteSheet(sprite)
        self.item_frames = load_sprites(sprite_sheet,5,4,28,22,False)
        self.image = self.item_frames[0]
        self.frame_count = 0
    
    def update(self):
        #if self._x == 0 and self._y == 1:
        self.frame_count += 1
        if self.frame_count == 20:
            self.frame_count = 0                
        self.image = self.item_frames[self.frame_count]

class Hitbox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
    
        self.image = pygame.Surface([width, height])
        self.image.fill(red)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
