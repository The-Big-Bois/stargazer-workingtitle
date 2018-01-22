import pygame
from game_globals import *
from game_rooms import *
from game_objects import *
from spritesheet_functions import SpriteSheet
import numpy as np

class Character(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.direction 
        self.frame_count = 0

        sprite_sheet = SpriteSheet("file_name.png")
        self.sprite_frames = load_sprites(sprite_sheet,rows,columns,sprite_width,sprite_height,flip)
        self.image = self.sprite_frames[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.position = np.array([self.rect.x,self.rect.y])

        self.move_speed = np.array([0,0])
        self.walk_speed = 3.5
        self.air_speed = 2

        self.hitbox = None
        self.attack_box = None

        self.timer = 0

    def update(self):
        """ Update chracter position/state. """
        self.timer += 1
        self.calc_grav()
        self.position += self.move_speed 

        # Hinder movement through obstacles
        obstacle_hit_list = pygame.sprite.spritecollide(self, self.room.platform_list, False)
        breakable_hit_list = pygame.sprite.spritecollide(self, self.room.breakables, False)
        self.character_in_air = True
        for obstacle in obstacle_hit_list:
            if self.move_speed[0] > 0:
                self.rect.right = obstacle.rect.left
            if self.move_speed[0] < 0:
                self.rect.left = obstacle.rect.right
            if self.move_speed[1] > 0:
                self.rect.bottom = obstacle.rect.top
            if self.move_speed[1] < 0:
                self.rect.top = obstacle.rect.bottom
            self.move_speed[1] = 0
            self.character_in_air = False
        for breakable in breakable_hit_list:
            if self.move_speed[0] > 0 and breakable.hits > 0:
                self.rect.right = breakable.rect.left
            if self.move_speed[0] < 0 and breakable.hits > 0:
                self.rect.left = breakable.rect.right
            if self.move_speed[1] > 0 and breakable.hits > 0:
                if breakable.collapsing:
                    breakable.hits -= 1
                self.rect.bottom = breakable.rect.top
            if self.move_speed[1] < 0 and breakable.hits > 0:
                if breakable.collapsing:
                    breakable.hits -= 1
                self.rect.top = breakable.rect.bottom
            elif breakable.hits <= 0:
                position = breakable.get_position()
                passable = Passable_Object(position[0],position[1],position[2],position[3],gray)
                self.room.passobject_list.add(passable)
                pygame.sprite.spritecollide(self, self.room.breakables, True)
            self.move_speed[1] = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.move_speed[1] == 0:
            self.move_speed[1] = 1
        else:
            self.move_speed[1] += 0.45

        if self.rect.bottom >= (screen_height+character_height) and self.move_speed[1] >= 0:
            self.move_speed[1] = 0
            self.rect.bottom = (screen_height+character_height)

    def go_left(self):
        self.direction = "L"
        if self.move_speed[1] >= 0:
            self.move_speed[0] = -1*self.walk_speed
        if self.character_in_air:
            self.move_speed[0] = -1*self.air_speed
        
    def go_right(self):
        self.direction = "R"
        if self.move_speed[1] >= 0:
            self.move_speed[0] = self.walk_speed
        if self.character_in_air:
            self.move_speed[0] = self.air_speed

    def stop(self):
        self.move_speed[0] = 0