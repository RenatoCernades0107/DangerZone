import pygame
import os #libreria que te ayuda con el sistema operativo
import random
import math
import csv

from pygame.constants import GL_CONTEXT_RELEASE_BEHAVIOR

#Colores
WHITE, BLACK = (255,255,255), (0,0,0)
RED_WINE, RED = (139, 5, 5), (234, 48, 48)
YELLOW = (255, 227, 68)
GREEN_LIFE, GREEN_DARK = (61, 216, 94), (39, 169, 66)

# Imgagenes

image_zombie = pygame.image.load(os.path.join('./assets/movZombie/movZombie_Default/movLeft/0-zombie_default.gif'))
image_player = pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/movLeft/1-player_1.png'))
image_bullet = pygame.image.load(os.path.join('./assets/bullets/bullet1.png'))
image_wall = pygame.image.load(os.path.join('./assets/wall.jpg'))

image_background_menu = pygame.image.load(os.path.join('./assets/menu_background.jpg'))
image_menu_pause = pygame.image.load(os.path.join('./assets/menu_pause.jpg'))
image_fondo_negro = pygame.image.load(os.path.join('./assets/fondonegro.jpg'))
image_gameover_background = pygame.image.load(os.path.join('./assets/gameover_background1.jpg'))



pygame.init()
#-------------------- Pantalla --------------------------#
WIDTH = 1500 
HEIGHT = int(WIDTH * 0.6)
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # 1500/900 = 15/9 = 5/3


# Grid

COLUMS = 30
ROWS = 18

SIZE_X = WIDTH // COLUMS
SIZE_Y = HEIGHT // ROWS

LEVEL = 1



# Fotogramas por segundos
clock = pygame.time.Clock()
FPS = 60


def life_bar(surface, x, y, points):

    bar_length = 5 * SIZE_X
    bar_height = int(0.5 * SIZE_Y)

    if points < 0:
        points = 0

    fill = (points / 100) * bar_length      # filling the bar depending on the points
    outline_rect = pygame.Rect(x, y - 10, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y - 10, fill, bar_height)
    pygame.draw.rect(surface, GREEN_LIFE, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

def health_bar(surface, x, y, points):

    bar_length = 0.7 * SIZE_X
    bar_height = int(0.1 * SIZE_Y)


    fill = (points / 100) * bar_length      # filling the bar depending on the points
    outline_rect = pygame.Rect(x, y - 10, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y - 10, fill, bar_height)
    pygame.draw.rect(surface, GREEN_LIFE, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

def hitbox(chr):
    hitbox = pygame.Rect(chr.rect.x, chr.rect.y, chr.rect.w, chr.rect.h)
    pygame.draw.rect(WIN, BLACK, hitbox, 5)

def draw_background(image):
    scale_window = pygame.transform.scale(image, (WIDTH, HEIGHT))
    WIN.blit(scale_window,(0,0))

def text(word,color, x, y,size_text):
    FONT = pygame.font.SysFont('Impact', size_text)
    text = pygame.Rect(x, y,  size_text*3,  size_text)
    button = pygame.Rect(x, y,  size_text*3,  size_text)

    if text.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(WIN, BLACK, text, -1)
        text = FONT.render(word, True, YELLOW)
    else:
        pygame.draw.rect(WIN, RED_WINE, text, -1)
        text = FONT.render(word, True, color)

    WIN.blit(text, (x, y))

    return button


#-------------------- Clase del jugador --------------------------#
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, id):
        pygame.sprite.Sprite.__init__(self)
        
        # ------- Caracteristicas del jugador ----------#
        self.speed = speed
        self.flip_x = False
        self.direccion_x = 1
        self.direccion_y = 1
        self.life = 100
        self.shoot_cooldown = 30
        self.max_ammo = 60
        self.damage = 20
        self.id = id

        #----- Buscamos la imagen y hacemos un rectangulo para ella ----- #
        sheet = image_player
        self.image = pygame.transform.scale(sheet, (int(SIZE_X-10), int(SIZE_Y-10)) )
        self.rect = self.image.get_rect()
        self.rect.center = (x , y)
        

    def update(self, moving_left, moving_right, moving_up, moving_down, shotting, walls_group):
        dx = 0
        dy = 0
        
        
        #--- Movimientos del jugador ----#
        if self.life >= 1:
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
            if shotting == True and self.shoot_cooldown == 30 and self.max_ammo > 0:
                self.shoot_cooldown = 0
                bullets = Bullet(self.rect.x, self.rect.y, 10, self.direccion_x, self.direccion_y)
                bullets_group.add(bullets)
                self.max_ammo -= 1
        
        
        if self.shoot_cooldown < 30:
            self.shoot_cooldown += 1
        
        # ----- Comprobar colision con el muro ---- #
        for wall in walls_group:
            if wall.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.rect.width, self.rect.height):
                dx, dy = 0, 0

        
        #--- actualizamos la posicion del jugador ----#
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
        WIN.blit(pygame.transform.flip(self.image, self.flip_x, False), (self.rect.x, self.rect.y))
        
#-------------------- Clase del Zombie --------------------------#
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # ------- Caracteristicas del zombie ----------#
        self.speed = 1.5
        self.flip_x = False
        self.life = 100
        self.damage = 10
        self.follow = random.randint(1, 2)
        

        #----- Buscamos la imagen y hacemos un rectangulo para ella ----- #
        sheet = image_zombie
        self.image = pygame.transform.scale(sheet, (int(SIZE_X), int(SIZE_Y)) )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self, player, walls_group):
        
        # ----- Seguimiento del zombie ---- #
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        distancia = math.sqrt((dx * dx) + (dy * dy))
        dx, dy = dx / distancia, dy /  distancia
        

        # ----- Comprobar colision con el muro ---- #
        for wall in walls_group:
            if wall.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.rect.width, self.rect.height):
                dx, dy = 0, 0

        
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
 
    def bleed(self, player):
        self.life -= player.damage

    def draw(self):
        WIN.blit(pygame.transform.flip(self.image, self.flip_x, False), (self.rect.x, self.rect.y))
        
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
        self.img_bullet = image_bullet
        self.image = pygame.transform.scale(self.img_bullet, (int(0.2*SIZE_X), int(0.2*SIZE_Y) ) )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self):
        # --- movimiento de la bala ---#
        self.rect.x += self.speed_x * self.direccion_x
        self.rect.y += self.speed_y * self.direccion_y



    def draw(self):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

#-------------------- Clase de paredes --------------------------#
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = image_wall
        self.image = pygame.transform.scale(img, (SIZE_X, SIZE_Y) )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


        
            

    def draw(self):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

class Z_spawn(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.zombies_count = 0
        self.spawn_time = 100

    def whatlevel(self):
        if LEVEL == 1:
            self.zombies_count = 60
        if LEVEL == 2:
            self.zombies_count = 90
        if LEVEL == 3:
            self.zombies_count = 120
        if LEVEL == 4:
            self.zombies_count = 150
        if LEVEL == 5:
            self.zombies_count = 200


    def createZombies(self):
        if self.spawn_time >= 100:
            for i in range(self.zombies_count//12):
                zombie = Zombie(self.x, self.y)
                zombies_group.add(zombie)
        else:
            self.spawn_time -= 100
    
            


#-------------------- Clase de niveles --------------------------#
class World_levels(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.objetcs = []

    def processing(self, data):
        
        # --- Procesando la data del nivel --- #
        for y, row in enumerate(data):
            for x, space in enumerate(row):
                
                if space >= -1:
                    pass
                if space <= 0 and space >= 0:
                    wall = Wall(x * SIZE_X, y * SIZE_Y)
                    walls_group.add(wall)
                if space <= 1 and space >= 1:
                    player1 = Player( x * SIZE_X,y * SIZE_Y, 5, 1)
                    
                if space <= 2 and space >= 2:
                    player2 = Player(x * SIZE_X,y * SIZE_Y, 5, 2)
    
                if space <= 3 and space >= 3:
                    zombie = Zombie(x * SIZE_X,y * SIZE_Y)
                    zombies_group.add(zombie)
                    # pass

        return player1, player2




walls_group = pygame.sprite.Group()
zombies_group = pygame.sprite.Group()


# ------ Creamos lo jugadores -------#




bullets_group = pygame.sprite.Group()



# --------- Cargando el mapa ----------#
world_data = []
for row in range(ROWS):
    r = [-1] * COLUMS
    world_data.append(r)

with open('./assets/levels/level{}.csv'.format(LEVEL), newline='') as data:
    file = csv.reader(data, delimiter=',')
    for x, line in enumerate(file) :
        for y, space in enumerate(line):
            world_data[x][y] = int(space)


world = World_levels()
player1, player2 = world.processing(world_data)



# ------ Timepo en un instante --- #
time = pygame.time.get_ticks() // 1000
print(time)



def main():
    global SCORE_GAME
     # score
    SCORE_GAME = 0
    running = True
    #Definir variable de movimiento para jugardor 1
    moving_left_p1 = False
    moving_right_p1 = False
    moving_up_p1 = False
    moving_down_p1 = False
    shotting_p1 = False
    
    #Definir variable de movimiento pa...ra jugardor 2
    moving_left_p2 = False
    moving_right_p2 = False
    moving_up_p2 = False
    moving_down_p2 = False
    shotting_p2 = False

    
    button_selected = 0
    
    
    
#-------------------- Bucle Principal del juego --------------------------#

    while running:
        # -- definimos --#
        

        #---- Clock ----#
        clock.tick(FPS)
        

        #-------------- Main menu ----------------#
        def main_menu(button):
            #--- Se pinta la pantalla ---#
            WIN.fill(WHITE)
            draw_background(image_background_menu)
            text('DANGER ZONE',YELLOW , WIDTH//2 - 400, HEIGHT//2 - 300, 150)
            button1 = text('1 PLAYER',WHITE, WIDTH//2 - 250, HEIGHT//2 - 100, 60)
            button2 = text('2 PLAYERS',WHITE, WIDTH//2 , HEIGHT//2 - 100, 60)
            button3 = text('LEADERBOARD',WHITE, WIDTH//2 - 200, HEIGHT//2, 60)
            button4 = text('OPTIONS',WHITE, WIDTH//2 - 130, HEIGHT//2 + 100, 60)
            button5 = text('EXIT',WHITE, WIDTH//2 - 80, HEIGHT//2 + 200, 60)
            #--- Se actualiza la pantalla ---#
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                    if button5.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                    if button4.collidepoint(pygame.mouse.get_pos()):
                        print('opciones')
                        button = 4
                    if button3.collidepoint(pygame.mouse.get_pos()):
                        print('puntuaciones')
                        button = 3
                    if button2.collidepoint(pygame.mouse.get_pos()):
                        print('2 players')
                        button = 2
                    if button1.collidepoint(pygame.mouse.get_pos()):
                        print('1 player')
                        button = 1
                    

            return button 

        
        if button_selected == 0:
            button_selected = main_menu(button_selected)

        elif button_selected == 1:
            SCORE_GAME, button_selected = in_game_singleplayer(SCORE_GAME, button_selected)

        elif button_selected == 2:
            SCORE_GAME, button_selected = in_game_multiplayer( SCORE_GAME, button_selected)

        elif button_selected == 3:
            pass

        elif button_selected == 4:
            button_selected = show_options(button_selected)

        elif button_selected == 5:
            button_selected = pause(button_selected)

        elif button_selected == 6:
            button_selected = gameover(button_selected)
            


        def show_options(button):
            #--- Se pinta la pantalla ---#
            WIN.fill(WHITE)
            draw_background(image_background_menu)
            text('OPTIONS',YELLOW, WIDTH//2 - 300, HEIGHT//2 - 200, 90)
            button1 = text('RETURN',WHITE, WIDTH//2 - 250, HEIGHT//2 - 100, 60)
            #--- Se actualiza la pantalla ---#
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                    if button1.collidepoint(pygame.mouse.get_pos()):
                        print('return')
                        button = 0
                    
            return button 

        def pause(button):
            image_fondo_negro.set_alpha(100) # BACKGROUND TRANSPARENTE
            draw_background(image_fondo_negro)
            
            text('PAUSE', WHITE, WIDTH//2 - 500, HEIGHT//2 - 300, 120)
            button1 = text('RETURN MENU', WHITE, WIDTH//2 - 500, HEIGHT//2 + 100, 60)
            button2 = text('PLAY', WHITE, WIDTH//2 - 500, HEIGHT//2 + 200, 60)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                    if button1.collidepoint(pygame.mouse.get_pos()):
                        print('volver al menu')
                        button = 0
                    if button2.collidepoint(pygame.mouse.get_pos()):
                        print('PLAY')
                        button = 2

            return button

        def gameover(button):
            draw_background(image_gameover_background)
            button1 = text('SAVE YOUR SCORE', WHITE, 0, HEIGHT - 100, 60)
            button2 = text('BACK TO MENU', WHITE, WIDTH - 350, HEIGHT - 100, 60)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                    if button1.collidepoint(pygame.mouse.get_pos()):
                        print('guardar score')
                        button = 0
                    if button2.collidepoint(pygame.mouse.get_pos()):
                        print('volver al menu')
                        button = 0

            return button

        def in_game_multiplayer(SCORE_GAME,button):
            
            #--- Se pinta la pantalla ---#
            WIN.fill(BLACK)
            

            # ---Comprobar si el jugador está vivo ---#

            if player1.life <= 0 and player2.life <= 0:
                button = 6

            # ------- creamos los zombies ----------#
            # NO OLVIDAR PONER LOS SPAWNS DE ZOMBIES EN EL EXCEL DEL PMAP
            

            #--- Dibujamos a los jugadores y actualizamos---#
            player1.update(moving_left_p1, moving_right_p1, moving_up_p1, moving_down_p1, shotting_p1, walls_group)
            player2.update(moving_left_p2, moving_right_p2, moving_up_p2, moving_down_p2, shotting_p2, walls_group)

            
            bullets_group.update() # Balas
            zombies_group.update(player1,  walls_group) # Zombies
            zombies_group.update(player2,  walls_group) # Zombies

            # ---- barra de vida de los zombies---#
            
            for zombie in zombies_group:
                # hitbox(zombie)
                health_bar(WIN, zombie.rect.x, zombie.rect.y, zombie.life)
                if zombie.life <= 0:
                    SCORE_GAME +=  100
                    zombie.kill()
                

            for bullet in bullets_group:
                hitbox(bullet)
            

            # Colision de zombies con los jugadores
            hits = pygame.sprite.groupcollide(zombies_group, bullets_group, False, True)

            for hit in hits:
                hit.bleed(player1)
                hit.bleed(player2)
                
            attacks = pygame.sprite.spritecollide(player1, zombies_group, True)

            for attack in attacks:
                player1.life -= 25
                attack.kill()

            attacks2 = pygame.sprite.spritecollide(player1, zombies_group, True)

            for attack in attacks2:
                player2.life -= 25
                attack.kill()
            
            bullets_group.draw(WIN) # Balas
            zombies_group.draw(WIN) #  Zombies
            walls_group.draw(WIN) #muros

            player1.draw()
            player2.draw()


            # ------- Barra de vida y balas de los jugadores ---------- #
            text('P1', WHITE, 5, HEIGHT - 60, 50)
            text('P2', WHITE, WIDTH - 500, HEIGHT - 60, 50)
            
            life_bar(WIN, 70, HEIGHT - 25, player1.life)
            life_bar(WIN, WIDTH - 400, HEIGHT - 25, player2.life)

            text('{}'.format(player1.max_ammo), WHITE, 350, HEIGHT - 60, 50)
            text('{}'.format(player2.max_ammo), WHITE, WIDTH - 100, HEIGHT - 60, 50)

            text('{}'.format(SCORE_GAME), WHITE, WIDTH//2, 5, 48)

            return SCORE_GAME, button

        def in_game_singleplayer(SCORE_GAME,button):
            #--- Se pinta la pantalla ---#
            WIN.fill(BLACK)
            

            # ---Comprobar si el jugador está vivo ---#

            if player1.life <= 0:
                button = 6

            # ------- creamos los zombies ----------#
            # NO OLVIDAR PONER LOS SPAWNS DE ZOMBIES EN EL EXCEL DEL PMAP
            

            #--- Dibujamos a los jugadores y actualizamos---#
            player1.update(moving_left_p1, moving_right_p1, moving_up_p1, moving_down_p1, shotting_p1, walls_group)
            

            bullets_group.update() # Balas
            zombies_group.update(player1, walls_group) # Zombies


            # ---- barra de vida de los zombies---#
            
            for zombie in zombies_group:
                # hitbox(zombie)
                health_bar(WIN, zombie.rect.x, zombie.rect.y, zombie.life)
                if zombie.life <= 0:
                    SCORE_GAME +=  100
                    zombie.kill()
                

            for bullet in bullets_group:
                hitbox(bullet)
            

            # Colision de zombies con los jugadores
            hits = pygame.sprite.groupcollide(zombies_group, bullets_group, False, True)

            for hit in hits:
                hit.bleed(player1)
                
            attacks = pygame.sprite.spritecollide(player1, zombies_group, True)

            for attack in attacks:
                player1.life -= 25
                attack.kill()

            
            bullets_group.draw(WIN) # Balas
            zombies_group.draw(WIN) #  Zombies
            walls_group.draw(WIN) #muros

            player1.draw()


            # ------- Barra de vida y balas de los jugadores ---------- #
            text('P1', WHITE, 5, HEIGHT - 60, 50)
            text('P2', WHITE, WIDTH - 500, HEIGHT - 60, 50)
            
            life_bar(WIN, 70, HEIGHT - 25, player1.life)
            life_bar(WIN, WIDTH - 400, HEIGHT - 25, player2.life)

            text('{}'.format(player1.max_ammo), WHITE, 350, HEIGHT - 60, 50)
            text('{}'.format(player2.max_ammo), WHITE, WIDTH - 100, HEIGHT - 60, 50)

            text('{}'.format(SCORE_GAME), WHITE, WIDTH//2, 5, 48)

            return SCORE_GAME, button



        #--- Se actualiza la pantalla ---#
        pygame.display.update()

        # ----- Eventos del juego --------#
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                

# ------------ Teclas para los jugadores ------------- #

            # ---- Presiona las teclas ------ #
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    button_selected = 5
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
            
    pygame.quit()
       
main()