import pygame
import os #libreria que te ayuda con el sistema operativo
import sys
import random
import math
import time

pygame.init()

# Pantalla
WIDTH, HEIGHT  = 1600, 1000
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Danger Zone!')

# FPS
FPS = 30

#Colores
WHITE, BLACK = (255,255,255), (0,0,0)
RED_WINE, RED = (139, 5, 5), (234, 48, 48)
YELLOW = (226, 243, 55)
GREEN_LIFE, GREEN_DARK = (61, 216, 94), (39, 169, 66)

class Bullet(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:/Users/Tom/Data/Art/bullet.png")
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += 10

class Player(pygame.sprite.Sprite):

    walking_frames_l = []
    walking_frames_r = []

    jumping_r = []
    jumping_l = []

    run_frames_r = []
    run_frames_l = []

    def __init__(self, x, y):
            image = pygame.image.load("C:\Users\Tom\Data\Art\Player1.png")
            self.walking_frames_r.append(image)
            

            image = pygame.image.load("C:\Users\Tom\Data\Art\Player1.png")
            image = pygame.transform.flip(image,True,False)
            self.walking_frames_l.append(image)
            

            self.frame_r = 0
            self.frame_l = 0

            self.last_key_pressed = None

            Player.__init__(self)
            self.xvel = 0
            self.yvel = 0
            self.onGround = False
            self.image = self.walking_frames_r[self.frame_r]
            self.rect = pygame.Rect(x,y,23,31)



    def update(self,shoot,up, down, left, right,select, pickups, platforms, inventory, player,bullets):

            if shoot:
                    bullet = Bullet()
                    bullet.rect.x = player.rect.x
                    bullet.rect.y = player.rect.y
                    bullets.add(bullet)
            if right:
                    print ("right")
            if left:
                    print("left")

            if up:
                    # only jump if on the ground
                    if self.onGround: self.yvel -= 7
            if down:
                    pass
            if left:

                    self.last_key_pressed = "LEFT"
                    self.xvel = -4
                    self.frame_l += 1
                    self.image = self.walking_frames_l[self.frame_l]
                    if self.frame_l == 8: self.frame_l = 0
            if right:

                    self.last_key_pressed = "RIGHT"
                    self.xvel = 4
                    self.frame_r += 1
                    self.image = self.walking_frames_r[self.frame_r]
                    if self.frame_r == 8: self.frame_r = 0

            if not (left or right):
                    if self.last_key_pressed == "LEFT":
                            self.image = self.walking_frames_l[1]

                    if self.last_key_pressed == "RIGHT":
                            self.image = self.walking_frames_r[1]


            if not self.onGround:
                    # only accelerate with gravity if in the air
                    self.yvel += 0.3
                    # max falling speed
                    if self.yvel > 30: self.yvel = 30
            if not(left or right):
                    self.xvel = 0
            # increment in x direction
            self.rect.left += self.xvel
            # do x-axis collisions
            self.collide(self.xvel, 0,pickups, platforms,select,inventory)
            # increment in y direction
            self.rect.top += self.yvel
            # assuming we're in the air
            self.onGround = False
            # do y-axis collisions
            self.collide(0, self.yvel, pickups, platforms,select,inventory)