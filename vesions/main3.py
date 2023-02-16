
import pygame
import os #libreria que te ayuda con el sistema operativo
import random
import math

#Colores
WHITE, BLACK = (255,255,255), (0,0,0)
RED_WINE, RED = (139, 5, 5), (234, 48, 48)
YELLOW = (226, 243, 55)
GREEN_LIFE, GREEN_DARK = (61, 216, 94), (39, 169, 66)


pygame.init()
#-------------------- Pantalla --------------------------#
WIDTH = 1500 
HEIGHT = int(WIDTH * 0.6)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Fotogramas por segundos
clock = pygame.time.Clock()
FPS = 60


#-------------------- Clase del jugador --------------------------#
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        
        # ------- Caracteristicas del jugador ----------#
        self.speed = speed
        self.flip_x = False
        self.direccion_x = 1
        self.direccion_y = 1
        self.life = 100

        #----- Buscamos la imagen y hacemos un rectangulo para ella ----- #
        self.image = pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/movLeft/0-player1.gif'))
        self.img = pygame.transform.scale(self.image, (int(self.image.get_width() * scale ), int(self.image.get_height() * scale  )) )
        self.rect = self.img.get_rect()
        self.rect.center = (x , y)

    def update(self, moving_left, moving_right, moving_up, moving_down, shotting):
        dx = 0
        dy = 0
        
        #--- Movimientos del jugador ----#
        if moving_left == True:
            dx = -self.speed
            self.flip_x = True
            self.direccion_x = -1
            self.direccion_y = 0

        if moving_right == True:
            dx =  self.speed
            self.flip_x = False
            self.direccion_x = 1
            self.direccion_y = 0

        if moving_up == True:
            dy = -self.speed
            self.direccion_x = 0
            self.direccion_y = -1

        if moving_down == True:
            dy = self.speed
            self.direccion_x = 0
            self.direccion_y = 1

        #--- Dispara el jugador ----#
        if shotting == True:
            bullets = Bullet(self.rect.x, self.rect.y, 10, self.direccion_x, self.direccion_y)
            bullets_group.add(bullets)
        
        #--- actualizamos la posicion del rectangulo ----#
        self.rect.x += dx
        self.rect.y += dy

        # ----- Comprobar que no se salga del mapa ---- #
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT - 5:
            self.rect.bottom = HEIGHT - 5
        
    

    def draw(self):
        WIN.blit(pygame.transform.flip(self.img, self.flip_x, False),self.rect.center)

#-------------------- Clase del Zombie --------------------------#
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        
        # ------- Caracteristicas del zombie ----------#
        self.speed = speed
        self.flip_x = False
        self.life = 50
        self.damage = 10

        #----- Buscamos la imagen y hacemos un rectangulo para ella ----- #
        self.image = pygame.image.load(os.path.join('./assets/movZombie/movZombie_Default/movLeft/0-zombie_default.gif'))
        self.img = pygame.transform.scale(self.image, (int(self.image.get_width() * scale ), int(self.image.get_height() * scale  )) )
        self.rect = self.img.get_rect()
        self.rect.center = (x , y)
    
    def update(self, player):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        distancia = math.sqrt(dx * dx + dy * dy)
        dx, dy = dx / distancia, dy /  distancia
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed



        # ----- Comprobar que no se salga del mapa ---- #
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT - 5:
            self.rect.bottom = HEIGHT - 5

        
    # def colitions(self, player):
    #     if player.colliderect(self.rect):
    #         player.life = -self.damage
    #         print(self.life)

    def draw(self):
        WIN.blit(pygame.transform.flip(self.img, self.flip_x, False),self.rect.center)

#-------------------- Clase de balas --------------------------#
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direccion_x, direccion_y):
        pygame.sprite.Sprite.__init__(self)
        
        # ------- Caracteristicas de la bala ----------#
        self.speed_x = speed
        self.speed_y = speed
        self.direccion_x = direccion_x
        self.direccion_y = direccion_y

        #----- Buscamos la imagen y hacemos un rectangulo para ella ----- #
        self.image = pygame.image.load(os.path.join('./assets/bullets/bullet_0.png'))
        self.img_bullet = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.1 ), int(self.image.get_height() * 0.1  )) )
        self.rect = self.img_bullet.get_rect()
        self.rect.center = (x , y)


    def update(self):
        # --- movimiento de la bala ---#
        self.rect.x += self.speed_x * self.direccion_x
        self.rect.y += self.speed_y * self.direccion_y



    def draw(self):
        WIN.blit(self.img_bullet, self.rect.center)

# ------ Creamos lo jugadores -------#
all_sprites = pygame.sprite.Group()

player1 = Player(50, 50, 0.5, 5)
player2 = Player(100, 50, 0.5, 5)

all_sprites.add(player1)
all_sprites.add(player2)

zombies_group = pygame.sprite.Group()

bullets_group = pygame.sprite.Group()

# ------ Timepo en un instante --- #
time = pygame.time.get_ticks() // 1000
print(time)

if time % 5 == 0:
    zombie = Zombie(1000, 900, 0.5, 2)
    zombies_group.add(zombie)

#-------------------- Bucle Principal del juego --------------------------#
def main():
    #Definir variable de movimiento para jugardor 1
    moving_left_p1 = False
    moving_right_p1 = False
    moving_up_p1 = False
    moving_down_p1 = False
    shotting_p1 = False
    
    #Definir variable de movimiento para jugardor 2
    moving_left_p2 = False
    moving_right_p2 = False
    moving_up_p2 = False
    moving_down_p2 = False
    shotting_p2 = False
    
    

    while True:
        # -- definimos tiempo --#
        

        #---- Clock ----#
        clock.tick(FPS)
        

        #-------------- Main menu ----------------#
        def main_menu():
            #--- Se pinta la pantalla ---#
            WIN.fill(RED_WINE)

            #--- Se actualiza la pantalla ---#
            pygame.display.update()

        
        
        def in_game():
            #--- Se pinta la pantalla ---#
            WIN.fill(RED_WINE)

            # ------- creamos los zombies ----------#
            
            

            #--- Dibujamos a los jugadores y actualizamos---#
            player1.update(moving_left_p1, moving_right_p1, moving_up_p1, moving_down_p1, shotting_p1)
            player2.update(moving_left_p2, moving_right_p2, moving_up_p2, moving_down_p2, shotting_p2)

            bullets_group.update() # Balas
            zombies_group.update(player1) # Zombies
            zombies_group.update(player2) # Zombies

            # Colision de zombies con los jugadores
            hits = pygame.sprite.groupcollide(zombies_group, bullets_group, False, True)

            for hit in hits:
                print(hit)
                print('le cayo al zombie')

            attacks = pygame.sprite.spritecollide(player1, zombies_group, True)

            for attack in attacks:
                player1.life -= 25
                attack.kill()

            player1.draw()
            player2.draw()
            bullets_group.draw(WIN) # Balas
            zombies_group.draw(WIN) #  Zombies

        in_game()

        #--- Se actualiza la pantalla ---#
        pygame.display.update()




        # ----- Eventos del juego --------#
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

# ------------ Teclas para los jugadores ------------- #

            # ---- Presiona las teclas ------ #
            if event.type == pygame.KEYDOWN:
                # ---- Player 1 --- #
                if event.key == pygame.K_a:
                    moving_left_p1 = True

                if event.key == pygame.K_d:
                    moving_right_p1 = True
                if event.key == pygame.K_w:
                    moving_up_p1 = True
                if event.key == pygame.K_s:
                    moving_down_p1 = True
                if event.key == pygame.K_SPACE:
                    shotting_p1 = True
                    
                # ---- Player 2 --- #
                if event.key == pygame.K_LEFT:
                    moving_left_p2 = True
                if event.key == pygame.K_RIGHT:
                    moving_right_p2 = True
                if event.key == pygame.K_UP:
                    moving_up_p2 = True
                if event.key == pygame.K_DOWN:
                    moving_down_p2 = True
                if event.key == pygame.K_COMMA:
                    shotting_p2 = True

            # ---- Suelta las teclas ------ #

            if event.type == pygame.KEYUP:
                # ---- Player 1 --- #
                if event.key == pygame.K_a:
                    moving_left_p1 = False
                if event.key == pygame.K_d:
                    moving_right_p1 = False
                if event.key == pygame.K_w:
                    moving_up_p1 = False
                if event.key == pygame.K_s:
                    moving_down_p1 = False
                if event.key == pygame.K_SPACE:
                    shotting_p1 = False

                # ---- Player 2 --- #
                if event.key == pygame.K_LEFT:
                    moving_left_p2 = False
                if event.key == pygame.K_RIGHT:
                    moving_right_p2 = False
                if event.key == pygame.K_UP:
                    moving_up_p2 = False
                if event.key == pygame.K_DOWN:
                    moving_down_p2 = False
                if event.key == pygame.K_COMMA:
                    shotting_p2 = False
            
        
main()