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

    def main_loop(self):
        game_running = True;

        while game_running:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    game_running = False;

        self.render_screen();

    def render_screen(self):
        game_display.fill((0, 0, 0));
        pygame.display.update();

        clock.tick(FPS);

    def load_resources(self):
        u = 0;



def main():
    game = Game();
    game.main_loop();

if __name__ == '__main__':
    main();