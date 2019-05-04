from player import Player;
from box import Box
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

        self.player_one = Player(game_display, 'resources/art/players/player_1.png', 100, 200);
        self.player_two = Player(game_display, 'resources/art/players/player_2.png',  200, 200);
        self.box = Box(700, 350, game_display, 'resources/art/boxes/box_01.png');

        self.joystick_list = None;
        self.load_resources();


    def main_loop(self):
        game_running = True;

        while game_running:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    game_running = False;

                ################################################################################################
                #############Gamepad controls
                if(len(self.joystick_list) != 0):

                    #Button input
                    if(event.type == pygame.JOYBUTTONDOWN):
                        if(self.joystick_list[event.joy].get_id() == 0):
                            print('Player one pressed ' + str(event.button));
                        elif(self.joystick_list[event.joy].get_id() == 1):
                            print('Player two pressed ' + str(event.button));

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

                        #player_list[joystick_list[event.joy].get_id()].controller_movement(axis, event.axis, True);
                ##################################################################################################
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
                #############################################################################

            self.render_screen();


    def render_screen(self):
        game_display.fill((0, 0, 0));

        self.player_one.update_player();
        self.player_two.update_player();
        self.box.update();

        pygame.display.update();

        clock.tick(FPS);


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