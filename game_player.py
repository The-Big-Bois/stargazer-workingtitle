import pygame
from game_globals import *
from game_rooms import *
from game_objects import *
from spritesheet_functions import SpriteSheet

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()


        self.direction = "R"
        self.frame_count = 0

        sprite_sheet = SpriteSheet("idle_01b.png")
        # Load all the left facing images into a list
        self.idle_frames_l = load_sprites(sprite_sheet,4,6,44,74,False)
        # Load all the left facing images, then flip them to face right.
        self.idle_frames_r = load_sprites(sprite_sheet,4,6,44,74,True)
        
        self.image = self.idle_frames_r[0]


        #self.image = pygame.Surface([44, 74])
        #self.image.fill((255,100,0))  

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self._x = 0
        self._y = 0
        self.room = None

        self.cloak_list = [sprite_sheet]
        self.cloak_index = 0
        self.weapon_upgrade = 0

        self.hitbox = None

        self.timer = 0
        self.attack_lasttime = 0
        self.attack_cooldown = 20

        self.animation_idle_lasttime = 0
        self.animation_idle_cooldown = 2

        self.dodge_lasttime = 0
        self.dodge_cooldown = 60

    def update(self):
        """ Update player position. """
        self.timer += 1
        self.calc_grav()
       
        self.rect.x += self._x
        # pos = self.rect.x + self.room.world_shift
        # if self.direction == 'R':
        #     frame = (pos // 30) % len(self.idle_frames_r)
        #     self.image = self.idle_frames_r[frame]
        # else:
        #     frame = (pos // 30) % len(self.idle_frames_r)
        #     self.image = self.idle_frames_r[frame]

        # Animates idle state when player is not moving
        if self._x == 0 and self._y == 1:
            if self.timer > self.animation_idle_lasttime + self.animation_idle_cooldown:
                self.animation_idle_lasttime = self.timer
                self.frame_count += 1
                if self.frame_count == 24:
                    self.frame_count = 0
                if self.direction == 'R':
                    self.image = self.idle_frames_r[self.frame_count]
                if self.direction == 'L':
                    self.image = self.idle_frames_l[self.frame_count]

        # Hinder movement through obstacles.
        hit_list = pygame.sprite.spritecollide(self, self.room.platform_list, False)
        for obstacle in hit_list:
            if self._x > 0:
                self.rect.right = obstacle.rect.left
            else:
                self.rect.left = obstacle.rect.right

        # Breakables are given a number of hits, when they have hits left they act as
        # obstacles, when hits reach zero they are replaced by a passable object 
        break_list = pygame.sprite.spritecollide(self, self.room.breakables, False)
        for breakable in break_list:
            if self._x > 0 and breakable.hits > 0:
                self.rect.right = breakable.rect.left
            elif self._x <= 0 and breakable.hits > 0:
                self.rect.left = breakable.rect.right
              

        self.rect.y += self._y
        hit_list = pygame.sprite.spritecollide(self, self.room.platform_list, False)
        self._inair = True
        for obstacle in hit_list:
            if self._y > 0:
                self.rect.bottom = obstacle.rect.top
            elif self._y < 0:
                self.rect.top = obstacle.rect.bottom
            self._y = 0
            self._inair = False
        # Y for breakables
        break_list = pygame.sprite.spritecollide(self, self.room.breakables, False)
        for breakable in break_list:
            if self._y > 0 and breakable.hits > 0:
                if breakable.collapsing == True:
                    breakable.hits -= 1
                self.rect.bottom = breakable.rect.top
            elif self._y < 0 and breakable.hits > 0:
                if breakable.collapsing == True:
                    breakable.hits -= 1
                self.rect.top = breakable.rect.bottom
            elif breakable.hits <= 0:
                position = breakable.get_position()
                passobj = Passable_Object(position[0],position[1],position[2],position[3], gray)
                self.room.passobject_list.add(passobj)
                pygame.sprite.spritecollide(self, self.room.breakables, True)
            self._y = 0

        # Stick attack hitbox to player
        if self.hitbox is not None: 
            if self.direction == 'L':
                self.hitbox.rect.x = self.rect.left-40 
                self.hitbox.rect.y = self.rect.y+20
            elif self.direction == 'R':
                self.hitbox.rect.x = self.rect.right
                self.hitbox.rect.y =  self.rect.y+20
            elif self.direction == 'D':
                self.hitbox.rect.x = self.rect.left+17 
                self.hitbox.rect.y = self.rect.bottom

        # Remove picked up items from screen
        picked_items = pygame.sprite.spritecollide(self, self.room.items, True)
        for item in picked_items:
            self.item_pickup(item)
                   
    def calc_grav(self):
        if self._y == 0:
            self._y = 1
        else:
            self._y += 0.45

        if self.rect.bottom >= (600+74) and self._y >= 0:
            self._y = 0
            self.rect.bottom = (600+74)
            
    # jump height is roughly 105px
    def jump(self):
        """ Called when user hits jump. """

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.room.platform_list, False)
        breakable_hit_list = pygame.sprite.spritecollide(self, self.room.breakables, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or len(breakable_hit_list) > 0 or self.rect.bottom >= 600:
            self.direction = "D"
            self._y = -9.5
            

    def go_left(self):
        self.direction = "L"
        if self._y >= 0:
            self._x = -4
        if self._inair:
            self._x = -3
        

    def go_right(self):
        self.direction = "R"
        if self._y >= 0:
            self._x = 4
        if self._inair:
            self._x = 3

    def stop(self):
        self._x = 0


    def attack(self, movingsprites):
        if self.timer > self.attack_lasttime + self.attack_cooldown:

            self.attack_lasttime = self.timer
            if self.direction == "R":
                self.hitbox = Hitbox(self.rect.right, self.rect.y+20, 40, 10)
            elif self.direction == "L":
                self.hitbox = Hitbox(self.rect.left-40, self.rect.y+20, 40, 10)
            elif self.direction == "D":
                self.hitbox = Hitbox(self.rect.left+17, self.rect.bottom, 10, 40)

            enemy_hit = pygame.sprite.spritecollide(self.hitbox, self.room.enemy_sprites, False)
            breakable_hit = pygame.sprite.spritecollide(self.hitbox, self.room.breakables, False)

            for enemy in enemy_hit:
                if enemy.attack_status == False:
                    enemy.hp -= 1

            for breakable in breakable_hit:
                breakable.hits -= 10
                if breakable.hits == 0:
                    position = breakable.get_position()
                    passobj = Passable_Object(position[0],position[1],position[2],position[3], gray)
                    self.room.passobject_list.add(passobj)
                    pygame.sprite.spritecollide(self.hitbox, self.room.breakables, True)
            movingsprites.add(self.hitbox)

    def dodge(self):
        self.dodge == True

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.room.platform_list, False)
        breakable_hit_list = pygame.sprite.spritecollide(self, self.room.breakables, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or len(breakable_hit_list) > 0:
            if self.direction == "R":
                self.rect.right += 70
                obstacles = pygame.sprite.spritecollide(self, self.room.platform_list, False)
                breakables = pygame.sprite.spritecollide(self, self.room.breakables, False)
                self.rect.right -= 70
                if len(obstacles) == 0 and len(breakables) == 0:
                    self.rect.right += 70
            elif self.direction == "L":
                self.rect.left -= 70
                obstacles = pygame.sprite.spritecollide(self, self.room.platform_list, False)
                breakables = pygame.sprite.spritecollide(self, self.room.breakables, False)
                self.rect.left += 70
                if len(obstacles) == 0 and len(breakables) == 0:
                    self.rect.left -= 70 

    def item_pickup(self, item):       
        cloaks = ["cloak_01","cloak_02","cloak_03"]
        sword_upgrades = ["whetstone_01","whetstone_02","whetstone_03"]
        
        if item.item_type in cloaks:
            if item.item_type == "cloak_01":
                sprite_sheet = SpriteSheet("idle_01b_red.png")
            if item.item_type == "cloak_02":
                sprite_sheet = SpriteSheet("idle_01b_blue.png")
            self.cloak_list.append(sprite_sheet)
            self.cloak_index += 1
            self.idle_frames_l = load_sprites(sprite_sheet,4,6,44,74,False)
            self.idle_frames_r = load_sprites(sprite_sheet,4,6,44,74,True)
           
            if self.direction == 'R':
                self.image = self.idle_frames_r[0]
            elif self.direction == 'L':
                self.image = self.idle_frames_l[0]

    def toggle_gear(self):
        if len(self.cloak_list) > 1:
            if self.cloak_index < len(self.cloak_list)-1:
                self.cloak_index += 1
            else:
                self.cloak_index = 0
            sprite_sheet = self.cloak_list[self.cloak_index]
            self.idle_frames_l = load_sprites(sprite_sheet,4,6,44,74,False)
            self.idle_frames_r = load_sprites(sprite_sheet,4,6,44,74,True)
           
            if self.direction == 'R':
                self.image = self.idle_frames_r[0]
            elif self.direction == 'L':
                self.image = self.idle_frames_l[0]


class Hitbox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
    
        self.image = pygame.Surface([width, height])
        self.image.fill(red)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
