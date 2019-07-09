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

# TODO: Fix hitboxes for bullets (check_for_player_bullets) and add obstacle collision

class Slime_Enemy:
    def __init__(self, game_display, player_one, player_two, enemy_list, x_location, y_location,
                 health, size_x, size_y, enemy_sprite, enemy_hit_sprite, col, rows, cell_index, room_number):
        self.game_display = game_display;
        self.location = [x_location, y_location];
        self.player_one = player_one;
        self.player_two = player_two;

        #When the slime multiplies he can add another slime to this list
        self.enemy_list = enemy_list;

        #The enemy has a normal spritesheet and one for when he gets hit
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

        #The number of columns and rows in the spritesheets
        self.col = col;
        self.rows = rows;

        # The current index of the spritesheet frame the slime
        # is supposed to display
        self.cell_index = cell_index;
        #Used for calculating the rate of which the slime should switch frames
        self.cell_counter = 0;

        #Used so the enemy as a bit of recovery time
        self.enemy_hurt_counter = 0;
        #Determines for how long the enemy should chase the player
        self.target_player_counter = 50;
        #Determines for how long the enemy should rest
        self.target_player_cooldown = 0;
        #Used so the enemy can have a little animation before he dies
        self.enemy_death_counter = 0;

        self.enemy_moving = False;
        self.enemy_dying = False;
        self.enemy_dead = False;
        self.enemy_aggroed = False;

        #self.enemy_health = 1;
        self.enemy_health = 9;
        self.enemy_speed = 5;
        self.enemy_xp = 5;

        # The room this slime is in
        self.room_number = room_number;

        #The direction from which the slime gets hit so he knows
        #which direction to get knocked back
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
        else:
            self.enemy_death_animation();
            self.enemy_death_counter -= 1;

            if(self.enemy_death_counter == 0):
                self.enemy_dying = False;
                self.enemy_dead = True;

                threading.Thread(
                    target=visual_controller.play_xp_gained(
                        self.game_display, self.get_enemy_xp(),
                        self.location
                    )
                ).start();


    def draw_enemy(self):
        if(self.enemy_hurt_counter > 0):
            self.enemy_hit_sheet.draw(self.game_display, self.cell_index - 1, self.location[0], self.location[1], 1);
            self.enemy_hurt_counter -= 1;

            self.location[0] += 15 * self.hit_direction;

            if(self.enemy_hurt_counter == 0):
                if(self.enemy_health % 3 == 0):
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
                if(self.enemy_health > 10):
                    if(target_player.location[0] + 35 < self.location[0]):
                        self.location[0] -= self.enemy_speed;
                    elif(target_player.location[0] - 80 > self.location[0]):
                        self.location[0] += self.enemy_speed;
                    else:
                        if(target_player.location[1] - 50 <= self.location[1] and
                           target_player.location[1] + 20 >= self.location[1]):
                            target_player.player_take_damage(1);

                elif(self.enemy_health > 5):
                    if(target_player.location[0] + 45 < self.location[0]):
                        self.location[0] -= self.enemy_speed;
                    elif(target_player.location[0] - 70 > self.location[0]):
                        self.location[0] += self.enemy_speed;
                    else:
                        if(target_player.location[1] - 50 <= self.location[1] and
                           target_player.location[1] + 20 >= self.location[1]):
                            target_player.player_take_damage(1);
                else:
                    if(target_player.location[0] + 50 < self.location[0]):
                        self.location[0] -= self.enemy_speed;
                    elif(target_player.location[0] - 50 > self.location[0]):
                        self.location[0] += self.enemy_speed;
                    else:
                        if(target_player.location[1] - 50 <= self.location[1] and
                           target_player.location[1] + 20 >= self.location[1]):
                            target_player.player_take_damage(1);

                if(self.enemy_health > 10):
                    if(target_player.location[1] - 25 < self.location[1]):
                        self.location[1] -= self.enemy_speed;
                    elif(target_player.location[1] - 25 > self.location[1]):
                        self.location[1] += self.enemy_speed;
                    else:
                        if(target_player.location[0] + 35 > self.location[0] and
                           target_player.location[0] - 80 < self.location[0]):
                            target_player.player_take_damage(1);
                elif(self.enemy_health > 5):
                    if(target_player.location[1] < self.location[1]):
                        self.location[1] -= self.enemy_speed;
                    elif(target_player.location[1] > self.location[1]):
                        self.location[1] += self.enemy_speed;
                else:
                    if(target_player.location[1] + 15 < self.location[1]):
                        self.location[1] -= self.enemy_speed;
                    elif(target_player.location[1] + 15 > self.location[1]):
                        self.location[1] += self.enemy_speed;


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

        if(len(bullet_list_one) > 0):
            for i in range(0, len(bullet_list_one)):
                if(bullet_list_one[i].direction == 1):
                    if(bullet_list_one[i].location[0] > self.location[0] and
                       bullet_list_one[i].location[0] < self.location[0] + self.size_x):
                        if(self.enemy_health > 5):
                            if(bullet_list_one[i].location[1] >= self.location[1] and
                               bullet_list_one[i].location[1] <= self.location[1] + self.size_y - 110):
                                del bullet_list_one[i];
                                self.damage_enemy(1, 1, self.player_one);
                        else:
                            if(bullet_list_one[i].location[1] >= self.location[1] and
                               bullet_list_one[i].location[1] <= self.location[1] + 50):
                                del bullet_list_one[i];
                                self.damage_enemy(1, 1, self.player_one);
                else:
                    if(bullet_list_one[i].location[0] <= self.location[0] + 120 and
                       bullet_list_one[i].location[0] >= self.location[0]):
                        if(self.enemy_health > 5):

                            if(bullet_list_one[i].location[1] >= self.location[1] and
                               bullet_list_one[i].location[1] <= self.location[1] + self.size_y - 110):
                                del bullet_list_one[i];
                                self.damage_enemy(1, -1, self.player_one);
                        else:
                            if(bullet_list_one[i].location[1] >= self.location[1] and
                               bullet_list_one[i].location[1] <= self.location[1] + 40):
                                del bullet_list_one[i];
                                self.damage_enemy(1, -1, self.player_one);

        bullet_list_two = self.player_two.bullet_list;

        if(len(bullet_list_two) > 0):
            for i in range(0, len(bullet_list_two)):
                if(bullet_list_two[i].direction == 1):
                    if(bullet_list_two[i].location[0] > self.location[0] and
                       bullet_list_two[i].location[0] < self.location[0] + self.size_x):
                        if(self.enemy_health > 5):
                            if(bullet_list_two[i].location[1] >= self.location[1] and
                               bullet_list_two[i].location[1] <= self.location[1] + self.size_y - 110):
                                del bullet_list_two[i];
                                self.damage_enemy(1, 1, self.player_two);
                        else:
                            if(bullet_list_two[i].location[1] >= self.location[1] and
                               bullet_list_two[i].location[1] <= self.location[1] + 50):
                                del bullet_list_two[i];
                                self.damage_enemy(1, 1, self.player_two);
                else:
                    if(bullet_list_two[i].location[0] <= self.location[0] + 120 and
                       bullet_list_two[i].location[0] >= self.location[0]):
                        if(self.enemy_health > 5):

                            if(bullet_list_two[i].location[1] >= self.location[1] and
                               bullet_list_two[i].location[1] <= self.location[1] + self.size_y - 110):
                                del bullet_list_two[i];
                                self.damage_enemy(1, -1, self.player_two);
                        else:
                            if(bullet_list_two[i].location[1] >= self.location[1] and
                               bullet_list_two[i].location[1] <= self.location[1] + 40):
                                del bullet_list_two[i];
                                self.damage_enemy(1, -1, self.player_two);


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
        if(self.enemy_health == 6):
            self.size_x = 150;
            self.size_y = 150;

            self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (self.size_x, self.size_y));
            self.enemy_sheet = Sprite_Sheet(self.enemy_sprite, self.col, self.rows);
            self.location[0] -= 20;
            self.location[1] += 20;

            self.enemy_list[self.room_number].append(
                    Slime_Enemy(
                        self.game_display, self.player_one, self.player_two, self.enemy_list,
                        self.location[0] + 60, self.location[1], self.enemy_health,
                        self.size_x, self.size_y,
                        'resources/art/enemies/blob_01_spritesheet.png',
                        'resources/art/enemies/blob_01_hit_spritesheet.png',
                        self.col, self.rows, self.cell_index - 1, self.room_number
                    )
            );

        elif (self.enemy_health == 3):
            self.size_x = 100;
            self.size_y = 100;

            self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (self.size_x, self.size_y));
            self.enemy_sheet = Sprite_Sheet(self.enemy_sprite, self.col, self.rows);

            self.location[0] -= 20;
            self.location[1] += 20;

            self.enemy_list[self.room_number].append(
                    Slime_Enemy(
                        self.game_display, self.player_one, self.player_two, self.enemy_list,
                        self.location[0] + 60, self.location[1], self.enemy_health,
                        self.size_x, self.size_y,
                        'resources/art/enemies/blob_01_spritesheet.png',
                        'resources/art/enemies/blob_01_hit_spritesheet.png',
                        self.col, self.rows, self.cell_index - 1, self.room_number
                    )
            );

        self.enemy_hit_sprite = pygame.transform.scale(self.enemy_hit_sprite, (self.size_x, self.size_y));
        self.enemy_hit_sheet = Sprite_Sheet(self.enemy_hit_sprite, self.col, self.rows);

        sound_controller.play_sfx(13, enemy_multiply_sfx);


    def get_enemy_xp(self):
        return self.enemy_xp;