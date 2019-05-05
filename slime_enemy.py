import pygame;
from spritesheet import Sprite_Sheet;

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

        self.slime_children = [];

        self.cell_index = cell_index;
        self.cell_counter = 0;
        self.enemy_hurt_counter = 0;

        self.enemy_moving = False;
        self.enemy_dying = False;
        self.enemy_dead = False;

        self.enemy_health = health;


    def update_enemy(self):
        if not(self.enemy_dead or self.enemy_dying):
            if not(self.enemy_moving):
                self.enemy_idle_animation();

            self.draw_enemy();
            self.cell_counter += 1;
        else:
            if(self.enemy_dying):
                self.enemy_death_animation();

        if(self.enemy_dead):
            del self;


    def draw_enemy(self):
        if(self.enemy_hurt_counter > 0):
            self.enemy_hit_sheet.draw(self.game_display, self.cell_index, self.location[0], self.location[1], 1);
            self.enemy_hurt_counter -= 1;

            self.location[0] += 15;

            if(self.enemy_hurt_counter == 0):
                if(self.enemy_health % 5 == 0):
                    self.multiply_enemy();
        else:
            self.enemy_sheet.draw(self.game_display, self.cell_index, self.location[0], self.location[1], 1);


    def enemy_idle_animation(self):
        if(self.cell_index < 0 or self.cell_index > 4):
            self.cell_index = 0;
        else:
            if(self.cell_counter % 7 == 0):
                self.cell_index += 1;

        if(self.cell_index > 2):
            self.cell_index = 0;


    def enemy_death_animation(self):
        u = 0;


    def damage_enemy(self, damage):
        if(self.enemy_health > 0):
            self.enemy_health -= 1;
            self.enemy_hurt_counter = 5;

            pygame.mixer.Channel(1).play(enemy_hit_sfx);

            if(self.enemy_health == 0):
                pygame.mixer.Channel(1).play(enemy_death_sfx);
                self.enemy_dying = True;


    def multiply_enemy(self):
        if(self.enemy_health == 10):
            self.size_x = 150;
            self.size_y = 150;

            self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (self.size_x, self.size_y));
            self.enemy_sheet = Sprite_Sheet(self.enemy_sprite, self.col, self.rows);
            self.location[0] -= 20;
            self.location[1] += 20;

            '''
            self.slime_children.append(Slime_Enemy(self.game_display, self.player_one, self.player_two,
                                                   self.location[0] + 60, self.location[1],
                                                   self.enemy_health, self.size_x, self.size_y,
                                                   'resources/art/enemies/blob_01_spritesheet.png',
                                                   'resources/art/enemies/blob_01_hit_spritesheet.png',
                                                   self.col, self.rows, self.cell_index - 1));
            '''

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

            '''
            self.slime_children.append(Slime_Enemy(self.game_display, self.player_one, self.player_two,
                                                   self.location[0] + 40, self.location[1], self.enemy_health,
                                                   self.size_x, self.size_y,
                                                   'resources/art/enemies/blob_01_spritesheet.png',
                                                   'resources/art/enemies/blob_01_hit_spritesheet.png',
                                                   self.col, self.rows, self.cell_index - 1));
            '''

            self.enemy_list.append(Slime_Enemy(self.game_display, self.player_one, self.player_two, self.enemy_list,
                                                   self.location[0] + 60, self.location[1], self.enemy_health,
                                                   self.size_x, self.size_y,
                                                   'resources/art/enemies/blob_01_spritesheet.png',
                                                   'resources/art/enemies/blob_01_hit_spritesheet.png',
                                                   self.col, self.rows, self.cell_index - 1));

        self.enemy_hit_sprite = pygame.transform.scale(self.enemy_hit_sprite, (self.size_x, self.size_y));
        self.enemy_hit_sheet = Sprite_Sheet(self.enemy_hit_sprite, self.col, self.rows);

        pygame.mixer.Channel(1).play(enemy_multiply_sfx);