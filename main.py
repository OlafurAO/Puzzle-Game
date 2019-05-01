from player import Player;

import pygame;

pygame.init();

screen_size = (1400, 700);
game_display = pygame.display.set_mode(screen_size);
clock = pygame.time.Clock();

FPS = 50;

class Game:
    def __init__(self):
        self.load_resources();

        self.level_number = 1;

        self.player_one = Player(game_display, 100, 200);
        self.player_two = Player(game_display, 200, 200);


    def main_loop(self):
        game_running = True;

        while game_running:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    game_running = False;

                if(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_w):
                        self.player_one.move_controller_y(-1);
                    if(event.key == pygame.K_s):
                        self.player_one.move_controller_y(1);
                    if(event.key == pygame.K_d):
                        self.player_one.move_controller_x(1);
                    if(event.key == pygame.K_a):
                        self.player_one.move_controller_x(-1);

                    if(event.key == pygame.K_UP):
                        self.player_two.move_controller_y(-1);
                    if(event.key == pygame.K_DOWN):
                        self.player_two.move_controller_y(1);
                    if(event.key == pygame.K_RIGHT):
                        self.player_two.move_controller_x(1);
                    if(event.key == pygame.K_LEFT):
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


            self.render_screen();


    def render_screen(self):
        game_display.fill((0, 0, 0));

        self.player_one.update_player();
        self.player_two.update_player();

        pygame.display.update();

        clock.tick(FPS);


    def load_resources(self):
        u = 0;


def main():
    game = Game();
    game.main_loop();


if __name__ == '__main__':
    main();