import pygame
from game_globals import *
from game_rooms import *
from game_objects import *
from spritesheet_functions import SpriteSheet
import numpy as np

class Character(pygame.sprite.Sprite):

    def __init__(self, x, y, walk_speed, air_speed, sprite_sheet_list, sprite_sheet_list_names,sheet_info):
        super().__init__()

        #self.direction 
        self.frame_count = 0

        # animation_states will be a list of lists, every element
        # being a list of sprites for a given animation. first list
        # is the list of idle sprites, next list is the list of walking
        # sprites etc.
        self.animation_states = []
        self.animation_states_dict = {}
        self.sheet_info = sheet_info
        for sprite_sheets in sprite_sheet_list:
            sheet = SpriteSheet(sprite_sheets)
            self.animation_states.append(load_sprites(sheet, sheet_info[0], sheet_info[1], sheet_info[2], sheet_info[3], False))
            self.animation_states.append(load_sprites(sheet, sheet_info[0], sheet_info[1], sheet_info[2], sheet_info[3], True))
        for i in range(0,len(self.animation_states)):
            self.animation_states_dict[sprite_sheet_list_names[i]] = self.animation_states[i]
        #self.animation_states_dict["idle"][0]    
        self.animation_states_index = 1
        self.animation_current = self.animation_states[self.animation_states_index]
        self.image = self.animation_current[0]
        self.animation_lastframe = 0

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.character_width = 44
        self.character_height = 74
        self.position = np.array([self.rect.x,self.rect.y], float)
        self.character_in_air = False 

        self.move_speed = np.array([0,0], float)
        self.walk_speed = walk_speed
        self.air_speed = air_speed

        self.hitbox_group = pygame.sprite.Group()
        self.attack_box_group = pygame.sprite.Group()
        self.attack_status = False

        self.timer = 0

        self.dead = False

    def update(self):
        """ Update chracter position/state. """
        self.timer += 1
        self.calc_grav()

        if not self.dead:

            if self.direction == "L":
                if self.animation_states_index % 2 == 1:
                    self.animation_states_index -= 1
                self.animation_current = self.animation_states[self.animation_states_index]
            if self.direction == "R":
                if self.animation_states_index % 2 == 0:
                    self.animation_states_index += 1
                self.animation_current = self.animation_states[self.animation_states_index]
            self.animate(self.animation_current, self.sheet_info[0]*self.sheet_info[1], 2)
            
            if self.dodge_state:
                if self.timer > self.dodge_lasttime + self.dodge_duration:
                    self.dodge_state = False
                    self.direction = self.dodge_postdodge_direction
                    self.move_speed[0] = self.dodge_postdodge_speed
                    if self.dodge_postdodge_jump:
                        self.dodge_postdodge_jump = False
                        self.jump()
                    if self.dodge_postdodge_attack:
                        self.dodge_postdodge_attack = False

            # Hinder movement through obstacles
            
            # x
            self.rect.x += self.move_speed[0]
            obstacle_hit_list = pygame.sprite.spritecollide(self, self.room.platform_list, False)
            for obstacle in obstacle_hit_list:
                if self.move_speed[0] > 0:
                    self.rect.right = obstacle.rect.left
                else:
                    self.rect.left = obstacle.rect.right
            breakable_hit_list = pygame.sprite.spritecollide(self, self.room.breakables, False)
            for breakable in breakable_hit_list:
                if self.move_speed[0] > 0 and breakable.hits > 0:
                    self.rect.right = breakable.rect.left
                elif self.move_speed[1] <= 0 and breakable.hits > 0:
                    self.rect.left = breakable.rect.right
            
            # y
            self.rect.y += self.move_speed[1]
            obstacle_hit_list = pygame.sprite.spritecollide(self, self.room.platform_list, False)
            self.character_in_air = True
            for obstacle in obstacle_hit_list:
                if self.move_speed[1] > 0:
                    self.rect.bottom = obstacle.rect.top
                elif self.move_speed[1] < 0:
                    self.rect.top = obstacle.rect.bottom
                self.move_speed[1] = 0
                self.character_in_air = False
            breakable_hit_list = pygame.sprite.spritecollide(self, self.room.breakables, False)
            for breakable in breakable_hit_list:
                if self.move_speed[1] > 0 and breakable.hits > 0:
                    if breakable.collapsing == True:
                        breakable.hits -= 1
                    self.rect.bottom = breakable.rect.top
                elif self.move_speed[1] < 0 and breakable.hits > 0:
                    if breakable.collapsing == True:
                        breakable.hits -= 1
                        self.rect.top = breakable.rect.bottom
                elif breakable.hits <= 0:
                    position = breakable.get_position()
                    passobj = Passable_Object(position[0],position[1],position[2],position[3],gray,"empty.png",False,False)
                    self.room.passobject_list.add(passobj)
                    pygame.sprite.spritecollide(self, self.room.breakables, True)
                self.move_speed[1] = 0

            # Stick attack hitbox to character
            if self.attack_box is not None: 
                if self.direction == 'L':
                    self.attack_box.rect.x = self.rect.left-40 
                    self.attack_box.rect.y = self.rect.y+20
                elif self.direction == 'R':
                    self.attack_box.rect.x = self.rect.right
                    self.attack_box.rect.y =  self.rect.y+20
                elif self.direction == 'D':
                    self.attack_box.rect.x = self.rect.left+17 
                    self.attack_box.rect.y = self.rect.bottom

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.move_speed[1] == 0:
            self.move_speed[1] = 1
        else:
            self.move_speed[1] += 0.45

        if self.rect.bottom >= (screen_height + self.character_height) and self.move_speed[1] >= 0:
            self.move_speed[1] = 0
            self.rect.bottom = (screen_height + self.character_height)

    def animate(self, sprites, frames, time_per_frame):
        if self.timer > self.animation_lastframe + time_per_frame:
            self.animation_lastframe = self.timer
            self.frame_count += 1
            if self.frame_count == frames:
                self.frame_count = 0
            self.image = sprites[self.frame_count]

    def go_left(self):
        if self.dodge_state == False:
            self.direction = "L"
            if self.move_speed[1] >= 0:
                self.move_speed[0] = -1*self.walk_speed
            if self.character_in_air:
                self.move_speed[0] = -1*self.air_speed
        else:
            self.dodge_postdodge_direction = "L"
            if self.move_speed[1] >= 0:
                self.dodge_postdodge_speed = -1*self.walk_speed
            if self.character_in_air:
                self.dodge_postdodge_speed = -1*self.air_speed
            
    def go_right(self):
        if self.dodge_state == False:
            self.direction = "R"
            if self.move_speed[1] >= 0:
                self.move_speed[0] = self.walk_speed
            if self.character_in_air:
                self.move_speed[0] = self.air_speed
        else:
            self.dodge_postdodge_direction = "R"
            if self.move_speed[1] >= 0:
                self.dodge_postdodge_speed = self.walk_speed
            if self.character_in_air:
                self.dodge_postdodge_speed = self.air_speed   

    def stop(self):
        if self.dodge_state == False:
            self.move_speed[0] = 0
        else:
            self.dodge_postdodge_speed = 0 

    def attack(self,targets):
        if self.timer > self.attack_lastframe + self.attack_cooldown:
            self.attack_lastframe = self.timer
            if self.direction == "R":
                self.attack_box = Hitbox(self.rect.right, self.rect.y+20, 40, 10)
            elif self.direction == "L":
                self.attack_box = Hitbox(self.rect.left-40, self.rect.y+20, 40, 10)
            elif self.direction == "D":
                self.attack_box = Hitbox(self.rect.left+17, self.rect.bottom, 10, 40)
        print(targets.hit_points)
        if targets.hit_points <= 0:
            targets.dead = True
            print('You died.')


    def jump(self):
        """ Called when user hits jump. """
        if self.dodge_state == False:
            self.rect.y += 2
            platform_hit_list = pygame.sprite.spritecollide(self, self.room.platform_list, False)
            breakable_hit_list = pygame.sprite.spritecollide(self, self.room.breakables, False)
            self.rect.y -= 2

            if len(platform_hit_list) > 0 or len(breakable_hit_list) > 0 or self.rect.bottom >= 600:
                self.direction = "D"
                self.move_speed[1] = -9.5
        else:
            self.dodge_postdodge_jump = True

    def dodge(self):
        if self.dodge_state == False and self.character_in_air == False:
            if self.timer > self.dodge_lasttime + self.dodge_cooldown:
                if self.move_speed[0] != 0:
                    self.dodge_state = True
                    self.dodge_lasttime = self.timer
                    self.dodge_postdodge_direction = self.direction
                    self.dodge_postdodge_speed = self.move_speed[0]

                    if self.direction == "L":
                        self.move_speed[0] = -self.dodge_speed
                    elif self.direction == "R":
                        self.move_speed[0] = self.dodge_speed

#
#
#

class Player(Character):

    def __init__(self, x, y, walk_speed, air_speed, sprite_sheet_list, sprite_sheet_list_names,sheet_info):
        super().__init__(x, y, walk_speed, air_speed, sprite_sheet_list, sprite_sheet_list_names,sheet_info)

        self.direction = "R"

        self.cloak_list = [0]
        self.cloak_index = 0
        self.weapon_upgrade = 0

        self.dodge_state = False
        self.dodge_lasttime = 0
        self.dodge_cooldown = 20
        self.dodge_duration = 10
        self.dodge_speed = 10
        self.dodge_postdodge_speed = 0
        self.dodge_postdodge_direction = "R"
        self.dodge_postdodge_jump = False
        self.dodge_postdodge_attack = False

        self.attack_lastframe = 0
        self.attack_cooldown = 20
        self.hit_points = 100
        self.attack_box = None

    def update(self):
        super(Player, self).update()

        if self.direction == "R":
            self.hitbox = Hitbox(self.rect.x,self.rect.y,30,74)
            self.hitbox_group.add(self.hitbox)
        if self.direction == "L":
            self.hitbox = Hitbox(self.rect.x+14,self.rect.y,30,74)
            self.hitbox_group.add(self.hitbox)

        # enemy_collide_list = pygame.sprite.spritecollide(self.hitbox, self.room.enemy_sprites, False)
        # for enemy in enemy_collide_list:
        #     if self.move_speed[0] > 0:
        #         self.rect.right = enemy.rect.left
        #     else:
        #         self.rect.left = enemy.rect.right

        picked_items = pygame.sprite.spritecollide(self, self.room.items, True)
        for item in picked_items:
            self.item_pickup(item)

    def attack(self, movingsprites):
        if self.dodge_state == False:
            self.attack_status = True
            if self.timer > self.attack_lastframe + self.attack_cooldown:

                self.attack_lastframe = self.timer
                if self.direction == "R":
                    self.attack_box = Hitbox(self.rect.right, self.rect.y+20, 40, 10)
                elif self.direction == "L":
                    self.attack_box = Hitbox(self.rect.left-40, self.rect.y+20, 40, 10)
                elif self.direction == "D":
                    self.attack_box = Hitbox(self.rect.left+17, self.rect.bottom, 10, 40)

                enemy_hit = pygame.sprite.spritecollide(self.attack_box, self.room.enemy_sprites, False)
                breakable_hit = pygame.sprite.spritecollide(self.attack_box, self.room.breakables, False)

                for enemy in enemy_hit:
                    if enemy.attack_status == False:
                        enemy.hit_points -= 50
                        print(enemy.hit_points)
                        if enemy.hit_points <= 0:
                            enemy.dead = True
                            print('Victory achieved.')
                    else:
                        print('Block')

                for breakable in breakable_hit:
                    breakable.hits -= 10
                    if breakable.hits == 0:
                        position = breakable.get_position()
                        passobj = Passable_Object(position[0],position[1],position[2],position[3], gray,"empty.png",False,False)
                        self.room.passobject_list.add(passobj)
                        pygame.sprite.spritecollide(self.attack_box, self.room.breakables, True)
                movingsprites.add(self.attack_box)
            self.attack_status = False
        else:
            self.dodge_postdodge_attack = True

    def item_pickup(self, item):       
        cloaks = ["cloak_01","cloak_02","cloak_03"]
        sword_upgrades = ["whetstone_01","whetstone_02","whetstone_03"]
        
        if item.item_type in cloaks:
            if item.item_type == "cloak_01":
                self.animation_states_index = 2
                self.cloak_list.append(2)
                self.cloak_index = len(self.cloak_list)-1
            if item.item_type == "cloak_02":
                self.animation_states_index = 4
                self.cloak_list.append(4)
                self.cloak_index = len(self.cloak_list)-1

    def toggle_gear(self):
        if len(self.cloak_list) > 1:
            if self.cloak_index < len(self.cloak_list)-1:
                self.cloak_index += 1
            else:
                self.cloak_index = 0
            self.animation_states_index = self.cloak_list[self.cloak_index]

#
#
#

class Enemy(Character):

    def __init__(self, x, y, walk_speed, air_speed, sprite_sheet_list, sprite_sheet_list_names, sheet_info, patrol, AI, player):
        super().__init__(x, y, walk_speed, air_speed, sprite_sheet_list, sprite_sheet_list_names, sheet_info)

        # Player attribute is used for referencing to player character
        self.patrol = patrol
        self.AI = AI
        self.player = player

        self.walk_speed = AI['move_speed']
        self.direction = 'L'

        self.dodge_state = False
        self.dodge_lasttime = 0
        self.dodge_cooldown = 20
        self.dodge_duration = 10
        self.dodge_speed = 10
        self.dodge_postdodge_speed = 0
        self.dodge_postdodge_direction = "R"
        self.dodge_postdodge_jump = False
        self.dodge_postdodge_attack = False

        self.attack_lastframe = 0
        self.attack_cooldown = 20
        self.detection = False
        self.in_attack_range = False
        self.attack_box = None

        self.hit_points = AI['hp']

        self.room = None
        

    def update(self):
        super(Enemy, self).update()

        if not self.dead:
            # player_collide_list = pygame.sprite.spritecollide(self, self.player.hitbox_group, False)
            # if self.move_speed[0] > 0:
            #     self.rect.right = self.player.rect.left
            #     self.stop()
            # else:
            #     self.rect.left = self.player.rect.right
            #     self.stop()

            # Player position references (shortest distance):
            pler = abs(self.player.rect.left - self.rect.right)
            elpr = abs(self.rect.left - self.player.rect.right)
            pteb = abs(self.player.rect.top - self.rect.bottom)
            etpb = abs(self.rect.top - self.player.rect.bottom)
            etpt = abs(self.rect.top - self.player.rect.top)
            min_x = min(pler, elpr)
            min_y = min(pteb, etpb)

            if min_x <= self.AI['detection_x'] and min_y <= self.AI['detection_y']:
                self.detection = True

            if min_x > self.AI['aggro_x'] or min_y > self.AI['aggro_y']:
                self.detection = False
                self.stop()

            # print(self.in_attack_range)
            # print(self.detection)

            if min_x <= self.AI['attack_range_x'] and etpt <= self.AI['attack_range_y']:
                self.in_attack_range = True
            if min_x > self.AI['attack_range_x'] or etpt > self.AI['attack_range_y']:
                self.in_attack_range = False

            if self.detection == True and self.in_attack_range == False:
                if elpr < pler:
                    self.go_left()
                if pler < elpr:
                    self.go_right()
            
            if self.in_attack_range:
                self.stop()
                self.attack_status = True
                if not self.player.dead:
                    self.attack(self.player)
                    if self.attack_box is not None:
                        target_hit = pygame.sprite.spritecollide(self.attack_box, self.player.hitbox_group, False)
                        if len(target_hit) > 0:
                            self.player.hit_points -= 15
                #print(self.player.hit_points)
                self.attack_status = False
