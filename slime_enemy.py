from spritesheet import Sprite_Sheet;
from math import sqrt;
import pygame;

pygame.mixer.pre_init(44100, 16, 2, 4096);
pygame.init();
pygame.mixer.set_num_channels(10);

enemy_hit_sfx = pygame.mixer.Sound('resources/sfx/enemy_hit_01.wav');
enemy_multiply_sfx = pygame.mixer.Sound('resources/sfx/enemy_multiply_01.wav');
enemy_death_sfx = pygame.mixer.Sound('resources/sfx/enemy_death_01.wav');

class Slime_Enemy:
    def __init__(self, game_display, player_one, player_two, enemy_list, x_location, y_location,
                 health, size_x, size_y, enemy_sprite, enemy_hit_sprite, col, rows, cell_index):
        self.game_display = game_display;
        self.location = [x_location, y_location];
        self.player_one = player_one;
        self.player_two = player_two;
        self.enemy_list = enemy_list;

        enemy_sprite = pygame.image.load(enemy_sprite);
        self.enemy_sprite = pygame.transform.scale(enemy_sprite, (size_x, size_y));

        enemy_hit_sprite = pygame.image.load(enemy_hit_sprite);
        self.enemy_hit_sprite = pygame.transform.scale(enemy_hit_sprite, (size_x, size_y));

        self.enemy_sheet = Sprite_Sheet(self.enemy_sprite, col, rows);
        self.enemy_hit_sheet = Sprite_Sheet(self.enemy_hit_sprite, col, rows);

        self.size_x = size_x;
        self.size_y = size_y;
        self.col = col;
        self.rows = rows;

        self.cell_index = cell_index;
        self.cell_counter = 0;
        self.enemy_hurt_counter = 0;
        self.target_player_counter = 50;
        self.target_player_cooldown = 0;
        self.enemy_death_counter = 0;

        self.enemy_moving = False;
        self.enemy_dying = False;
        self.enemy_dead = False;

        self.enemy_health = health;
        self.enemy_speed = 5;
        self.hit_direction = 0;


    def update_enemy(self):
        if not(self.enemy_dead or self.enemy_dying):
            self.check_for_player_bullets();
            self.enemy_controller();

            if not(self.enemy_moving):
                self.enemy_idle_animation();

            self.draw_enemy();
            self.cell_counter += 1;
        else:
            if(self.enemy_dying):
                self.enemy_death_animation();
                self.enemy_death_counter -= 1;

                if(self.enemy_death_counter == 0):
                    self.enemy_dying = False;
                    self.enemy_dead = True;

        if(self.enemy_dead):
            del self;


    def draw_enemy(self):
        if(self.enemy_hurt_counter > 0):
            self.enemy_hit_sheet.draw(self.game_display, self.cell_index - 1, self.location[0], self.location[1], 1);
            self.enemy_hurt_counter -= 1;

            self.location[0] += 15 * self.hit_direction;

            if(self.enemy_hurt_counter == 0):
                if(self.enemy_health % 5 == 0):
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
                if(target_player.location[0] + 35 < self.location[0]):
                    self.location[0] -= self.enemy_speed;
                elif(target_player.location[0] - 80 > self.location[0]):
                    self.location[0] += self.enemy_speed;
                else:
                    ####################NEED TO FIX
                    target_player.take_damage(1);

                if(target_player.location[1] < self.location[1]):
                    self.location[1] -= self.enemy_speed;
                elif(target_player.location[1] > self.location[1]):
                    self.location[1] += self.enemy_speed;

                    ################ADD DAMAGE


    def find_player_distance(self):
        player_one_distance_x = (self.player_one.location[0] - self.location[0])**2;
        player_one_distance_y = (self.player_one.location[1] - self.location[1])**2;
        player_one_distance = sqrt((player_one_distance_x + player_one_distance_y));

        player_two_distance_x = (self.player_two.location[0] - self.location[0]) ** 2;
        player_two_distance_y = (self.player_two.location[1] - self.location[1]) ** 2;
        player_two_distance = sqrt((player_two_distance_x + player_two_distance_y));

        if(player_one_distance > 400 and player_two_distance > 400):
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
                                self.damage_enemy(1, 1);
                        else:
                            if(bullet_list_one[i].location[1] >= self.location[1] and
                               bullet_list_one[i].location[1] <= self.location[1] + 50):
                                del bullet_list_one[i];
                                self.damage_enemy(1, 1);
                else:
                    if(bullet_list_one[i].location[0] <= self.location[0] + 120 and
                       bullet_list_one[i].location[0] >= self.location[0]):
                        if(self.enemy_health > 5):

                            if(bullet_list_one[i].location[1] >= self.location[1] and
                               bullet_list_one[i].location[1] <= self.location[1] + self.size_y - 110):
                                del bullet_list_one[i];
                                self.damage_enemy(1, -1);
                        else:
                            if(bullet_list_one[i].location[1] >= self.location[1] and
                               bullet_list_one[i].location[1] <= self.location[1] + 40):
                                del bullet_list_one[i];
                                self.damage_enemy(1, -1);

        bullet_list_two = self.player_two.bullet_list;

        if (len(bullet_list_two) > 0):
            for i in range(0, len(bullet_list_two)):
                if (bullet_list_two[i].direction == 1):
                    if (bullet_list_two[i].location[0] > self.location[0] and
                        bullet_list_two[i].location[0] < self.location[0] + self.size_x):
                        if (self.enemy_health > 5):
                            if (bullet_list_two[i].location[1] >= self.location[1] and
                                bullet_list_two[i].location[1] <= self.location[1] + self.size_y - 110):
                                del bullet_list_two[i];
                                self.damage_enemy(1, 1);
                        else:
                            if (bullet_list_two[i].location[1] >= self.location[1] and
                                bullet_list_two[i].location[1] <= self.location[1] + 50):
                                del bullet_list_two[i];
                                self.damage_enemy(1, 1);
                else:
                    if (bullet_list_two[i].location[0] <= self.location[0] + 120 and
                        bullet_list_two[i].location[0] >= self.location[0]):
                        if (self.enemy_health > 5):

                            if (bullet_list_two[i].location[1] >= self.location[1] and
                                bullet_list_two[i].location[1] <= self.location[1] + self.size_y - 110):
                                del bullet_list_two[i];
                                self.damage_enemy(1, -1);
                        else:
                            if (bullet_list_two[i].location[1] >= self.location[1] and
                                bullet_list_two[i].location[1] <= self.location[1] + 40):
                                del bullet_list_two[i];
                                self.damage_enemy(1, -1);


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


    def damage_enemy(self, damage, direction):
        if(self.enemy_health > 0):
            self.enemy_health -= 1;
            self.enemy_hurt_counter = 5;

            self.hit_direction = direction;

            pygame.mixer.Channel(8).play(enemy_hit_sfx);

            if(self.enemy_health == 0):
                pygame.mixer.Channel(9).play(enemy_death_sfx);
                self.enemy_dying = True;
                self.enemy_death_counter = 5;


    def multiply_enemy(self):
        if(self.enemy_health == 10):
            self.size_x = 150;
            self.size_y = 150;

            self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (self.size_x, self.size_y));
            self.enemy_sheet = Sprite_Sheet(self.enemy_sprite, self.col, self.rows);
            self.location[0] -= 20;
            self.location[1] += 20;

            self.enemy_list.append(Slime_Enemy(self.game_display, self.player_one, self.player_two, self.enemy_list,
                                                   self.location[0] + 60, self.location[1], self.enemy_health,
                                                   self.size_x, self.size_y,
                                                   'resources/art/enemies/blob_01_spritesheet.png',
                                                   'resources/art/enemies/blob_01_hit_spritesheet.png',
                                                   self.col, self.rows, self.cell_index - 1));

        elif (self.enemy_health == 5):
            self.size_x = 100;
            self.size_y = 100;

            self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (self.size_x, self.size_y));
            self.enemy_sheet = Sprite_Sheet(self.enemy_sprite, self.col, self.rows);

            self.location[0] -= 20;
            self.location[1] += 20;

            self.enemy_list.append(Slime_Enemy(self.game_display, self.player_one, self.player_two, self.enemy_list,
                                                   self.location[0] + 60, self.location[1], self.enemy_health,
                                                   self.size_x, self.size_y,
                                                   'resources/art/enemies/blob_01_spritesheet.png',
                                                   'resources/art/enemies/blob_01_hit_spritesheet.png',
                                                   self.col, self.rows, self.cell_index - 1));

        self.enemy_hit_sprite = pygame.transform.scale(self.enemy_hit_sprite, (self.size_x, self.size_y));
        self.enemy_hit_sheet = Sprite_Sheet(self.enemy_hit_sprite, self.col, self.rows);

        pygame.mixer.Channel(7).play(enemy_multiply_sfx);