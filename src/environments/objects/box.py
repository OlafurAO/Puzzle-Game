import pygame

pygame.mixer.pre_init(44100, 16, 2, 4096);
pygame.init();
pygame.mixer.set_num_channels(10);


box_push_sfx = pygame.mixer.Sound('resources/sfx/box_push_01.wav');
box_stop_sfx = pygame.mixer.Sound('resources/sfx/box_stop_01.wav')


#instance of a box, 
class Box:
    def __init__(self, game_display, wall_list, X_location, Y_location, box_art):
        self.game_display = game_display
        self.wall_list = wall_list;

        #the locantion of the box element
        self.X_location = X_location
        self.Y_location = Y_location

        #speed and size of the box when kicked
        self.width = 95;
        self.height = 95;

        self.speed = 10

        #boolian which shows when the box is supposed to be moveing (false if at edge)
        self.isMoving = False

        #when supposed to be moveing, what direction
        self.direction = 'Right'

        self.box_art = pygame.image.load(box_art).convert_alpha()
        self.box_art = pygame.transform.scale(self.box_art, (110, 110));

        self.rect = pygame.Rect(X_location, Y_location, self.width, self.width);


    # updates the location of the box every second and moves it
    def update_box(self):
        if(self.isMoving and not self.box_obstacle_collision()):
            if (self.direction == 'RIGHT' and self.X_location < 1350):
                self.X_location += self.speed
            elif (self.direction == 'UP' and self.Y_location > 0):
                self.Y_location -= self.speed
            elif (self.direction == 'LEFT' and self.X_location > 0):
                self.X_location -= self.speed
            elif (self.direction == 'DOWN' and self.Y_location < 650):
                self.Y_location += self.speed;

            self.rect = pygame.Rect(self.X_location, self.Y_location, self.width, self.width);


    def draw_box(self):
        self.game_display.blit(self.box_art, (self.X_location - 10, self.Y_location - 10));


    def box_obstacle_collision(self):
        for wall in self.wall_list:
            if(pygame.sprite.collide_rect(wall, self)):
                pygame.mixer.Channel(1).play(box_stop_sfx);
                self.isMoving = False;
                return True;

    #move the box
    def move(self, playerLocation):
        #checks if box is on the right
        if(playerLocation[0] < self.X_location):
            self.isMoving = True
            self.direction = 'RIGHT'

        #checks if box is on top of player/ should be moved up
        elif(playerLocation[1] < self.Y_location + self.width):
            self.isMoving = True
            self.direction = 'UP'

        #checks if box is on the bottom of the player/ should be modved down
        elif(playerLocation[1] > self.Y_location):
            self.isMoving = True
            self.direction = 'DOWN'

        #checks if a box should be moved to the left, and if it is on the left
        elif (playerLocation[0] < self.X_location):
            self.isMoving = True
            self.direction = 'LEFT'

        if(self.isMoving):
            pygame.mixer.Channel(1).play(box_push_sfx)