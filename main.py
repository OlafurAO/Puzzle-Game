from player import Player;
from box import Box;
from slime_enemy import Slime_Enemy;
from map import *;
import pygame;

pygame.init();

X_size = 1400 
Y_size = 700

screen_size = (X_size, Y_size);
game_display = pygame.display.set_mode(screen_size);
clock = pygame.time.Clock();

FPS = 50;


class Game:
    def __init__(self):
        self.level_number = 1;

        self.joystick_list = None;
        self.level_one = None;
        self.level_one_walls = None;
        self.camera = None;

        self.player_one = None;
        self.player_two = None;

        self.walls = pygame.sprite.Group();
        self.load_level_one_obstacles();

        self.player_one = Player(game_display, screen_size, 'resources/art/players/player_1.png', 100, 200, self.walls);
        self.player_two = Player(game_display, screen_size, 'resources/art/players/player_2.png', 200, 200, self.walls);

        self.box = Box(675, 290, game_display, 'resources/art/boxes/box_01.png');

        self.enemy_list = [];
<<<<<<< HEAD
        self.enemy_list.append(Slime_Enemy(game_display, self.player_one, self.player_two, self.enemy_list,
                                 500, 500, 15, 200, 200, 'resources/art/enemies/blob_01_spritesheet.png',
                                 'resources/art/enemies/blob_01_hit_spritesheet.png',2, 2, 0));

        self.joystick_list = None;
        self.level_one = None;
        self.camera = None;
=======
>>>>>>> 786a16f3217f5bf5bee0d497fa319bc9306a0a55

        self.load_resources();


        # self.enemy_list.append(Slime_Enemy(game_display, self.player_one, self.player_two, self.enemy_list,
        #                        500, 500, 15, 200, 200, 'resources/art/enemies/blob_01_spritesheet.png',
        #                       'resources/art/enemies/blob_01_hit_spritesheet.png',2, 2, 0));


    def main_loop(self):
        game_running = True;

        while game_running:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    game_running = False;

                ###########################################
                #############Gamepad controls
                if(len(self.joystick_list) != 0):

                    #Button input
                    if(event.type == pygame.JOYBUTTONDOWN):
                        #Player one gamepad controls
                        if(self.joystick_list[event.joy].get_id() == 0):
                            if(event.button == 0):
                                self.player_one.player_attack();
                                print('B');
                            elif(event.button == 1):
                                self.box.move(self.player_one.location);
                                print('A');
                            elif(event.button == 9):
                                print('start');
                            elif(event.button == 8):
                                print('select');

                        #Player two gamepad controls
                        elif(self.joystick_list[event.joy].get_id() == 1):
                            if(event.button == 0):
                                self.player_two.player_attack();
                                print('B');
                            elif(event.button == 1):
                                self.box.move(self.player_two.location);
                                print('A');
                            elif(event.button == 9):
                                print('start');
                            elif(event.button == 8):
                                print('select');

                    #D-pad movement
                    if(event.type == pygame.JOYAXISMOTION):
                        axis = self.joystick_list[event.joy].get_axis(event.axis);

                        #Player 1 gamepad controls
                        if(self.joystick_list[event.joy].get_id() == 0):
                            if(event.axis == 1):
                                if(axis == 0.999969482421875):
                                    self.player_one.move_controller_y(1);
                                elif(axis == -1.0):
                                    self.player_one.move_controller_y(-1);
                                else:
                                    self.player_one.move_controller_y(0);
                            else:
                                if(axis == 0.999969482421875):
                                    self.player_one.move_controller_x(1);
                                elif(axis == -1.0):
                                    self.player_one.move_controller_x(-1);
                                else:
                                    self.player_one.move_controller_x(0);

                        #Player 2 gamepad controls
                        elif(self.joystick_list[event.joy].get_id() == 1):
                            if(event.axis == 1):
                                if(axis == 0.999969482421875):
                                    self.player_two.move_controller_y(1);
                                elif(axis == -1.0):
                                    self.player_two.move_controller_y(-1);
                                else:
                                    self.player_two.move_controller_y(0);
                            else:
                                if (axis == 0.999969482421875):
                                    self.player_two.move_controller_x(1);
                                elif (axis == -1.0):
                                    self.player_two.move_controller_x(-1);
                                else:
                                    self.player_two.move_controller_x(0);

                ###########################################
                ##############Keyboard controls
                if(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_w):
                        self.player_one.move_controller_y(-1);
                    elif(event.key == pygame.K_s):
                        self.player_one.move_controller_y(1);
                    if(event.key == pygame.K_d):
                        self.player_one.move_controller_x(1);
                    elif(event.key == pygame.K_a):
                        self.player_one.move_controller_x(-1);
                    if(event.key == pygame.K_p):
                        self.box.move(self.player_one.location)

                    if(event.key == pygame.K_UP):
                        self.player_two.move_controller_y(-1);
                    elif(event.key == pygame.K_DOWN):
                        self.player_two.move_controller_y(1);
                    if(event.key == pygame.K_RIGHT):
                        self.player_two.move_controller_x(1);
                    elif(event.key == pygame.K_LEFT):
                        self.player_two.move_controller_x(-1);

                    if(event.key == pygame.K_k):
                        self.player_one.player_attack();


                elif(event.type == pygame.KEYUP):
                    if(event.key == pygame.K_w):
                        self.player_one.move_controller_y(0);
                    if(event.key == pygame.K_s):
                        self.player_one.move_controller_y(0);
                    if(event.key == pygame.K_d):
                        self.player_one.move_controller_x(0);
                    if(event.key == pygame.K_a):
                        self.player_one.move_controller_x(0);

                    if(event.key == pygame.K_UP):
                        self.player_two.move_controller_y(0);
                    if(event.key == pygame.K_DOWN):
                        self.player_two.move_controller_y(0);
                    if(event.key == pygame.K_RIGHT):
                        self.player_two.move_controller_x(0);
                    if(event.key == pygame.K_LEFT):
                        self.player_two.move_controller_x(0);
                ###############################################

            self.render_screen();


    def render_screen(self):
        game_display.fill((0, 0, 100));

        self.camera.update_map();
        self.player_one.update_player();
        self.player_two.update_player();
        self.box.update();

        for enemy in self.enemy_list:
            enemy.update_enemy();

        pygame.display.update();

        clock.tick(FPS);


    def load_level_one_obstacles(self):
        # self.level_one = Map('resources/art/levels/rooms/level_01/room_01.tmx');
        self.level_one = Map('resources/art/levels/rooms/level_01/room_01_test.tmx');
        self.level_one_img = self.level_one.make_map();
        self.map_rect = self.level_one_img.get_rect();

        self.camera = Camera(game_display, screen_size, self.player_one, self.player_two,
                             self.level_one.make_map(), (0, 0));

        for tile_object in self.level_one.tmxdata.objects:
            if (tile_object.name == 'Wall'):
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height);


    def load_resources(self):
        self.setup_joysticks();

    def setup_joysticks(self):
        joystick_list = [];
        for i in range(0, pygame.joystick.get_count()):
            joystick_list.append(pygame.joystick.Joystick(i));

        for i in joystick_list:
            i.init();
            print('Detected gamepad: ' + i.get_name(), i.get_id());
            print('Initializing ' + i.get_name());

        self.joystick_list = joystick_list;


def main():
    game = Game();
    game.main_loop();


if __name__ == '__main__':
    main();