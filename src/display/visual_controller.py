import pygame;
import time;

class Visual_Controller:
    def __init__(self):
            #self.game_display #Later
            self.xp_font = pygame.font.Font('resources/fonts/joystix monospace.ttf', 25);

            # Handles how long an xp animation should play
            self.xp_gained_counter = 0;


    def update_visuals(self):
        if(self.xp_gained_counter > 0):
            self.update_xp();


    def update_xp(self):
        self.draw_xp_gained();
        self.xp_gained_counter -= 1;


    def draw_on_screen(self):
        u = 0;


    def draw_xp_gained(self):
        self.game_display.blit(self.xp_text, [self.xp_location[0] - self.xp_text.get_width() / 2,
                                         self.xp_location[1] - self.xp_text.get_height() / 2]);


    def play_xp_gained(self, game_display, xp, location):
        self.xp_text = self.xp_font.render(str(xp), True, (0, 0, 0))
        self.game_display = game_display;
        self.xp_location = location;
        self.xp_gained_counter = 50;


        self.draw_xp_gained();


    # Overloaded function
    #def display_xp_gained(self, xp, location):
    #    text = font.render('YOU ARE DEAD', True, (255, 0, 0));