import pygame

pygame.mixer.pre_init(44100, 16, 2, 4096);
pygame.init();
pygame.mixer.set_num_channels(10);


box_push_sfx = pygame.mixer.Sound('resources/sfx/box_push_01.wav');
box_stop_sfx = pygame.mixer.Sound('resources/sfx/box_stop_01.wav')


#instance of a box, 
class Box:
  def __init__(self, X_location, Y_location, game_display, box_art):
    #the locantion of the box element 
    self.X_location = X_location
    self.Y_location = Y_location
    self.game_display = game_display
    #speed and size of the box when kicked
    self.size = 50
    self.speed = 10
    #boolian which shows when the box is supposed to be moveing (false if at edge)
    self.isMoving = False
    #when supposed to be moveing, what direction
    self.direction = 'Right'

    self.box_art = pygame.image.load(box_art).convert_alpha()
    self.box_art = pygame.transform.scale(self.box_art, (70, 70));

    #the box itself, should probably be moved to a seprate def 
    pygame.draw.rect(self.game_display, (255,0,0), [0,0,self.size,self.size])
  

  #move the box 
  def move(self, playerLocation):
    #checks if box is on the right 
    if (playerLocation[0] + 60 > self.X_location and playerLocation[0] +60 < self.X_location +50 and
    ((playerLocation[1] + 25 > self.Y_location) and (playerLocation[1] + 25 < self.Y_location + 50) or 
    (playerLocation[1]  <  self.Y_location + 50) and (playerLocation[1] > self.Y_location))):
      print('a')
      self.isMoving = True
      self.direction == 'Right'
    #checks if box is on top of player/ should be moved up 
    elif (playerLocation[1] > self.Y_location and playerLocation[1] < self.Y_location + 60 and 
    ((playerLocation[0] + 25 > self.X_location) and
    (playerLocation[0] - 25 < self.X_location))):
      print('b')
      self.isMoving = True
      self.direction = 'UP'
    #checks if box is on the bottom of the player/ should be modved down 
    elif (playerLocation[1] < self.Y_location and playerLocation[1] > self.Y_location - 60 and 
    ((playerLocation[0] + 25 > self.X_location) and 
    (playerLocation[0] - 25 < self.X_location))):
      print('C')
      self.isMoving = True
      self.direction = 'DOWN'
    #checks if a box should be moved to the left, and if it is on the left 
    elif (playerLocation[1] > self.Y_location and playerLocation[1] < self.Y_location + 60 
    and ((playerLocation[0] + 25 > self.X_location) 
    and (playerLocation[0] - 25 < self.X_location + 50))):
      print('D')
      self.isMoving = True
      self.direction = 'LEFT'

    pygame.mixer.Channel(1).play(box_push_sfx)

#updates the location of the box every second and moves it
  def update(self): 
    if(self.isMoving):
      if(self.direction == 'Right' and self.X_location < 1350):
        self.X_location += self.speed
      elif(self.direction == 'UP' and self.Y_location > 0 ):
        self.Y_location -= self.speed
      elif(self.direction == 'LEFT' and self.X_location > 0):
        self.X_location -= self.speed
      elif(self.direction == 'DOWN' and self.Y_location < 650):
        self.Y_location += self.speed
      else:
        self.isMoving = False;
        pygame.mixer.Channel(1).play(box_stop_sfx);

    pygame.draw.rect(self.game_display, (255, 0, 0), [self.X_location, self.Y_location, 50, 50]);
    self.game_display.blit(self.box_art, (self.X_location - 10, self.Y_location - 10));