import pygame;
from spritesheet import Sprite_Sheet;

class Slime_Enemy:
    def __init__(self, game_display, player_one, player_two, x_location, y_location, health, size_x, size_y, enemy_sprite, col, rows, cell_index):
        self.game_display = game_display;
        self.location = [x_location, y_location];
        self.player_one = player_one;
        self.player_two = player_two;

        enemy_sprite = pygame.image.load(enemy_sprite);
        self.enemy_sprite = pygame.transform.scale(enemy_sprite, (size_x, size_y));

        self.sheet = Sprite_Sheet(self.enemy_sprite, col, rows);

        self.size_x = size_x;
        self.size_y = size_y;
        self.col = col;
        self.rows = rows;

        self.slime_children = [];

        self.cell_index = cell_index;
        self.cell_counter = 0;

        self.enemy_moving = False;
        self.enemy_health = health;


    def update_enemy(self):
        if not(self.enemy_moving):
            if(self.cell_index < 0 or self.cell_index > 4):
                self.cell_index = 0;
            else:
                if(self.cell_counter % 7 == 0):
                    self.cell_index += 1;

            if(self.cell_index > 2):
                self.cell_index = 0;

        if(len(self.slime_children) != 0):
            for i in self.slime_children:
                i.update_enemy();

        self.draw_enemy();
        self.cell_counter += 1;


    def draw_enemy(self):
        self.sheet.draw(self.game_display, self.cell_index,  self.location[0], self.location[1], 1);


    def damage_enemy(self, damage):
        if(self.enemy_health > 0):
            self.enemy_health -= 1;

            if(self.enemy_health == 2):
                self.size_x = 150;
                self.size_y = 150;

                self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (self.size_x, self.size_y));
                self.sheet = Sprite_Sheet(self.enemy_sprite, self.col, self.rows);
                self.location[0] -= 20;
                self.location[1] += 20;

                self.slime_children.append(Slime_Enemy(self.game_display, self.player_one, self.player_two,
                                 self.location[0] + 60, self.location[1], self.enemy_health, self.size_x, self.size_y,
                                 'resources/art/enemies/blob_01_spritesheet.png', self.col, self.rows, self.cell_index - 1))







