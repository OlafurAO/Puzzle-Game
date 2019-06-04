from player import Player;
from box import Box;
from slime_enemy import Slime_Enemy;
from map import *;
import pygame;
import os;

pygame.init();

#X_size = 1400
X_size = 960;
Y_size = 720;

screen_size = (X_size, Y_size);
game_display = pygame.display.set_mode(screen_size);
clock = pygame.time.Clock();

FPS = 50;


class Game:
    def __init__(self):
        self.level_number = 0;
        self.current_room_number = 0;

        self.joystick_list = self.setup_joysticks();
        self.level_one = None;
        self.camera = None;

        self.player_one = None;
        self.player_two = None;

        self.level_one_rooms = [];
        self.level_one_doors = [];

        self.load_resources();
        self.load_levels();

        self.player_one = Player(game_display, screen_size,
                                 'resources/art/players/player_1.png',
                                 screen_size[0]/2 + 60, screen_size[1]/2, self.current_room_number, self.level_one_walls, self.level_one_doors);
        self.player_two = Player(game_display, screen_size,
                                 'resources/art/players/player_2.png',
                                 screen_size[0]/2 - 110, screen_size[1]/2, self.current_room_number, self.level_one_walls, self.level_one_doors);

        self.enemy_list = [];
        self.box_list = [];

        self.enemy_list.append(Slime_Enemy(game_display, self.player_one, self.player_two, self.enemy_list,
                               500, 500, 15, 200, 200, 'resources/art/enemies/blob_01_spritesheet.png',
                              'resources/art/enemies/blob_01_hit_spritesheet.png',2, 2, 0));

        self.box = Box(675, 290, game_display, 'resources/art/boxes/box_01.png');


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

                        #Player 1 D-pad controls
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

                        #Player 2 D-pad controls
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

        if(self.player_one.player_switch_rooms or
                self.player_two.player_switch_rooms):
            self.switch_rooms();

        self.camera_list[self.current_room_number].update_map();
        self.player_one.update_player();
        self.player_two.update_player();
        self.box.update();

        for enemy in self.enemy_list:
            enemy.update_enemy();

        pygame.display.update();

        clock.tick(FPS);


    #def loading_screen(self):


    def switch_rooms(self):
        self.player_one.player_switch_rooms = False;
        self.player_two.player_switch_rooms = False;

        ###########################################################
        ######TEMPORARY HARD CODED BULLSHIT FIX THIS ABSOLUTE TRASH
        ###########################################################
        self.player_one.location[0] = self.level_one_doors[1][0].x + \
                                      self.level_one_doors[1][0].width / 2 + 30;
        self.player_one.location[1] = self.level_one_doors[1][0].y - 100;

        self.player_two.location[0] = self.level_one_doors[1][0].x + 40;
        self.player_two.location[1] = self.level_one_doors[1][0].y - 100;

        self.current_room_number = 1;
        ###########################################################

        self.player_one.set_player_current_room(self.current_room_number);
        self.player_two.set_player_current_room(self.current_room_number);


    def load_level_one_obstacles(self):
        self.level_one_walls = [[] for i in range(len(self.level_one))];
        self.level_one_doors = [[] for i in range(len(self.level_one))];

        #Loops through the objects in the map and adds them to
        #lists corresponding to their name
        #TODO: add more objects like boxes, coins or stuff like that
        #TODO: also give the doors their own class so it's easier to connect them
        for room in range(len(self.level_one)):
            for tile_object in self.level_one[room].tmxdata.objects:
                if (tile_object.type == 'Wall'):
                    self.level_one_walls[room].append(
                            Obstacle(self, tile_object.name, tile_object.x, tile_object.y,
                                     tile_object.width, tile_object.height));

                if (tile_object.type == 'Doorway'):
                    direction = '';

                    if(tile_object.x > screen_size[0]/2 + 200):
                        direction = 'RIGHT';
                    elif(tile_object.x < screen_size[0]/2 - 200):
                        direction = 'LEFT';
                    else:
                        if(tile_object.y > screen_size[1]/2):
                            direction = 'DOWN';
                        elif(tile_object.y < screen_size[1]/2):
                            direction = 'UP';

                    print(direction);

                    self.level_one_doors[room].append(
                            Doorway(self, tile_object.name, direction, tile_object.x, tile_object.y,
                                     tile_object.width, tile_object.height));


    def load_resources(self):
        #self.setup_joysticks();
        u = 0;


    def load_levels(self):
        self.load_level_one();

    def load_level_one(self):
        self.level_one = []
        self.camera_list = [];

        # Load the files for the rooms in level 1
        for filename in os.listdir('resources/art/levels/rooms/level_01'):
            if ('room' in filename):
                self.level_one.append(Map('resources/art/levels/rooms/level_01/' + str(filename)));

        # Initialize a camera object for each room, makes
        # the level scroll if the room is big enough
        for i in self.level_one:
            self.camera_list.append(Camera(game_display, screen_size,
                                           self.player_one, self.player_two,
                                           i.make_map(), (0, 0)));

        self.load_level_one_obstacles();


    def setup_joysticks(self):
        joystick_list = [];
        for i in range(0, pygame.joystick.get_count()):
            joystick_list.append(pygame.joystick.Joystick(i));

        for i in joystick_list:
            i.init();
            print('Detected gamepad: ' + i.get_name(), i.get_id());
            print('Initializing ' + i.get_name());

        return joystick_list;


def main():
    game = Game();
    game.main_loop();


if __name__ == '__main__':
    main();