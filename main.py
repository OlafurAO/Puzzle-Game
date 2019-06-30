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

        self.gamepad_controller.disable_gamepads();


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