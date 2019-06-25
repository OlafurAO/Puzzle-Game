'''
    ////////TILED MAP INFO
        -Tile Width: 48px
        -Tile Height: 48px

        Object names:
            -Walls: "Wall"
            -Doors: "Doorway"
'''

import pygame;
import os;

from map import *;

class Environments:
    def __init__(self, game_display, screen_size, player_one, player_two):
        self.game_display = game_display;
        self.screen_size = screen_size;
        self.player_one = player_one;
        self.player_two = player_two;

        # Stores the layout of the level and how the
        # rooms are connected
        self.level_door_connection = [];

        # Takes care of displaying the map and scrolling the room
        self.camera = None;

        #Keeps track of the
        self.level_one = None;

        self.level_number = 0;
        self.current_room_number = 0;
        self.number_of_rooms = 0;

        self.load_levels();


    def update_environment(self):
        if (self.player_one.player_switch_rooms or \
           self.player_two.player_switch_rooms):
            self.switch_rooms();

        self.draw_environment();


    def draw_environment(self):
        self.camera_list[self.current_room_number].update_map();


    def set_players(self, one, two):
        self.player_one = one;
        self.player_two = two;


    def switch_levels(self):
        u = 0;


    def switch_rooms(self):
        self.player_one.player_switch_rooms = False;
        self.player_two.player_switch_rooms = False;

        doorway = self.player_one.player_entered_door();

        if(doorway == None):
            doorway = self.player_two.player_entered_door();

        for i in self.level_door_connection:
            if(doorway.id in i):
                if(doorway.id == i[0]):
                    for door in range(len(self.level_one_doors)):
                        for k in range(len(self.level_one_doors[door])):
                            if(self.level_one_doors[door][k].id == i[1]):
                                self.current_room_number = door;
                                self.change_room_and_player_position(self.level_one_doors[door][k]);

                                print(doorway.id, self.level_one_doors[door][k].id);
                                return;

                else:
                    for door in range(len(self.level_one_doors)):
                        for k in range(len(self.level_one_doors[door])):
                            if(self.level_one_doors[door][k].id == i[0]):
                                self.current_room_number = door;
                                self.change_room_and_player_position(self.level_one_doors[door][k]);

                                print(doorway.id, self.level_one_doors[door][k].id);
                                return;


    def change_room_and_player_position(self, doorway):
        self.player_one.set_player_current_room(self.current_room_number);
        self.player_two.set_player_current_room(self.current_room_number);

        if(doorway.direction == 'DOWN'):
            self.player_one.location[0] = doorway.x + doorway.width / 2 + 20;
            self.player_one.location[1] = doorway.y - 100;

            self.player_two.location[0] = doorway.x + doorway.width / 2 - 65;
            self.player_two.location[1] = doorway.y - 100;

        elif(doorway.direction == 'UP'):
            self.player_one.location[0] = doorway.x + doorway.width / 2 + 20;
            self.player_one.location[1] = doorway.y + 65;

            self.player_two.location[0] = doorway.x + doorway.width / 2 - 65;
            self.player_two.location[1] = doorway.y + 65;

        elif(doorway.direction == 'LEFT'):
            self.player_one.location[0] = doorway.x + 60;
            self.player_one.location[1] = doorway.y + doorway.height / 2 + 20;

            self.player_two.location[0] = doorway.x + 60;
            self.player_two.location[1] = doorway.y + doorway.height / 2 - 65;

            self.player_one.current_x_direction = 1;
            self.player_two.current_x_direction = 1;

        elif(doorway.direction == 'RIGHT'):
            self.player_one.location[0] = doorway.x - 95;
            self.player_one.location[1] = doorway.y + doorway.height / 2 + 20;

            self.player_two.location[0] = doorway.x - 95;
            self.player_two.location[1] = doorway.y + doorway.height / 2 - 65;

            self.player_one.current_x_direction = -1;
            self.player_two.current_x_direction = -1;

        #TODO: left and right


    # This function decides the layout of the rooms
    # and will most likely be in its own class later
    # when the generation becomes more complex
    def generate_level(self):
        current_room_number = 0;
        room_counter = 0;

        while(room_counter < 4):
            for current_door in self.level_one_doors[current_room_number]:
                for next_room in range(current_room_number + 1, self.number_of_rooms):
                    for next_door in self.level_one_doors[next_room]:
                        if(current_door.direction == 'UP'):
                            if(next_door.direction == 'DOWN'):
                                if not(self.door_already_linked(current_door, next_door)):
                                    self.link_doors(current_door, next_door);
                                    room_counter += 1;

                        elif(current_door.direction == 'DOWN'):
                            if(next_door.direction == 'UP'):
                                if not(self.door_already_linked(current_door, next_door)):
                                    self.link_doors(current_door, next_door);
                                    room_counter += 1;

                        elif(current_door.direction == 'LEFT'):
                            if(next_door.direction == 'RIGHT'):
                                if not(self.door_already_linked(current_door, next_door)):
                                    self.link_doors(current_door, next_door);
                                    room_counter += 1;

                        elif(current_door.direction == 'RIGHT'):
                            if(next_door.direction == 'LEFT'):
                                if not(self.door_already_linked(current_door, next_door)):
                                    self.link_doors(current_door, next_door);
                                    room_counter += 1;

            current_room_number += 1;

            if(current_room_number >= self.number_of_rooms):
                break;

        #print(self.level_door_connection);


    #Helper function for the generate_level function
    def link_doors(self, current_door, next_door):
        if((current_door.id, next_door.id) not in self.level_door_connection and
           (next_door.id, current_door.id) not in self.level_door_connection):
            self.level_door_connection.append((current_door.id, next_door.id));
            current_door.linked = True;
            next_door.linked = True;


    def door_already_linked(self, current_door, next_door):
        return current_door.linked or next_door.linked;


    def load_level_one_obstacles(self):
        self.level_one_walls = [[] for i in range(len(self.level_one))];
        self.level_one_doors = [[] for i in range(len(self.level_one))];

        door_id = 0;

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
                    direction = self.get_door_direction(tile_object);
                    #print(direction)

                    self.level_one_doors[room].append(
                            Doorway(self, door_id, tile_object.name, direction,
                                    False, tile_object.x, tile_object.y,
                                    tile_object.width, tile_object.height));

                    door_id += 1;


    def load_levels(self):
        self.load_level_one();
        self.generate_level();


    def load_level_one(self):
        self.level_one = []
        self.camera_list = [];

        # Load the files for the rooms in level 1
        for filename in os.listdir('resources/art/levels/rooms/level_01'):
            if('room' in filename):
                self.level_one.append(Map('resources/art/levels/rooms/level_01/' + str(filename)));
                self.number_of_rooms += 1;
                #print(filename);

        # Initialize a camera object for each room, makes
        # the level scroll if the room is big enough
        for i in self.level_one:
            self.camera_list.append(Camera(self.game_display, self.screen_size,
                                           self.player_one, self.player_two,
                                           i.make_map(), (0, 0)));

        self.load_level_one_obstacles();


    def get_door_direction(self, tile_object):
        if (tile_object.x > self.screen_size[0] / 2 + 200):
            return 'RIGHT';
        elif (tile_object.x < self.screen_size[0] / 2 - 200):
            return 'LEFT';
        else:
            if (tile_object.y > self.screen_size[1] / 2):
                return 'DOWN';
            elif (tile_object.y < self.screen_size[1] / 2):
                return 'UP';


    def get_level_wall_list(self):
        return self.level_one_walls;


    def get_level_door_list(self):
        return self.level_one_doors;
