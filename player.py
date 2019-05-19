import pygame;

pygame.mixer.pre_init(44100, 16, 2, 4096);
pygame.init();
pygame.mixer.set_num_channels(10);

player_hit_sfx = pygame.mixer.Sound('resources/sfx/player_hit_01.wav');
player_hit_02_sfx = pygame.mixer.Sound('resources/sfx/player_hit_02.wav');
player_bullet_sfx = pygame.mixer.Sound('resources/sfx/player_bullet_01.wav');

class Player:
    def __init__(self, game_display, screen_size, player_img, location_x, location_y, wall_list):
        self.game_display = game_display;
        self.screen_size = screen_size;
        self.player_sprite_right = pygame.image.load(player_img).convert_alpha();
        self.player_sprite_left = pygame.transform.flip(self.player_sprite_right, True, False).convert_alpha();
        self.level_wall_list = wall_list;

        self.player_sprite_right = pygame.transform.scale(self.player_sprite_right, (70, 70));
        self.player_sprite_left = pygame.transform.scale(self.player_sprite_left, (70, 70));

        self.location = [location_x, location_y];

        self.move_direction_x = 0;
        self.move_direction_y = 0;
        self.current_x_direction = 1;
        self.bullet_list = [];

        self.health = 10;
        self.speed = 10;

        self.player_moving = False;

        self.player_damage_cooldown = 0;


    def update_player(self):
        self.draw_player();

        if(self.player_moving):
            self.move_player();

        if(len(self.bullet_list) != 0):
            for bullet in self.bullet_list:
                if(bullet.location[0] > self.screen_size[0] or bullet.location[0] < 0):
                    del self.bullet_list[self.bullet_list.index(bullet)];
                    break;
                else:
                    bullet.update_bullet();

        if(self.player_damage_cooldown > 0):
            self.player_damage_cooldown -= 1;


    def draw_player(self):
        if(self.player_damage_cooldown > 30):
            pygame.draw.rect(self.game_display, (255, 0, 0), [self.location[0], self.location[1], 50, 50]);
        else:
            if(self.current_x_direction == 1):
                self.game_display.blit(self.player_sprite_right, (self.location[0] - 10, self.location[1] - 10));
            elif(self.current_x_direction == -1):
                self.game_display.blit(self.player_sprite_left, (self.location[0] - 10, self.location[1] - 10));


    def move_player(self):
        if(self.player_damage_cooldown < 30):
            if not(self.player_obstacle_collision_x()):
                self.location[0] += self.speed * self.move_direction_x;

            if not(self.player_obstacle_collision_y()):
                self.location[1] += self.speed * self.move_direction_y;


    def player_obstacle_collision_x(self):
        for wall in self.level_wall_list:
            if(self.move_direction_x == 1):
                if(self.location[0] < wall.x):
                    if(self.location[0] >= wall.x - (wall.width / 2 + 10) and
                       self.location[0] <= wall.x + (wall.width / 2)):
                        if(wall.y <= self.location[1] <= wall.y + wall.height):
                            return True;
            elif(self.move_direction_x == -1):
                if(self.location[0] > wall.x):
                    if(self.location[0] <= wall.x + (wall.width + 10) and
                       self.location[0] >= wall.x - (wall.width / 2 + 10)):
                        if(wall.y <= self.location[1] <= wall.y + wall.height):
                            return True;


    def player_obstacle_collision_y(self):
        return False;



    def move_controller_x(self, x_direction):
        if(x_direction != 0):
            self.current_x_direction = x_direction;

        self.move_direction_x = x_direction;
        self.player_moving = True;


    def move_controller_y(self, y_direction):
        self.move_direction_y = y_direction;

        self.player_moving = True;

    def player_attack(self):
        if(len(self.bullet_list) == 0):
            self.bullet_list.append(Bullet(self.game_display, self.screen_size,
                                           self.location[0], self.location[1],
                                           self.current_x_direction));
            pygame.mixer.Channel(1).play(player_bullet_sfx);


    def take_damage(self, damage):
        if(self.player_damage_cooldown == 0):
            self.player_damage_cooldown = 40;
            self.health += damage;

            #pygame.mixer.Channel(1).play(player_hit_sfx);
            pygame.mixer.Channel(2).play(player_hit_02_sfx);

class Bullet:
    def __init__(self, game_display, screen_size, location_x, location_y, direction):
        self.game_display = game_display;
        self.location = [location_x, location_y];
        self.direction = direction;

        self.speed = 15;

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