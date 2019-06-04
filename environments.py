import pygame;
import os;

from map import *;

class Environments:
    def __init__(self, game_display, screen_size, player_one, player_two):
        self.game_display = game_display;
        self.screen_size = screen_size;
        self.player_one = player_one;
        self.player_two = player_two;

        self.level_one = None;
        self.camera = None;

        self.level_one_rooms = [];
        self.level_one_doors = [];

        self.level_number = 0;
        self.current_room_number = 0;

        self.load_levels();


    def update_environment(self):
        self.draw_environment();


    def draw_environment(self):
        self.camera_list[self.current_room_number].update_map();


    def switch_levels(self):
        u = 0;


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

                    if(tile_object.x > self.screen_size[0]/2 + 200):
                        direction = 'RIGHT';
                    elif(tile_object.x < self.screen_size[0]/2 - 200):
                        direction = 'LEFT';
                    else:
                        if(tile_object.y > self.screen_size[1]/2):
                            direction = 'DOWN';
                        elif(tile_object.y < self.screen_size[1]/2):
                            direction = 'UP';

                    print(direction);

                    self.level_one_doors[room].append(
                            Doorway(self, tile_object.name, direction, tile_object.x, tile_object.y,
                                     tile_object.width, tile_object.height));


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
            self.camera_list.append(Camera(self.game_display, self.screen_size,
                                           self.player_one, self.player_two,
                                           i.make_map(), (0, 0)));

        self.load_level_one_obstacles();


    def get_level_wall_list(self):
        return self.level_one_walls;


    def get_level_door_list(self):
        return self.level_one_doors;
