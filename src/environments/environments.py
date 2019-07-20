'''INFO
    ########################################
    ////////TILED MAP INFO
    ########################################
        -Tile Width: 48px
        -Tile Height: 48px

        Object names:
            -Walls: "Wall"
            -Doorways: "Doorway"
            -Doors:
                -Doors opened by defeating enemies: "Door_Enemy"
                -Doors opened by pressing switch: "Door_<switch type>_<switch id>"
            -Switches:
                -Switches that can be pressed by player: "Light_Switch_01"
                -Switched that need to be pressed with boxes: "Heavy_Switch_01"

        Enemy names:
            -Slimes:
                -Green slime: "Green_Slime"
    #######################################
'''

import os;

from src.environments.map import *;
from src.enemies.slime_enemy import Slime_Enemy;
from src.environments.objects.box import Box;


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

        self.level_number = 0;
        self.current_room_number = 0;
        self.number_of_rooms = 0;


    def update_environment(self):
        # Checks if one of the players has entered a doorway
        if(self.player_one.player_switch_rooms or
           self.player_two.player_switch_rooms):
            self.switch_rooms();

        self.update_enemies();
        self.update_doors();
        self.update_boxes();

        self.draw_environment();


    def update_enemies(self):
        # Removes an enemy from the list if he has been killed by a player.
        # This code is an unnecessarily complicated mess because you cant delete
        # list elements in a traditional for loop (for i in enemy_list)
        new_enemy_list = self.enemy_list[self.current_room_number];

        for enemy in range(len(self.enemy_list[self.current_room_number])):
            if (self.enemy_list[self.current_room_number][enemy].enemy_dead):
                del new_enemy_list[enemy];
                break;  # The loop needs to be broken immediately or we get an index error

        self.enemy_list[self.current_room_number] = new_enemy_list;


    def update_doors(self):
        # If all enemies in the room are dead, this code checks if any doors
        # in the room had a "kill enemies" condition and opens it
        if(len(self.enemy_list[self.current_room_number]) == 0):
            for door in self.level_one_doors[self.current_room_number]:
                if(door.get_condition() == 'ENEMY'):
                    door.open_door();


    def update_boxes(self):
        if(self.player_one.is_player_interacting()):
            self.player_one.disable_interaction();
            for box in self.level_one_boxes[self.current_room_number]:
                if(self.interaction_collision(box, self.player_one)):
                    box.move(self.player_one.get_player_location());

        for box in self.level_one_boxes[self.current_room_number]:
            box.update_box();


    def draw_environment(self):
        self.camera_list[self.current_room_number].update_map();

        # Update all the enemies in the current room
        for enemy in self.enemy_list[self.current_room_number]:
            enemy.update_enemy();

        # Draw all the doors in the current room
        for door in self.level_one_doors[self.current_room_number]:
            if not(door.is_door_open()):
                door.draw_door();

        for switch in self.level_one_switches[self.current_room_number]:
            switch.draw_switch();

        for box in self.level_one_boxes[self.current_room_number]:
            box.draw_box();


    def set_players(self, one, two):
        self.player_one = one;
        self.player_two = two;


    def switch_levels(self):
        u = 0;


    def switch_rooms(self):
        self.player_one.player_switch_rooms = False;
        self.player_two.player_switch_rooms = False;

        # Get the doorway that player one has entered (if any)
        doorway = self.player_one.player_entered_doorway();
        # If player one hasn't entered a doorway, check if player two has
        if(doorway == None):
            doorway = self.player_two.player_entered_doorway();

        for i in self.level_door_connection:
            # Check if the current doorway is in the tuple i
            if(doorway.id in i):
                if(doorway.id == i[0]):  # Check if the current doorway is the first element in the tuple
                    # Find the door object that corresponds to the id of
                    # the door which the current door is connected to
                    for door in range(len(self.level_one_doorways)):
                        for k in range(len(self.level_one_doorways[door])):
                            # Check if the id of [door][k] matches the id of the door connected
                            # to the current door. If so, we've found our door object
                            if(self.level_one_doorways[door][k].id == i[1]):
                                self.current_room_number = door;
                                self.change_room_and_player_position(self.level_one_doorways[door][k]);
                                return;

                # Same shit here, only this time the current door is the second element in the tuple
                else:
                    for door in range(len(self.level_one_doorways)):
                        for k in range(len(self.level_one_doorways[door])):
                            if(self.level_one_doorways[door][k].id == i[0]):
                                self.current_room_number = door;
                                self.change_room_and_player_position(self.level_one_doorways[door][k]);
                                return;


    def change_room_and_player_position(self, doorway):
        self.player_one.set_player_current_room(self.current_room_number);
        self.player_two.set_player_current_room(self.current_room_number);

        # This set of if statements repositions the players in the middle
        # of the doorway they came through, according to the doorway's direction.
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


    # This function decides the layout of the rooms
    # and will most likely be in its own class later
    # when the generation becomes more complex
    def generate_level(self):
        current_room_number = 0;
        room_counter = 0;

        # Shut up, it works
        if(self.level_number == 0):
            while(room_counter < 4):
                # Loop through every door in the current room
                for current_door in self.level_one_doorways[current_room_number]:
                    for next_room in range(current_room_number + 1, self.number_of_rooms):
                        # Loop through every door in the next room
                        for next_door in self.level_one_doorways[next_room]:
                            # This set of if statements checks the direction of the current door
                            # and links the next door to it if it fits
                            if(current_door.direction == 'UP'):
                                if(next_door.direction == 'DOWN'):
                                    # Checks if either of the doors have already been linked
                                    # to another door
                                    if not(self.is_door_already_linked(current_door, next_door)):
                                        self.link_doors(current_door, next_door);
                                        room_counter += 1;

                            elif(current_door.direction == 'DOWN'):
                                if(next_door.direction == 'UP'):
                                    if not(self.is_door_already_linked(current_door, next_door)):
                                        self.link_doors(current_door, next_door);
                                        room_counter += 1;

                            elif(current_door.direction == 'LEFT'):
                                if(next_door.direction == 'RIGHT'):
                                    if not(self.is_door_already_linked(current_door, next_door)):
                                        self.link_doors(current_door, next_door);
                                        room_counter += 1;

                            elif(current_door.direction == 'RIGHT'):
                                if(next_door.direction == 'LEFT'):
                                    if not(self.is_door_already_linked(current_door, next_door)):
                                        self.link_doors(current_door, next_door);
                                        room_counter += 1;

                current_room_number += 1;

                if(current_room_number >= self.number_of_rooms):
                    break;


    def link_doors(self, current_door, next_door):
        # Links the two doors together, creating a connection between them
        self.level_door_connection.append((current_door.id, next_door.id));
        current_door.linked = True;
        next_door.linked = True;


    def load_levels(self):
        self.load_level_one();
        self.generate_level();


    def load_level_one(self):
        self.level_one = []
        self.camera_list = [];

        # Load the .tmx files for the rooms in level 1
        for filename in os.listdir('resources/art/levels/rooms/level_01'):
            if('room' in filename):
                self.level_one.append(Map('resources/art/levels/rooms/level_01/' + str(filename)));
                self.number_of_rooms += 1;

        # Initialize a camera object for each room, makes
        # the level scroll if the room is big enough
        for i in self.level_one:
            self.camera_list.append(Camera(self.game_display, self.screen_size,
                                           self.player_one, self.player_two,
                                           i.make_map(), (0, 0)));

        self.load_level_one_obstacles();


    def load_level_one_obstacles(self):
        # These lists of lists keep track of the objects for each room.
        self.level_one_walls = [[] for i in range(len(self.level_one))];
        self.level_one_doorways = [[] for i in range(len(self.level_one))];
        self.level_one_doors = [[] for i in range(len(self.level_one))];
        self.level_one_switches = [[] for i in range(len(self.level_one))];
        self.level_one_boxes = [[] for i in range(len(self.level_one))];

        doorway_id = 0;  # Give each doorway a unique id
        door_id = 0;     # Give each door a unique id

        # Loops through the objects in the map and adds them by
        # type corresponding to their names
        #TODO: add more objects like boxes, coins or stuff like that
        for room in range(len(self.level_one)):
            for tile_object in self.level_one[room].tmxdata.objects:
                if(tile_object.type == 'Wall'):
                    self.level_one_walls[room].append(
                            Obstacle(
                                self, tile_object.name, tile_object.x, tile_object.y,
                                tile_object.width, tile_object.height
                            )
                    );

                elif(tile_object.type == 'Doorway'):
                    # Get the direction of the doorway, to make it easier
                    # to link it to other doors
                    direction = self.get_door_direction(tile_object);

                    self.level_one_doorways[room].append(
                            Doorway(
                                self, doorway_id, tile_object.name, direction,
                                False, tile_object.x, tile_object.y,
                                tile_object.width, tile_object.height
                            )
                    );

                    doorway_id += 1;

                elif(tile_object.type == "Door"):
                    self.create_door(tile_object, door_id, room);
                    door_id += 1;

                elif(tile_object.type == 'Switch'):
                    self.create_switch(tile_object, room);

                elif(tile_object.type == 'Box'):
                    self.create_box(tile_object, room);


    def create_door(self, door, door_id, room):
        # Get the direction of the door, to determine how it should
        # be displayed
        direction = self.get_door_direction(door);

        # The condition that has to be met for the door to open
        condition = '';

        if(door.name == 'Door_Enemy'):
            condition = 'ENEMY';

        elif('Door_Heavy' in door.name):
            condition = 'HEAVY_' + door.name[-2:];

        elif('Door Light' in door.name):
            condition = 'LIGHT_' + door.name[-2:];


        self.level_one_doors[room].append(
                Door(
                    self, door_id, direction, condition, door.x,
                    door.y, door.width, door.height
                )
        );


    def create_switch(self, tile_object, room):
        self.level_one_switches[room].append(
            Switch(
                self.game_display, tile_object.type,
                tile_object.x, tile_object.y,
                tile_object.width, tile_object.height
            )
        );


    def create_box(self, tile_object, room):
        self.level_one_boxes[room].append(
            Box(
                self.game_display, self.level_one_walls[room],
                tile_object.x, tile_object.y,
                'resources/art/boxes/box_01.png'
            )
        );


    def load_enemies(self):
        # Keeps track of the enemies of the level and
        # in which rooms they are
        self.enemy_list = [[] for i in range(len(self.level_one))];

        for room in range(len(self.level_one)):
            for tile_object in self.level_one[room].tmxdata.objects:
                if(tile_object.type == 'Enemy'):
                    self.spawn_enemy(tile_object, room);


    def spawn_enemy(self, enemy, room):
        if(enemy.name == 'Green_Slime'):
            self.enemy_list[room].append(
                Slime_Enemy(
                    self.game_display, self.player_one,
                    self.player_two, self.enemy_list,
                    enemy.x, enemy.y, 15, 200, 200, self.get_level_wall_list(),
                    'resources/art/enemies/blob_01_spritesheet.png',
                    'resources/art/enemies/blob_01_hit_spritesheet.png',
                    2, 2, 0, room
                )
            );


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
        return self.level_one_doorways;



    def get_level_obstacle_list(self):
        return self.level_one_boxes;


    def is_door_already_linked(self, current_door, next_door):
        return current_door.linked or next_door.linked;


    # Is the player close enough to an object
    # to be able to interact with it?
    def interaction_collision(self, object, player):
        return pygame.sprite.collide_rect(object, player);