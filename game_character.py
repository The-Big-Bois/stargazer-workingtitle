import pygame
from game_globals import *
from game_rooms import *
from game_objects import *
from spritesheet_functions import SpriteSheet
import numpy as np

class Character(pygame.sprite.Sprite):

    def __init__(self, x, y, walk_speed, air_speed, sprite_sheet_list):
        super().__init__()

        self.direction 
        self.frame_count = 0

        # animation_states will be a list of lists, every element
        # being a list of sprites for a given animation. first list
        # is the list of idle sprites, next list is the list of walking
        # sprites etc.
        self.animation_states = []
        for sprite_sheets in sprite_sheet_list:
            self.animation_states.append(load_sprites(sprite_sheets,rows,columns,sprite_width,sprite_height,flip))
        self.animation_current = self.animation_states[0]
        self.image = self.animation_current[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.position = np.array([self.rect.x,self.rect.y])

        self.move_speed = np.array([0,0])
        self.walk_speed = walk_speed
        self.air_speed = air_speed

        self.hitbox = None
        self.attack_box = None

        self.timer = 0

    def update(self):
        """ Update chracter position/state. """
        self.timer += 1
        self.calc_grav()
        self.position += self.move_speed 
        self.animate(self.animation_current,24,2)

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

    def animate(self, sprites, frames, time_per_frame):
        if self.timer > self.animation_lastframe + time_per_frame:
            self.animation_lastframe = self.timer
            self.frame_count += 1
            if self.frame_count == frames:
                self.frame_count = 0
            self.image = self.sprites[self.frame_count]

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
        if self.direction == 'R':
            self.animation_current = self.animation_states[0]
        if self.direction == 'L':
            self.animation_current = self.animation_states[1]