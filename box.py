import pygame 

class Box:
  def __init__(self, X_location, Y_location, game_display):
    self.X_location = X_location
    self.Y_location = Y_location
    self.game_display = game_display
    self.size = 50
    self.speed = 10
    self.isMoving = False
    self.direction = 'Right'
    pygame.draw.rect(self.game_display, (255,0,0), [0,0,self.size,self.size])
  
  def move(self, playerLocation):
    if (playerLocation[0] + 60 > self.X_location and playerLocation[0] +60 < self.X_location +50 and
    ((playerLocation[1] + 25 > self.Y_location) and (playerLocation[1] + 25 < self.Y_location + 50) or 
    (playerLocation[1]  <  self.Y_location + 50) and (playerLocation[1] > self.Y_location))):
      print('a')
      self.isMoving = True
      self.direction == 'Right'

  def update(self): 
    pygame.draw.rect(self.game_display, (255, 0, 0), [self.X_location, self.Y_location, 50, 50]);
    if(self.isMoving):
      if(self.direction == 'Right'):
        self.X_location += self.speed