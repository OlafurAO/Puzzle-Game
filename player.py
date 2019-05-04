import pygame;

class Player:
    def __init__(self, game_display, player_img, location_x, location_y):
        self.game_display = game_display;
        self.player_sprite_right = pygame.image.load(player_img).convert_alpha();
        self.player_sprite_left = pygame.transform.flip(self.player_sprite_right, True, False).convert_alpha();

        self.player_sprite_right = pygame.transform.scale(self.player_sprite_right, (70, 70));
        self.player_sprite_left = pygame.transform.scale(self.player_sprite_left, (70, 70));

        self.location = [location_x, location_y];

        self.move_direction_x = 0;
        self.move_direction_y = 0;
        self.current_x_direction = 1;

        self.player_moving = False;
        self.speed = 10;


    def update_player(self):
        self.draw_player();

        if(self.player_moving):
            self.move_player();


    def draw_player(self):
        if(self.current_x_direction == 1):
            self.game_display.blit(self.player_sprite_right, (self.location[0] - 10, self.location[1] - 10));
        elif(self.current_x_direction == -1):
            self.game_display.blit(self.player_sprite_left, (self.location[0] - 10, self.location[1] - 10));

        #pygame.draw.rect(self.game_display, (255, 255, 255), [self.location[0], self.location[1], 50, 50]);


    def move_player(self):
        self.location[0] += self.speed * self.move_direction_x;
        self.location[1] += self.speed * self.move_direction_y;


    def move_controller_x(self, x_direction):
        if(x_direction != 0):
            self.current_x_direction = x_direction;

        self.move_direction_x = x_direction;
        self.player_moving = True;


    def move_controller_y(self, y_direction):
        self.move_direction_y = y_direction;

        self.player_moving = True;
