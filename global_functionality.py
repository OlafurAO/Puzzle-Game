import pygame


def check_if_hit(oneXY, twoXY, size):
  if (oneXY[0] + 60 > twoXY[0] and oneXY[0] +60 < twoXY[0] +50 and
  ((oneXY[1] + 25 > twoXY[1]) and (oneXY[1] + 25 < twoXY[1] + 50) or 
  (oneXY[1]  <  twoXY[1] + 50) and (oneXY[1] > twoXY[1]))):
    return True