import pygame 


#instance of a box, 
class Box:
  def __init__(self, X_location, Y_location, game_display):
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

#updates the location of the box every second and moves it, checks the 'direction' and moves accordingly 
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
    pygame.draw.rect(self.game_display, (255, 0, 0), [self.X_location, self.Y_location, 50, 50]);