import pygame;
import threading;
from math import sqrt;


from src.display.visual_controller import Visual_Controller;
from src.display.spritesheet import Sprite_Sheet;
from src.audio.sound_controller import Sound_Controller;

sound_controller = Sound_Controller();
visual_controller = Visual_Controller();

# SFX files
enemy_hit_sfx = pygame.mixer.Sound('resources/sfx/enemy_hit_01.wav');
enemy_multiply_sfx = pygame.mixer.Sound('resources/sfx/enemy_multiply_01.wav');
enemy_death_sfx = pygame.mixer.Sound('resources/sfx/enemy_death_01.wav');

# TODO: Add obstacle collision
# TODO: Polish AI
# TODO: Fix multiplication function

class Slime_Enemy:
    def __init__(self, game_display, player_one, player_two, enemy_list, x_location, y_location,
                 health, size_x, size_y, level_wall_list, enemy_sprite, enemy_hit_sprite, col, rows, cell_index, room_number):
        self.game_display = game_display;
        self.location = [x_location, y_location];
        self.player_one = player_one;
        self.player_two = player_two;

        # When the slime multiplies he can add another slime to this list
        self.enemy_list = enemy_list;

        # The enemy has a normal spritesheet and one for when he gets hit
        enemy_sprite = pygame.image.load(enemy_sprite);
        self.enemy_sprite = pygame.transform.scale(enemy_sprite, (size_x, size_y));
        enemy_hit_sprite = pygame.image.load(enemy_hit_sprite);
        self.enemy_hit_sprite = pygame.transform.scale(enemy_hit_sprite, (size_x, size_y));

        self.enemy_sheet = Sprite_Sheet(self.enemy_sprite, col, rows);
        self.enemy_hit_sheet = Sprite_Sheet(self.enemy_hit_sprite, col, rows);

        # Determines the size of the slime. When he multiplies he creates a new slime and
        # Can directly initialize the new slime to his size
        self.size_x = size_x;
        self.size_y = size_y;
        self.enemy_width = 50;
        self.enemy_height = 50;


        self.level_wall_list = level_wall_list;

        # Used to detect collision
        self.rect = pygame.Rect(self.location[0], self.location[1], self.enemy_width, self.enemy_width);
        pygame.sprite.Group.add(self);

        # The number of columns and rows in the spritesheets
        self.col = col;
        self.rows = rows;

        # The current index of the spritesheet frame the slime
        # is supposed to display
        self.cell_index = cell_index;
        # Used for calculating the rate of which the slime should switch frames
        self.cell_counter = 0;

        # Used so the enemy as a bit of recovery time
        self.enemy_hurt_counter = 0;
        # Determines for how long the enemy should chase the player
        self.target_player_counter = 50;
        # Determines for how long the enemy should rest
        self.target_player_cooldown = 0;
        # Used so the enemy can have a little animation before he dies
        self.enemy_death_counter = 0;

        self.enemy_moving = False;
        self.enemy_dying = False;
        self.enemy_dead = False;
        self.enemy_aggroed = False;

        #self.enemy_health = 1;
        self.enemy_health = 9;
        self.enemy_speed = 5;
        self.enemy_damage = 1;
        self.enemy_xp = 5;

        # The room this slime is in
        self.current_room = room_number;

        # The direction from which the slime gets hit so he knows
        # which direction to get knocked back
        self.hit_direction = 0;


    def update_enemy(self):
        # Find a better spot for this
        # visual_controller.update_visuals();
        if(self.enemy_dead):
            return;
 
        if not(self.enemy_dying):
            self.check_for_player_bullets();
            self.enemy_controller();

            if not(self.enemy_moving):
                self.enemy_idle_animation();

            self.draw_enemy();
            self.cell_counter += 1;

            self.update_rect();

        else:
            self.enemy_death_animation();
            self.enemy_death_counter -= 1;
            self.kill_enemy();


    def update_rect(self):
        self.rect = pygame.Rect(self.location[0], self.location[1], self.enemy_width, self.enemy_width);


    def draw_enemy(self):
        if(self.enemy_hurt_counter > 0):
            self.enemy_hit_sheet.draw(self.game_display, self.cell_index - 1, self.location[0], self.location[1], 1);
            self.enemy_hurt_counter -= 1;

            if not(self.enemy_obstacle_collision(self.hit_direction, 'X')):
                self.location[0] += 5 * self.hit_direction;

            if(self.enemy_hurt_counter == 0):
                if((self.enemy_health == 6 or self.enemy_health == 3) and self.enemy_health != 0):
                    self.multiply_enemy();
                    self.hit_direction = 0;
        else:
            self.enemy_sheet.draw(self.game_display, self.cell_index, self.location[0], self.location[1], 1);


    def enemy_controller(self):
        if(self.enemy_hurt_counter == 0):
            target_player = self.find_player_distance();

            if(target_player == None):
                return;

            if(self.target_player_counter > 0):
                if not(self.enemy_player_collision(target_player)):
                    if(target_player.location[0] >= self.location[0]):
                        if not(self.enemy_obstacle_collision(1, 'X')):
                            self.location[0] += self.enemy_speed;

                    elif(target_player.location[0] <= self.location[0]):
                        if not(self.enemy_obstacle_collision(-1, 'X')):
                            self.location[0] -= self.enemy_speed;

                    if(target_player.location[1] >= self.location[1]):
                        if not(self.enemy_obstacle_collision(1, 'Y')):
                            self.location[1] += self.enemy_speed;

                    elif(target_player.location[1] <= self.location[1]):
                        if not(self.enemy_obstacle_collision(-1, 'Y')):
                            self.location[1] -= self.enemy_speed;
                else:
                    target_player.player_take_damage(self.enemy_damage);


    def find_player_distance(self):
        player_one_distance_x = (self.player_one.location[0] - self.location[0]) ** 2;
        player_one_distance_y = (self.player_one.location[1] - self.location[1]) ** 2;
        player_one_distance = sqrt((player_one_distance_x + player_one_distance_y));

        player_two_distance_x = (self.player_two.location[0] - self.location[0]) ** 2;
        player_two_distance_y = (self.player_two.location[1] - self.location[1]) ** 2;
        player_two_distance = sqrt((player_two_distance_x + player_two_distance_y));

        if((player_one_distance > 400 and player_two_distance > 400 and
           not self.enemy_aggroed) or self.enemy_hurt_counter > 0):
            return None;

        if(self.target_player_counter > 0):
            self.target_player_counter -= 1;

            if(self.target_player_counter == 0):
                self.target_player_cooldown = 50;

        if(self.target_player_cooldown > 0):
            self.target_player_cooldown -= 1;

            if(self.target_player_cooldown == 0):
                self.target_player_counter = 50;

        if(player_one_distance < player_two_distance):
            return self.player_one;
        else:
            return self.player_two;


    def check_for_player_bullets(self):
        bullet_list_one = self.player_one.bullet_list;

        for bullet in range(len(bullet_list_one)):
            if(pygame.sprite.collide_rect(bullet_list_one[bullet], self)):
                self.damage_enemy(bullet_list_one[bullet].get_damage(),
                                  bullet_list_one[bullet].get_direction(),
                                  bullet_list_one[bullet].get_owner());
                del bullet_list_one[bullet];


    def enemy_obstacle_collision(self, enemy_move_direction, axis):
        for wall in self.level_wall_list[self.current_room]:
            if(axis == 'X'):
                if(enemy_move_direction == 1):
                    if(wall.x > self.location[0] + self.enemy_width):
                        if(pygame.sprite.collide_rect(wall, self)):
                            return True;

                elif(enemy_move_direction == -1):
                    if(wall.x + wall.width < self.location[0]):
                        if(pygame.sprite.collide_rect(wall, self)):
                            return True;

            elif(axis == 'Y'):
                if(enemy_move_direction == 1):
                    if(wall.y > self.location[1] + self.enemy_height):
                        if(pygame.sprite.collide_rect(wall, self)):
                            return True;

                elif(enemy_move_direction == -1):
                    if(wall.y + wall.height < self.location[1]):
                        if(pygame.sprite.collide_rect(wall, self)):
                            return True;


    def enemy_player_collision(self, player):
        return pygame.sprite.collide_rect(player, self);


    def kill_enemy(self):
        if (self.enemy_death_counter == 0):
            self.enemy_dying = False;
            self.enemy_dead = True;

            threading.Thread(
                target=visual_controller.play_xp_gained(
                    self.game_display, self.get_enemy_xp(),
                    self.location
                )
            ).start();


    def enemy_idle_animation(self):
        if(self.enemy_hurt_counter == 0):
            if(self.cell_index < 0 or self.cell_index > 4):
                self.cell_index = 0;
            else:
                if(self.cell_counter % 7 == 0):
                    self.cell_index += 1;

            if(self.cell_index > 2):
                self.cell_index = 0;


    def enemy_death_animation(self):
        self.enemy_hit_sheet.draw(self.game_display, self.cell_index, self.location[0], self.location[1], 1);
        self.location[0] += 15 * self.hit_direction;

        x_location = self.location[0];
        y_location = self.location[1];


    def damage_enemy(self, damage, direction, player):
        if not(self.enemy_aggroed):
            self.enemy_aggroed = True;

        if(self.enemy_health > 0):
            self.enemy_health -= 1;
            self.enemy_hurt_counter = 5;

            self.hit_direction = -direction;

            sound_controller.play_sfx(11, enemy_hit_sfx);

            if(self.enemy_health == 0):
                sound_controller.play_sfx(12, enemy_death_sfx);
                sound_controller.play_sfx(13, enemy_multiply_sfx);

                player.add_to_kill_list(self);
                player.gain_xp(self.get_enemy_xp());

                self.enemy_dying = True;
                self.enemy_death_counter = 5;


    def multiply_enemy(self):
        if(self.enemy_health == 0):
            return;
        else:
            if(self.enemy_health == 6 and self.size_x == 200):
                self.size_x = 150;
                self.size_y = 150;

                self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (self.size_x, self.size_y));
                self.enemy_sheet = Sprite_Sheet(self.enemy_sprite, self.col, self.rows);
                self.location[0] -= 20;
                self.location[1] += 20;

                self.enemy_list[self.current_room].append(
                        Slime_Enemy(
                            self.game_display, self.player_one, self.player_two, self.enemy_list,
                            self.location[0] + 60, self.location[1], self.enemy_health,
                            self.size_x, self.size_y, self.level_wall_list,
                            'resources/art/enemies/blob_01_spritesheet.png',
                            'resources/art/enemies/blob_01_hit_spritesheet.png',
                            self.col, self.rows, self.cell_index - 1, self.current_room
                        )
                );


            elif(self.enemy_health == 3 and self.size_x == 150):
                self.size_x = 100;
                self.size_y = 100;

                self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (self.size_x, self.size_y));
                self.enemy_sheet = Sprite_Sheet(self.enemy_sprite, self.col, self.rows);

                self.location[0] -= 20;
                self.location[1] += 20;

                self.enemy_list[self.current_room].append(
                        Slime_Enemy(
                            self.game_display, self.player_one, self.player_two, self.enemy_list,
                            self.location[0] + 60, self.location[1], self.enemy_health,
                            self.size_x, self.size_y, self.level_wall_list,
                            'resources/art/enemies/blob_01_spritesheet.png',
                            'resources/art/enemies/blob_01_hit_spritesheet.png',
                            self.col, self.rows, self.cell_index - 1, self.current_room
                        )
                );


            self.enemy_hit_sprite = pygame.transform.scale(self.enemy_hit_sprite, (self.size_x, self.size_y));
            self.enemy_hit_sheet = Sprite_Sheet(self.enemy_hit_sprite, self.col, self.rows);

            sound_controller.play_sfx(13, enemy_multiply_sfx);


    def get_enemy_xp(self):
        return self.enemy_xp;