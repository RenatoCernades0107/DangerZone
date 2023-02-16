import pygame
import os #libreria que te ayuda con el sistema operativo
import sys
import random
import math


# FPS
FPS = 30

#Colores
WHITE, BLACK = (255,255,255), (0,0,0)
RED_WINE, RED = (139, 5, 5), (234, 48, 48)
YELLOW = (226, 243, 55)
GREEN_LIFE, GREEN_DARK = (61, 216, 94), (39, 169, 66)

# Clase para los jugadores
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        # Llama al constructor de la clase padre (Sprite)
        pygame.sprite.Sprite.__init__(self) 

        # ancho y alto del personaje
        self.width, self.height = 120, 120

        self.image = pygame.image.load(os.path.join('./assets/player1.gif'))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        self.speed = 20
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH/2, HEIGHT/2
        self.shoot = False
        self.direction = 0

    def update(self, keypressed):
        #Definir movimientos
        self.running_left = False
        self.running_right = False
        self.running_up = False
        self.running_down = False

        if pygame.KEYDOWN:
            if keypressed[pygame.K_a]:
                self.running_left = True
            if keypressed[pygame.K_d]:
                self.running_right = True
            if keypressed[pygame.K_w]:
                self.running_up = True
            if keypressed[pygame.K_s]:
                self.running_down = True
            if keypressed[pygame.K_t]:
                self.shoot = True
        
        if self.running_left:
            self.direction = -1
            self.rect.x -= self.speed
        if self.running_right:
            self.direction = 1
            self.rect.x += self.speed

        # if self.running_up:
        #     self.direction = -1
        #     self.rect.y -= self.speed
        # if self.running_down:
        #     self.direction = 1
        #     self.rect.y += self.speed

image_bullets = pygame.image.load(os.path.join('./assets/bullet.png'))
bullet_width, bullet_height = 100, 100
img_bullets = pygame.transform.scale(image_bullets, (bullet_width, bullet_height))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = img_bullets
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
    
    def update(self):
        self.rect.x += (self.direction * self.speed)





# ------------ Creamos la ventana ------------ #
pygame.init()
#Pantalla
WIDTH, HEIGHT  = 600, 600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Danger Zone!')
# ------------ Lista de sprites ------------ #
# lista_proyectiles = pygame.sprite.Group()
lista_de_todos_los_sprites = pygame.sprite.Group()
player = Player()
lista_de_todos_los_sprites.add(player)

bullet_group = pygame.sprite.Group()



def DangerZone():
    running = True
    clock = pygame.time.Clock()
# ------------ Bucle Principal ------------ #
    
    while running:
        key_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if player.shoot:
                bullet = Bullet(player.rect.x, player.rect.y, player.direction)
                bullet_group.add(bullet)

        bullet_group.update()
        lista_de_todos_los_sprites.update(key_pressed)
        
        WIN.fill(RED_WINE)

        lista_de_todos_los_sprites.draw(WIN)
        bullet_group.draw(WIN)
    
        clock.tick(FPS)
        pygame.display.update()
        
DangerZone()
