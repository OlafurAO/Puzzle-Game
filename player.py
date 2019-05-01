import pygame;

class Player:
    def __init__(self, game_display, location_x, location_y):
        self.game_display = game_display;
        self.location = [location_x, location_y];

        self.speed = 10;

        self.player_moving = False;

        self.move_direction_x = 0;
        self.move_direction_y = 0;

    def update_player(self):
        self.draw_player();

        if(self.player_moving):
            self.move_player();


    def draw_player(self):
        pygame.draw.rect(self.game_display, (255, 255, 255), [self.location[0], self.location[1], 50, 50]);

    def move_player(self):
        self.location[0] += self.speed * self.move_direction_x;
        self.location[1] += self.speed * self.move_direction_y;

    def move_controller_x(self, x_direction):
        self.move_direction_x = x_direction;

        self.player_moving = True;

    def move_controller_y(self, y_direction):
        self.move_direction_y = y_direction;

        self.player_moving = True;






