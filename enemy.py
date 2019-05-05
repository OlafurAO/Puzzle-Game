import pygame;
from spritesheet import Sprite_Sheet;

class Enemy:
    def __init__(self, game_display, x_location, y_location, enemy_sprite, col, rows):
        self.game_display = game_display;
        self.location = [x_location, y_location];

        enemy_sprite = pygame.image.load(enemy_sprite);
        enemy_sprite = pygame.transform.scale(enemy_sprite, (200, 200));

        self.sheet = Sprite_Sheet(enemy_sprite, col, rows);

        self.cell_index = 0;
        self.cell_counter = 0;

        self.enemy_moving = False;


    def update_enemy(self):
        if not(self.enemy_moving):
            if(self.cell_index < 0 or self.cell_index > 4):
                self.cell_index = 0;
            else:
                if(self.cell_counter % 7 == 0):
                    self.cell_index += 1;

            if(self.cell_index > 2):
                self.cell_index = 0;

        self.draw_enemy();
        self.cell_counter += 1;


    def draw_enemy(self):
        self.sheet.draw(self.game_display, self.cell_index,  self.location[0], self.location[1], 1);

