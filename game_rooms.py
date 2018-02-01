import pygame
from game_globals import *
from game_objects import *
from game_character import *
from sprite_sheets import *
from game_ai import *


class Room(object):
    """Base class for all rooms. """

    def __init__(self, player):
        self.background = pygame.sprite.Group()
        self.background_layer = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        self.passobject_list = pygame.sprite.Group()
        self.breakables = pygame.sprite.Group()
        self.items = pygame.sprite.Group()    
        self.enemy_sprites = pygame.sprite.Group()        
        self.player = player
    
        # How far this world has been scrolled left/right
        self.world_shift = 0
        # Up/down
        self.altitude_shift = 0

    
    def update(self):
        self.background.update()
        self.background_layer.update()
        self.platform_list.update()
        self.passobject_list.update()
        self.items.update()
        self.breakables.update()
        self.enemy_sprites.update()

    def draw(self, screen):

        #screen.fill(black)

        self.background.draw(screen)
        self.background_layer.draw(screen)
        self.platform_list.draw(screen)
        self.passobject_list.draw(screen)
        self.items.draw(screen)
        self.breakables.draw(screen)
        self.enemy_sprites.draw(screen)
    
    def shift_world(self, shift_x):

        # Keep track of the shift amount    
        self.world_shift += shift_x

        #go through all sprites and shift
        for layer in self.background_layer:
            layer.rect.x += shift_x/4
        for platform in self.platform_list:
            platform.rect.x += shift_x
        for passobject in self.passobject_list:
            passobject.rect.x += shift_x
        for item in self.items:
            item.rect.x += shift_x 
        for breakable in self.breakables:
            breakable.rect.x += shift_x   
        for enemy in self.enemy_sprites:
            enemy.rect.x += shift_x

    def shift_altitude(self, shift_y):

        # Keep track of the shift amount    
        self.altitude_shift += shift_y

        #go through all sprites and shift
        for platform in self.platform_list:
            platform.rect.y += shift_y
        for passobject in self.passobject_list:
            passobject.rect.y += shift_y
        for item in self.items:
            item.rect.y += shift_y
        for breakable in self.breakables:
            breakable.rect.y += shift_y    
        for enemy in self.enemy_sprites:
            enemy.rect.y += shift_y


class Room1(Room):
    def __init__(self,player):
        Room.__init__(self, player)

        # Stops scrolling after reaching these values
        self.level_end = 0
        self.level_beg = 0
        self.level_height = 150
        self.level_low = 0
        
        self.background.add(Background(0,0,800,600,gray,"moone_ver_3.png",True,False))
                    #reminder[locationx,y,sizex,y]
        obstacles = [[-20,570,1290,40,green,"floor.png",False,False],
                    [100,-200,20,726,green,"wall.png",False,False],
                    [750,-200,20,676,green,"wall.png",False,False],
                    [700,476,100,20,green,"wall.png",False,False],
                    [650,370,100,20,red,"sturdy_branch_swapped.gif",True,True],
                    [125,-20,100,20,red,"sturdy_branch_swapped.gif",True,True],
                    [125,170,100,20,red,"sturdy_branch_swapped.gif",True,True],
                    [230,270,100,20,red,"sturdy_branch_swapped.gif",True,False],
                    [320,370,100,20,red,"sturdy_branch_swapped.gif",True,False],
                    [230,470,100,20,red,"sturdy_branch_swapped.gif",True,False],
                    [310,80,100,20,red,"sturdy_branch_swapped.gif",True,False]]
        
        passable_objects = [[120,-997,300,1600,gray,"phat_tree_2.gif",True,False],
                            #[220,-20,10,20,gray,"branch.png",False,False],
                            #[220,170,10,20,gray,"branch.png",False,False],
                            #[310,370,10,20,gray,"branch.png",False,False],
                            [650,370,100,20,red,"sturdy_branch_swapped.gif",True,True],
                            [120,-20,100,20,red,"sturdy_branch_swapped.gif",True,True],
                            [120,170,100,20,red,"sturdy_branch_swapped.gif",True,True],
                            [230,270,100,20,red,"sturdy_branch_swapped.gif",True,False],
                            [320,370,100,20,red,"sturdy_branch_swapped.gif",True,False],
                            [230,470,100,20,red,"sturdy_branch_swapped.gif",True,False],
                            [310,80,100,20,red,"sturdy_branch_swapped.gif",True,False]]

        breakable_objects = [[700,496,20,74,brown,"chest_battered.png",False,False,False],
                            #[600,516,20,54,brown,"chest_battered.png",False,False,False],
                            #[620,516,80,20,brown,"chest_battered.png",False,False,False],
                            [100,496,20,74,brown,"door.png",False,False,False],
                            [500,300,100,20,brown,"breaking_branch.png",False,False,True],
                            [500,195,100,20,brown,"breaking_branch.png",False,False,True],
                            [630,533,65,37,brown,"chest_battered.gif",True,False,True]]

        enemies = [[650,292,3,2,bandit_sprites,sprite_sheet_list_names,bandit_sheet_info,False,bandit_ai,self.player]]

        #items = [[772,454,20,28, "cloak", "red_poncho_spritesheet.png"]]
        items = [[645,545,20,28,gray,"red_poncho_spritesheet.png",True,False,"cloak_01"],
                [155,-45,20,28,gray,"blue_poncho_spritesheet.png",True,False,"cloak_02"]]
        
        #make following for-loop into function
        for item in obstacles:
            obst = Obstacle(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7])
            self.platform_list.add(obst)
        
        for item in passable_objects:
            passobj = Passable_Object(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7])
            self.passobject_list.add(passobj)

        for item in breakable_objects:
            breakobj = Breakable_Object(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8])
            self.breakables.add(breakobj)
        
        for item in enemies:
            enemy = Enemy(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9])
            self.enemy_sprites.add(enemy)
            enemy.room = self


        for pickup in items:
            item = Item(pickup[0], pickup[1], pickup[2], pickup[3], pickup[4], pickup[5],pickup[6],pickup[7],pickup[8])
            self.items.add(item)

class Room2(Room):
    def __init__(self, player):
        Room.__init__(self, player)

        # World stops scrolling after reaching these values
        self.level_end = -500
        self.level_beg = 0
        self.level_height = 0
        self.level_low = 0

        self.background.add(Background(0,0,800,600,gray,"moone_ver_3.png",True,False))
        self.background_layer.add(Background(0,0,1600,600,gray,"new_tree_scroll_large.gif",True,False))

        obstacles = [[-20,570,496,40,green,"floor.png",False,False],
                    [550,570,770,40,green,"floor.png",False,False],
                    [650,465,100,20,turqoise,"sturdy_branch_swapped.png",True,True]]

        enemies = [[550,492,3,2,bandit_sprites,sprite_sheet_list_names,bandit_sheet_info,False,bandit_ai,self.player]]
        #x, y, walk_speed, air_speed, sprite_sheet_list, sprite_sheet_list_names, patrol, AI, player

        for item in obstacles:
            obst = Obstacle(item[0], item[1], item[2],item[3],item[4],item[5],item[6],item[7])
            self.platform_list.add(obst)

        for item in enemies:
            enemy = Enemy(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9])
            self.enemy_sprites.add(enemy)
            enemy.room = self


class Room3(Room):
    def __init__(self, player):
        Room.__init__(self, player)

        # Stops scrolling after reaching these values
        self.level_end = -500
        self.level_beg = 0
        self.level_height = 0
        self.level_low = 0

        self.background.add(Background(0,0,800,600,gray,"moone_ver_3.png",True,False))

        obstacles = [[-20,570,1340,40,green,"floor.png",False,False],
                    [650,530,100,20,green,"sturdy_branch_swapped.png",True,True]]

        for item in obstacles:
            obst = Obstacle(item[0], item[1], item[2],item[3],item[4],item[5],item[6],item[7])
            self.platform_list.add(obst)
