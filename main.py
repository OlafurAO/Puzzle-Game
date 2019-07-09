import pygame;

from src.input.input_controller import Input_Controller;
from src.audio.sound_controller import Sound_Controller;
from src.player.player import Player;
from src.environments.environments import Environments;
from src.objects.box import Box;


################################### Used for audio tests
from src.audio.sound_controller import Sound_Controller;
sound_controller = Sound_Controller();
########################################################


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
                            'resources/art/players/player_1.png', 1,
                            screen_size[0] / 2 + 60, screen_size[1]/2,
                            0, self.environments.get_level_wall_list(),
                            self.environments.get_level_door_list()
        );

        self.player_two = Player(
                            game_display, screen_size,
                            'resources/art/players/player_2.png', 2,
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

                # Gamepad input
                if(self.gamepad_count != 0):
                    self.input_controller.gamepad_input_controller(event, self.player_one, self.player_two);

                # Keyboard input
                self.input_controller.keyboard_and_mouse_input_controller(event, self.player_one, self.player_two);

                if(event.type == pygame.KEYDOWN):
                    ###############################################
                    ####################Audio tests
                    if(event.key == pygame.K_y):
                        sound_controller.play_music(
                            'resources/music/Best VGM 153 - Mega Man 2 - '
                            'Dr. Wily Stage 1  2.mp3'
                        );
                    elif(event.key == pygame.K_u):
                        sound_controller.pause_music();
                    elif(event.key == pygame.K_i):
                        sound_controller.resume_music();
                    elif(event.key == pygame.K_o):
                        sound_controller.stop_music();
                    ##############################################

                ###############################################

            self.render_screen();

        self.input_controller.disable_gamepads();


    def render_screen(self):
        game_display.fill((0, 0, 100));

        self.environments.update_environment();
        self.player_one.update_player();
        self.player_two.update_player();
        #self.box.update();

        #for enemy in self.enemy_list:
         #   enemy.update_enemy();

        pygame.display.update();

        clock.tick(FPS);


    def load_resources(self):
        #self.setup_joysticks();
        u = 0;


    def gamepad_setup(self):
        self.input_controller = Input_Controller();
        self.gamepad_count = self.input_controller.get_gamepad_count();


def main():
    game = Game();
    game.main_loop();


if __name__ == '__main__':
    main();