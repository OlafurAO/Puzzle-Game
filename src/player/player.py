import pygame;
import math;

from src.display.visual_controller import Visual_Controller;
from src.audio.sound_controller import Sound_Controller;


sound_controller = Sound_Controller();

# SFX files
player_hit_sfx = pygame.mixer.Sound('resources/sfx/player_hit_01.wav');
player_hit_02_sfx = pygame.mixer.Sound('resources/sfx/player_hit_02.wav');
player_bullet_sfx = pygame.mixer.Sound('resources/sfx/player_bullet_01.wav');

# TODO: Player wall collision doesn't work very well, probably best to delete it and start over
# TODO: Implement player health
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
        self.current_aim_direction = 1;

        # Keeps track of the player's bullets
        self.bullet_list = [];
        self.kill_list = [];

        self.health = 10;
        self.speed = 10;
        self.xp = 0;

        self.player_moving = False;
        self.player_switch_rooms = False;

        # Used so the player has recovery time when damaged so he
        # doesn't get  annihilated immediately
        self.player_damage_cooldown = 0;

        # Used to see where the player is aiming
        self.reticule = Reticule(game_display, location_x, location_y, self.location);
        self.player_width = 50;
        self.player_height = 50;

        self.rect = pygame.Rect(self.location[0], self.location[1], self.player_width, self.player_height);


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

        self.reticule.update_reticule();
        self.rect = pygame.Rect(self.location[0], self.location[1], self.player_width, self.player_height);


    def update_bullets(self):
        # Takes care of deleting bullet objects when they've gone offscreen
        if (len(self.bullet_list) != 0):
            for bullet in self.bullet_list:
                if (bullet.location[0] > self.screen_size[0] or bullet.location[0] < 0 or
                    bullet.location[1] > self.screen_size[1] or bullet.location[1] < 0):
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
            if(self.current_aim_direction == 1):
                self.game_display.blit(self.player_sprite_right, (self.location[0] - 10, self.location[1] - 10));
            elif(self.current_aim_direction == -1):
                self.game_display.blit(self.player_sprite_left, (self.location[0] - 10, self.location[1] - 10));


    def move_player(self):
        if(self.player_damage_cooldown < 30):
            if(self.move_direction_x != 0):
                move_offset = self.speed * self.move_direction_x;
                self.location[0] += move_offset;

                if(self.player_obstacle_collision(self.move_direction_x, 'X')):
                    self.location[0] -= move_offset;

            if(self.move_direction_y != 0):
                move_offset = self.speed * self.move_direction_y;
                self.location[1] += move_offset;

                if(self.player_obstacle_collision(self.move_direction_y, 'Y')):
                    self.location[1] -= move_offset;


    def player_obstacle_collision(self, player_move_direction, axis):
        for wall in self.level_wall_list[self.current_room]:
            if(axis == 'X'):
                if(player_move_direction == 1):
                    if(wall.x > self.location[0]):
                        if(pygame.sprite.collide_rect(wall, self)):
                            return True;

                elif(player_move_direction == -1):
                    if(wall.x < self.location[0]):
                        if(pygame.sprite.collide_rect(wall, self)):
                            return True;

            elif(axis == 'Y'):
                if(player_move_direction == 1):
                    if(wall.y > self.location[1]):
                        if (pygame.sprite.collide_rect(wall, self)):
                            return True;

                elif(player_move_direction == -1):
                    if(wall.y < self.location[1]):
                        if (pygame.sprite.collide_rect(wall, self)):
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


    def mouse_move_aiming_reticule(self, mouse_position):
        self.reticule.mouse_move_reticule(mouse_position);

        if(mouse_position[0] < self.location[0] + 20):
            self.current_aim_direction = -1;
        elif(mouse_position[0] > self.location[0] + 20):
            self.current_aim_direction = 1;


    def gamepad_move_aiming_reticule_x(self, direction):
        self.reticule.gamepad_move_reticule_x(direction);


    def gamepad_move_aiming_reticule_y(self, direction):
        self.reticule.gamepad_move_reticule_y(direction);


    def player_attack(self):
        # As of now, the player can only shoot one bullet at a time
        # so this checks whether or not a player's bullet is already
        # on the screen
        if(len(self.bullet_list) == 0):
            bullet_angle = self.reticule.get_reticule_angle(self.player_width, self.player_height);

            self.bullet_list.append(
                    Bullet(
                        self.game_display, self.screen_size,
                        self, bullet_angle, self.location[0],
                        self.location[1], -self.current_aim_direction
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


    def add_to_kill_list(self, enemy):
        self.kill_list.append(enemy);


    def gain_xp(self, xp):
        self.xp += xp;
        print(self.xp);


    def set_player_current_room(self, room):
        self.current_room = room;


    def get_player_num(self):
        return self.player_num;


class Bullet:
    def __init__(self, game_display, screen_size, owner, bullet_angle, location_x, location_y, direction):
        self.game_display = game_display;
        self.owner = owner; # Player who shot the bullet, can be used to keep track of kills
        self.bullet_angle = bullet_angle;
        self.location = [location_x, location_y];
        self.direction = direction;

        self.damage = 1;
        self.speed = 30;

        self.bullet_width = 15;
        self.bullet_height = 15;

        #Inital location of the bullet is changed depending on which way the player is facing,
        #so that it doesn't spawn inside of the player sprite
        if(direction == 1):
            self.location[0] += 45;
        else:
            self.location[0] -= 5;

        self.location[1] += 20;

        self.rect = pygame.Rect(self.location[0], self.location[1], self.bullet_width, self.bullet_height);


    def update_bullet(self):
        self.move_bullet();
        self.draw_bullet();
        self.update_rect();


    def update_rect(self):
        self.rect = pygame.Rect(self.location[0], self.location[1], self.bullet_width, self.bullet_height);


    def draw_bullet(self):
        pygame.draw.rect(self.game_display, (255, 255, 255), [self.location[0], self.location[1], self.bullet_width, self.bullet_height]);


    def move_bullet(self):
        self.location[0] += self.speed * math.cos(self.bullet_angle);
        self.location[1] += self.speed * math.sin(self.bullet_angle);


    def get_damage(self):
        return self.damage;


    def get_owner(self):
        return self.owner;


    def get_direction(self):
        return self.direction;


# Keeps track of which direction the player is pointing their weapon
class Reticule:
    def __init__(self, game_display, location_x, location_y, player_location):
        self.game_display = game_display;
        self.location = [location_x + 20, location_y - 50];
        self.player_location = player_location;

        self.sensitivity = 10;

        self.x_direction = 0;
        self.y_direction = 0;


    def update_reticule(self):
        if(self.x_direction != 0):
            self.gamepad_move_reticule_x(self.x_direction);

        if(self.y_direction != 0):
            self.gamepad_move_reticule_y(self.y_direction);

        self.draw_reticule();


    def draw_reticule(self):
        pygame.draw.rect(self.game_display, (255, 0, 0), [self.location[0], self.location[1], 10, 10]);


    def mouse_move_reticule(self, mouse_position):
        self.location = list(mouse_position);


    def gamepad_move_reticule_x(self, direction):
        if(direction == 1):
            if(self.location[0] < self.player_location[0] + 100):
                self.location[0] += self.sensitivity * direction;
        elif(direction == -1):
            if (self.location[0] > self.player_location[0] - 60):
                self.location[0] += self.sensitivity * direction;

        self.x_direction = direction;


    def gamepad_move_reticule_y(self, direction):
        if(direction == 1):
            if(self.location[1] < self.player_location[1] + 100):
                self.location[1] += self.sensitivity * direction;
        elif(direction == -1):
            if(self.location[1] > self.player_location[1] - 60):
                self.location[1] += self.sensitivity * direction;

        self.y_direction = direction;


    def reposition_reticule_x(self, move_offset):
        self.location[0] += move_offset;


    def reposition_reticule_y(self, move_offset):
        self.location[1] += move_offset;


    def get_reticule_position(self):
        return self.location;


    def get_reticule_angle(self, player_width, player_height):
        player_x = self.player_location[0] + player_width / 2;
        player_y = self.player_location[1] + player_height / 2;

        delta_x = self.location[0] - player_x;
        delta_y = self.location[1] - player_y;

        return math.atan2(delta_y, delta_x);