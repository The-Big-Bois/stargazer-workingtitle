import pygame
import numpy as np
import os 
from spritesheet_functions import *
from game_objects import *
from game_rooms import *
from game_globals import *
from game_player import *


def main():

    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption('Stargazer (working title)')


    # ~~~ Objects ~~~

    player = Player(start_pos,496)
    

    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)

    rooms = []

    room = Room1(player)
    rooms.append(room)

    room = Room2(player)
    rooms.append(room)

    room = Room3(player)
    rooms.append(room)

    current_room_no = 0
    current_room = rooms[current_room_no]
    player.room = current_room


    # ~~~ Main Loop ~~~

    done = False
    clock = pygame.time.Clock()

    frames_current = 0

    while not done:
        #frames_current += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.jump()
                if event.key == pygame.K_a:
                    player.go_left()
                if event.key == pygame.K_d:
                    player.go_right()
                if event.key == pygame.K_SPACE:
                    player.attack(movingsprites)

                if event.key == pygame.K_LSHIFT:
                    player.dodge()
                if event.key == pygame.K_TAB:
                    player.toggle_gear()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player._x < 0:
                    player.stop()
                if event.key == pygame.K_d and player._x > 0:
                    player.stop()
                if event.key == pygame.K_SPACE:
                    movingsprites.remove(player.hitbox)
               

        movingsprites.update()
        current_room.update()
    


        # ~~~ Game Logic ~~~
        world_shift_enable = True
        altitude_shift_enable = True


        # If player has just entered a room, shift_world will be disabled
        if player.rect.left >= 120 and player.rect.right <= 500:
            world_shift_enable = True
        if player.rect.top >= 75 and player.rect.bottom <= 575:
            altitude_shift_enable = True 


        # If the player gets near the right side, shift the world to the left -x
        if player.rect.right >= 500 and world_shift_enable:
            if current_room.world_shift > current_room.level_end:
                diff = player.rect.right - 500
                player.rect.right = 500
                current_room.shift_world(-diff)

        # If the player gets near the bottom, shift the world up -y
        if player.rect.bottom >= 570 and altitude_shift_enable:
            if current_room.altitude_shift > current_room.level_low:
                diff = 570 - player.rect.bottom
                player.rect.bottom = 570
                current_room.shift_altitude(diff)

        # If the player gets near the left side, shift the world to the right +x
        if player.rect.left <= 120 and world_shift_enable:
            if current_room.world_shift < current_room.level_beg:
                diff = 120 - player.rect.left
                player.rect.left = 120
                current_room.shift_world(diff)

        # If the player gets near the top, shift the world down +y
        if player.rect.top <= 75 and altitude_shift_enable:
            if current_room.altitude_shift < current_room.level_height:
                diff = player.rect.top - 75
                player.rect.top = 75
                current_room.shift_altitude(-diff)
                

        # If the player exits the screen on either side, change level
        if player.rect.x < -44:
            world_shift_enable = False
            if current_room_no <= len(rooms)-1:
                current_room_no -= 1
                current_room = rooms[current_room_no]
                player.room = rooms[current_room_no]
                player.rect.x = 755
        if player.rect.x > 801:
            world_shift_enable = False
            if current_room_no < len(rooms)-1:
                current_room_no += 1
                current_room = rooms[current_room_no]
                player.room = rooms[current_room_no]
                player.rect.x = 1
            else:
                current_room_no = 0
                current_room = rooms[current_room_no]
                player.room = rooms[current_room_no]
                player.rect.x = 1

        
        # ~~~ Drawing ~~~

        screen.fill((0, 0, 0))
        
        current_room.draw(screen)
        movingsprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)  

        # ~~~ End Drawing ~~~      

if __name__ == "__main__":
    main()
