import pygame;

from src.audio.sound_controller import Sound_Controller;


sound_controller = Sound_Controller();

# SFX files
player_hit_sfx = pygame.mixer.Sound('resources/sfx/player_hit_01.wav');
player_hit_02_sfx = pygame.mixer.Sound('resources/sfx/player_hit_02.wav');
player_bullet_sfx = pygame.mixer.Sound('resources/sfx/player_bullet_01.wav');

# TODO: player wall collision doesn't work very well, probably best to delete it and start over
# TODO: implement player health
# TODO: New player models?

class Player:
    def __init__(self, game_display, screen_size, player_img, player_num, location_x, location_y, current_room, wall_list, door_list):
        self.game_display = game_display;
        self.screen_size = screen_size;

        # Sprite sheets for when the player looks to the right and left
        self.player_sprite_right = pygame.image.load(player_img).convert_alpha();
        self.player_sprite_left = pygame.transform.flip(self.player_sprite_right, True, False).convert_alpha();
        self.player_sprite_right = pygame.transform.scale(self.player_sprite_right, (70, 70));
        self.player_sprite_left = pygame.transform.scale(self.player_sprite_left, (70, 70));

        # Number of the player
        self.player_num = player_num;

        self.location = [location_x, location_y];
        self.current_room = current_room;

        # Lists of objects the player can collide with
        self.level_wall_list = wall_list;
        self.level_door_list = door_list;

        self.move_direction_x = 0;
        self.move_direction_y = 0;
        self.current_x_direction = 1;

        # Keeps track of the player's bullets
        self.bullet_list = [];

        self.health = 10;
        self.speed = 10;

        self.player_moving = False;
        self.player_switch_rooms = False;

        # Used so the player has recovery time when damaged so he
        # doesn't get  annihilated immediately
        self.player_damage_cooldown = 0;


    def update_player(self):
        if(self.player_moving):
            self.move_player();

        # Check if the player is currently in a doorway
        doorway = self.player_entered_doorway();
        if(doorway != None):
            self.player_switch_rooms = True;

        # Controls the player's recovery time after being
        # hit by an enemy
        if(self.player_damage_cooldown > 0):
            self.player_damage_cooldown -= 1;

        self.update_bullets();

        self.draw_player();


    def update_bullets(self):
        # Takes care of deleting bullet objects when they've gone offscreen
        if (len(self.bullet_list) != 0):
            for bullet in self.bullet_list:
                if (bullet.location[0] > self.screen_size[0] or bullet.location[0] < 0):
                    del self.bullet_list[self.bullet_list.index(bullet)];
                    break;
                else:
                    bullet.update_bullet();


    def draw_player(self):
        #If the player is damaged he becomes a red box for a bit
        if(self.player_damage_cooldown > 30):
            pygame.draw.rect(self.game_display, (255, 0, 0), [self.location[0], self.location[1], 50, 50]);
        else:
            #The direction of the player determines which spritesheet to use
            if(self.current_x_direction == 1):
                self.game_display.blit(self.player_sprite_right, (self.location[0] - 10, self.location[1] - 10));
            elif(self.current_x_direction == -1):
                self.game_display.blit(self.player_sprite_left, (self.location[0] - 10, self.location[1] - 10));


    def move_player(self):
        # The player can't move for a bit after he's damaged
        if(self.player_damage_cooldown < 30):
            if(self.move_direction_x != 0):
                # If the player is colliding with an obstacle on the x-axis,
                # he cant move in that direction
                if not(self.player_obstacle_collision_x()):
                    self.location[0] += self.speed * self.move_direction_x;

            if(self.move_direction_y != 0):
                # If the player is colliding with an obstacle on the x-axis,
                # he cant move in that direction
                if not(self.player_obstacle_collision_y()):
                    self.location[1] += self.speed * self.move_direction_y;


    # TODO: redo this function and make it better
    def player_obstacle_collision_x(self):
        # So the player can't move beyond the edge of the screen
        if(self.location[0] >= self.screen_size[0] - 10 or
           self.location[0] <= 10):
            return True;

        for wall in self.level_wall_list[self.current_room]:
            # If the player is moving to the right and there is a wall in the way,
            # there is a collision and the function returns true
            # wall.x is in the center of the wall instead of the top left corner,
            # which is the reason for (wall.width / 2).
            if(self.move_direction_x == 1):
                if(self.location[0] < wall.x):
                    if(self.location[0] >= wall.x - 60 and
                       self.location[0] <= wall.x + (wall.width / 2)):
                        if(wall.y <= self.location[1] <= wall.y + wall.height):
                            return True;

            # If the player is moving to the left and there is a wall to his left
            # there is a collision and the function returns true
            elif(self.move_direction_x == -1):
                if(self.location[0] > wall.x):
                    if(self.location[0] <= wall.x + (wall.width + 10) and
                       self.location[0] >= wall.x - (wall.width / 2 + 10)):
                        if(wall.y <= self.location[1] <= wall.y + wall.height):
                            return True;


    def player_obstacle_collision_y(self):
        # So the player cant move beyond the edge of the screen
        if(self.move_direction_y == -1):
            if(self.location[1] <= 10):
                return True;
        elif(self.move_direction_y == 1):
            if(self.location[1] >= self.screen_size[1] - 30):
                return True;

        # If the player is moving up and there is a wall above him,
        # there is a collision and the function returns true
        for wall in self.level_wall_list[self.current_room]:
            if(self.move_direction_y == -1):
                if(self.location[1] > wall.y):
                    if(self.location[1] <= wall.y + (wall.height + 10) and
                       self.location[1] >= wall.y - (wall.height / 2 + 10)):
                        if(wall.x - 50 <= self.location[0] <= wall.x + wall.width):
                            return True;

            elif(self.move_direction_y == 1):
                if(self.location[1] < wall.y):
                    if(self.location[1] <= wall.y + (wall.height + 10) and
                       self.location[1] >= wall.y - (wall.height / 2 + 10)):
                        if(wall.x - 50 <= self.location[0] <= wall.x + wall.width):
                            return True;


    def player_entered_doorway(self):
        # Detects if the player is in a doorway, returns the name
        # of the door if so, else it return None
        for doorway in self.level_door_list[self.current_room]:
            if(self.location[1] >= doorway.y - 20 and
               self.location[1] <= doorway.y + 20):
                if(self.location[0] >= doorway.x and
                   self.location[0] <= doorway.x + doorway.width):
                    return doorway;

            elif(self.location[1] >= doorway.y - 70 and
                 self.location[1] <= doorway.y + 20):
                if(self.location[0] >= doorway.x and
                   self.location[0] <= doorway.x + doorway.width):
                    return doorway;

            elif(self.location[0] >= doorway.x - 50 and
                 self.location[0] <= doorway.x + 20):
                if(self.location[1] <= doorway.y + doorway.height and
                   self.location[1] >= doorway.y):
                    return doorway;

        return None;


    def move_controller_x(self, x_direction):
        if(x_direction != 0):
            self.current_x_direction = x_direction;

        self.move_direction_x = x_direction;
        self.player_moving = True;


    def move_controller_y(self, y_direction):
        self.move_direction_y = y_direction;

        self.player_moving = True;


    def player_attack(self):
        # As of now, the player can only shoot one bullet at a time
        # so this checks whether or not a player's bullet is already
        # on the screen
        if(len(self.bullet_list) == 0):
            self.bullet_list.append(
                    Bullet(
                        self.game_display, self.screen_size,
                        self, self.location[0], self.location[1],
                        self.current_x_direction
                    )
            );

            # pew pew
            if(self.get_player_num() == 1):
                sound_controller.play_sfx(2, player_bullet_sfx);
            elif(self.get_player_num() == 2):
                sound_controller.play_sfx(3, player_bullet_sfx);



    def player_take_damage(self, damage):
        #Player takes damage if the recovery time has run out
        if(self.player_damage_cooldown == 0):
            self.player_damage_cooldown = 40;
            self.health += damage;

            if(self.get_player_num() == 1):
                sound_controller.play_sfx(4, player_hit_02_sfx);
            elif(self.get_player_num() == 2):
                sound_controller.play_sfx(5, player_hit_02_sfx);


    def set_player_current_room(self, room):
        self.current_room = room;


    def get_player_num(self):
        return self.player_num;


class Bullet:
    def __init__(self, game_display, screen_size, owner, location_x, location_y, direction):
        self.game_display = game_display;
        self.owner = owner; # Player who shot the bullet
        self.location = [location_x, location_y];
        self.direction = direction;

        self.speed = 15;

        #Inital x-location is changed depending on which way the player is facing,
        #so that it doesn't spawn inside of the player sprite
        if(direction == 1):
            self.location[0] += 45;
        else:
            self.location[0] -= 5;

        self.location[1] += 20;


    def update_bullet(self):
        self.location[0] += self.speed * self.direction;
        self.draw_bullet();


    def draw_bullet(self):
        pygame.draw.rect(self.game_display, (255, 255, 255), [self.location[0], self.location[1], 15, 15]);