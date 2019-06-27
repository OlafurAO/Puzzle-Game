import pygame;

from src.gamepad.gamepad_controller import Gamepad_Controller;
from src.player.player import Player;
from src.environments.environments import Environments;
from src.objects.box import Box;


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
        self.gamepad_setup();
        self.load_resources();

        self.player_one = None;
        self.player_two = None;

        self.environments = Environments(game_display, screen_size, self.player_one, self.player_two);
        self.environments.load_levels();

        self.player_one = Player(
                            game_display, screen_size,
                            'resources/art/players/player_1.png',
                            screen_size[0] / 2 + 60, screen_size[1]/2,
                            0, self.environments.get_level_wall_list(),
                            self.environments.get_level_door_list()
        );

        self.player_two = Player(
                            game_display, screen_size,
                            'resources/art/players/player_2.png',
                            screen_size[0] / 2 - 110, screen_size[1]/2,
                            0, self.environments.get_level_wall_list(),
                            self.environments.get_level_door_list()
        );

        self.environments.set_players(self.player_one, self.player_two);
        self.environments.load_enemies();

        self.enemy_list = [];
        self.box_list = [];


        '''
        self.box = Box(675, 290, game_display, 'resources/art/boxes/box_01.png');
        '''


    def main_loop(self):
        game_running = True;

        while game_running:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    game_running = False;

                if(self.gamepad_count != 0):
                    self.gamepad_controller.gamepad_input_controller(event, self.player_one, self.player_two);

                '''
                ###########################################
                #############Gamepad controls
                if(len(self.gamepads) != 0):

                    #Button input
                    if(event.type == pygame.JOYBUTTONDOWN):

                        #Player one gamepad controls
                        if(self.gamepads[event.joy].get_id() == 0):
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
                        elif(self.gamepads[event.joy].get_id() == 1):
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
                        axis = self.gamepads[event.joy].get_axis(event.axis);

                        #Player 1 D-pad controls
                        if(self.gamepads[event.joy].get_id() == 0):
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
                        elif(self.gamepads[event.joy].get_id() == 1):
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
                '''
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

        self.environments.update_environment();
        self.player_one.update_player();
        self.player_two.update_player();
        #self.box.update();

        for enemy in self.enemy_list:
            enemy.update_enemy();

        pygame.display.update();

        clock.tick(FPS);


    def load_resources(self):
        #self.setup_joysticks();
        u = 0;


    def gamepad_setup(self):
        self.gamepad_controller = Gamepad_Controller();
        self.gamepad_count = self.gamepad_controller.get_gamepad_count();



def main():
    game = Game();
    game.main_loop();


if __name__ == '__main__':
    main();