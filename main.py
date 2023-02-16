import pygame
import os
import random
import math
import csv
import math


# --------------- COMENTARIOS ----------------------#
# INTEGRANTES:
# Max Bryam Antúnez Alfaro
# Joaquín Alonso Galvez Menendez
# Enzo Gabriel Camizan Vidal
# Alexandro Martin Chamochumbi Gutierrez
# Renato Aurelio Cernades Ames

#LINK DEL VIDEO: https://youtu.be/GcSHyXNjMkY


pygame.init()
pygame.mixer.init()

#Colores
WHITE, BLACK = (255,255,255), (0,0,0)
RED_WINE, RED = (139, 5, 5), (234, 48, 48)
YELLOW = (255, 227, 68)
GREEN_LIFE, GREEN_DARK = (61, 216, 94), (39, 169, 66)

# Imgagenes

image_zombie = pygame.image.load(os.path.join('./assets/movZombie/movZombie_Default/movLeft/0-zombie_default.gif'))

image_bullet = pygame.image.load(os.path.join('./assets/bullets/bullet4.png'))
image_bullet2 = pygame.image.load(os.path.join('./assets/bullets/bullet5.png'))

image_background_menu = pygame.image.load(os.path.join('./assets/menu_background.jpg'))
image_menu_pause = pygame.image.load(os.path.join('./assets/menu_pause.jpg'))
image_fondo_negro = pygame.image.load(os.path.join('./assets/fondonegro.jpg'))
image_gameover_background = pygame.image.load(os.path.join('./assets/gameover_background1.jpg'))
image_mute = pygame.image.load(os.path.join('./assets/mute.png'))


#punteros
image_ponter1 = pygame.image.load(os.path.join('./assets/pointers/pointer2.png'))

# Sonidos
menu_song = pygame.mixer.Sound('./sounds/menu_song.ogg')
final_song = pygame.mixer.Sound('./sounds/sonido_final.mp3')
bullet_sound = pygame.mixer.Sound('./assets/sounds/bullet_sound.wav')
reloading_sound1 = pygame.mixer.Sound('./assets/sounds/reloading_sound1.mp3')
# reloading_sound2 = pygame.mixer.Sound('./assets/sounds/reloading_sound2.mp3')
zombie_sound1 = pygame.mixer.Sound('./assets/sounds/zombie_sound1.mp3')
zombie_sound2 = pygame.mixer.Sound('./assets/sounds/zombie_sound2.mp3')

maxhealth_sound = pygame.mixer.Sound('./assets/sounds/maxhealth_sound.mp3')
maxdamage_sound = pygame.mixer.Sound('./assets/sounds/max_damage_sound.mp3')
Max_Ammo_sound = pygame.mixer.Sound('./assets/sounds/Max_Ammo_sound.mp3')



#-------------------- Pantalla --------------------------#
WIDTH = 1500 
HEIGHT = int(WIDTH * 0.6)
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # 1500/900 = 15/9 = 5/3


# Grid

COLUMS = 30
ROWS = 18

SIZE_X = WIDTH // COLUMS
SIZE_Y = HEIGHT // ROWS




# Fotogramas por segundos
clock = pygame.time.Clock()
FPS = 35

def draw_pointer(img, mouse_x, mouse_y):
    size = (40, 40)
    image = pygame.transform.scale(img, size)
    WIN.blit(image, (mouse_x + 10, mouse_y + 10) )

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
    pygame.draw.rect(WIN, WHITE, hitbox, 5)

def draw_background(image):
    scale_window = pygame.transform.scale(image, (WIDTH, HEIGHT))
    WIN.blit(scale_window,(0,0))

def text(word,color, x, y,size_text, fill):
    FONT = pygame.font.SysFont('Impact', size_text)
    text = pygame.Rect(x, y,  size_text*7,  size_text)
    button = pygame.Rect(x, y,  size_text*3,  size_text)
    
    if text.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(WIN, BLACK, text, fill)
        text = FONT.render(word, True, YELLOW)
    else:
        pygame.draw.rect(WIN, WHITE, text, fill)
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
        self.shoot_cooldown = 40
        self.max_ammo = 280
        self.guncharger = 60
        self.reloading_time = 200
        self.damage = 25
        self.id = id



        #----- Buscamos la imagen y hacemos un rectangulo para ella ----- #
        self.image_player_idle = [pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/idle/idle01.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/idle/idle02.png'))]
            
        self.image_player_run = [pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/running/run1.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/running/run2.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/running/run3.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/running/run4.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/running/run5.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/running/run6.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/running/run7.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/running/run8.png'))]
        
        self.image_player_shoot = [pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/shooting/shooting1.01.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/shooting/shooting1.02.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/shooting/shooting1.03.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/shooting/shooting1.04.png')),]

        self.image_player_died = [pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/shooting/shooting1.01.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/dead/dead02.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/dead/dead03.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/dead/dead04.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/dead/dead05.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/dead/dead06.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/dead/dead07.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/dead/dead08.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/dead/dead09.png')),
                            pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/dead/dead10.png'))]
        
        # image_player_shoot = [pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/shooting1.01.png')),
                            # pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/shooting1.02.png')),
                            # pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/shooting1.03.png')),
                            # pygame.image.load(os.path.join('./assets/movPlayer/movPlayer1/files/shooting1.04.png'))]
        
        self.sheet_idle = self.image_player_idle
        
        self.sheet_idle[0].set_clip(pygame.Rect(0, 0, 40, 40))

        self.image = self.sheet_idle[0].subsurface(self.sheet_idle[0].get_clip())
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.movement_sheet = self.sheet_idle
        self.frame = 0

    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > len(frame_set) - 1:
            self.frame = 0

        return frame_set[self.frame]

    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))

        return clipped_rect

    def update(self, moving_left, moving_right, moving_up, moving_down, shotting, reloading ,walls_group):
        dx = 0
        dy = 0
        
        #--- Movimientos del jugador ----#
        if self.life >= 1:
            if moving_left == True:
                
                dx = -self.speed
                self.flip_x = True
                self.direccion_x = -1
                self.direccion_y = 0
                self.movement_sheet = self.image_player_run
            elif moving_right == True:
                
                dx =  self.speed
                self.flip_x = False
                self.direccion_x = 1
                self.direccion_y = 0
                self.movement_sheet = self.image_player_run
            else:
                self.movement_sheet = self.image_player_idle

            if moving_up == True:
                
                dy = -self.speed
                self.direccion_x = 0
                self.direccion_y = -1
                self.movement_sheet = self.image_player_run
            elif moving_down == True:
                
                dy = self.speed
                self.direccion_x = 0
                self.direccion_y = 1
                self.movement_sheet = self.image_player_run
        
            #--- Dispara el jugador ----#
            
            if shotting == True and self.shoot_cooldown >= 20 and self.guncharger > 0 and self.reloading_time >= 100:
                bullet_sound.play()
                self.shoot_cooldown = 0
                self.guncharger -= 1
                bullets = Bullet(self.rect.x, self.rect.y, 10, self.direccion_x, self.direccion_y, 'player')
                bullets_group.add(bullets)
                self.movement_sheet = self.image_player_shoot
                

            if reloading == True and self.reloading_time >= 100 and self.max_ammo > 0:
                reloading_sound1.play(2)
                self.reloading_time = 0
                self.max_ammo -= 60 - self.guncharger
                self.guncharger += 60 - self.guncharger
                  
            if self.reloading_time < 100:
                self.reloading_time += 1

            if self.shoot_cooldown < 20:
                self.shoot_cooldown += 1

            # ------------- frames ---------------#
            self.frame += 1
            if self.frame > len(self.movement_sheet) - 1:
                self.frame = 0
            self.image = self.movement_sheet[self.frame].subsurface(self.movement_sheet[self.frame].get_clip())
        else:
            self.movement_sheet = self.image_player_died
            self.frame += 1
            if self.frame > len(self.movement_sheet) - 1:
                self.frame = 0
                self.kill()
            self.image = self.movement_sheet[self.frame].subsurface(self.movement_sheet[self.frame].get_clip())
            
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
    
    def oneplayershoot(self,reloading, shoot):

        # ------ Disparar -------#
        if shoot == True and self.guncharger > 0 and self.shoot_cooldown >= 30 and self.reloading_time >= 100:
            bullet_sound.play()
            self.guncharger -= 1
            a, b = pygame.mouse.get_pos()
            rx = (a - self.rect.x)
            ry = (b - self.rect.y)

            bullet = Bullet(0, 0, 0.08 , 1, 1, 'player')
            bullet.ejex = rx
            bullet.ejey = ry
            bullet.rect.x = self.rect.x
            bullet.rect.y = self.rect.y
            bullets_group.add(bullet)
            self.movement_sheet = self.image_player_shoot
            

    def draw(self):
        WIN.blit(pygame.transform.flip(self.image, self.flip_x, False), (self.rect.x, self.rect.y))
        
#-------------------- Clase del Zombie --------------------------#
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # ------- Caracteristicas del zombie ----------#
        self.speed = 1.4
        self.flip_x = False
        self.life = 100
        self.damage = 8
        self.follow = random.randint(1, 2)
        self.shoot_time = 300

        
        #----- Buscamos la imagen y hacemos un rectangulo para ella ----- #
        sheet = image_zombie
        self.image = pygame.transform.scale(sheet, (int(SIZE_X - 10), int(SIZE_Y- 10)) )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self, player, walls_group, dificulty):
        # if player.id == self.follow:
        

        # ----- Seguimiento del zombie ---- #
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        distancia = math.sqrt((dx * dx) + (dy * dy))
        dx, dy = dx / distancia, dy /  distancia
        
        
        #----- Comprobar colision con el muro ---- #
        for wall in walls_group:
            if wall.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.rect.width, self.rect.height):
                dx = 0
                dy = 1
                if wall.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.rect.width, self.rect.height):
                    dy = 0
                    dx = 1
                    
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # ----- disparos del zombie ---- #
        
        # if self.shoot_time >= 300:
        #     self.shoot_time = 0
        #     bullet = Bullet(self.rect.x, self.rect.y, 10, dx, dy, 'zombie')
        #     bullet.ejex = dx
        #     bullet.ejey = dy
        #     bullets_group.add(bullet)
     
        # if self.shoot_time < 300:
        #     self.shoot_time += 1

        #----- DIFICULTADES ---- #
        
        if dificulty == 0:
            self.damage = 8

        elif dificulty == 1:
            self.damage = 15

        elif dificulty == 2:
            self.damage = 40
        
        
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
    def __init__(self, x, y, speed, direccion_x, direccion_y, type):
        pygame.sprite.Sprite.__init__(self)
        
        # ------- Caracteristicas de la bala ----------#
        self.speed_x = speed
        self.speed_y = speed
        self.direccion_x = direccion_x
        self.direccion_y = direccion_y
        self.type = type

        if self.type == 'player':
            self.img_bullet = image_bullet
        elif self.type == 'zombie':
            self.img_bullet = image_bullet2

        #----- Buscamos la imagen y hacemos un rectangulo para ella ----- #
        
        self.image = pygame.transform.scale(self.img_bullet, (int(0.2*SIZE_X), int(0.2*SIZE_Y) ) )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self):
        # --- movimiento de la bala ---#
        self.rect.x += self.speed_x * self.direccion_x
        self.rect.y += self.speed_y * self.direccion_y

    def update_oneplayer(self):
        self.rect.x += self.ejex * self.speed_x
        self.rect.y += self.ejey * self.speed_y

        for wall in walls_group:
            if wall.rect.colliderect(self.rect):
                self.kill()


    def draw(self):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

#-------------------- Clase de paredes --------------------------#
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join('./assets/walls/wall{}.png'.format(LEVEL)))
        self.image = pygame.transform.scale(img, (SIZE_X, SIZE_Y) )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if LEVEL == 2:
            img = pygame.image.load(os.path.join('./assets/walls/wall2.png'))
            self.image = pygame.transform.scale(img, (SIZE_X, SIZE_Y))
        if LEVEL == 3:
            img = pygame.image.load(os.path.join('./assets/walls/wall3.png'))
            self.image = pygame.transform.scale(img, (SIZE_X, SIZE_Y))
        if LEVEL == 4:
            img = pygame.image.load(os.path.join('./assets/walls/wall4.png'))
            self.image = pygame.transform.scale(img, (SIZE_X, SIZE_Y))
        if LEVEL == 5:
            img = pygame.image.load(os.path.join('./assets/walls/wall5.png'))
            self.image = pygame.transform.scale(img, (SIZE_X, SIZE_Y))
        

    def draw(self):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

#-------------------- Clase de spawns --------------------------#
class Z_spawn(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.zombies_count = 10
        self.spawn_time = 200

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

    def update(self):
        cont = 0
        rand_time = random.randint(200, 350)
        if self.spawn_time >= rand_time and cont <= self.zombies_count:
            for i in range(1):
                zombie_sound1.set_volume(0.1)
                zombie_sound1.play()
                zombie = Zombie(self.x, self.y)
                zombies_group.add(zombie)
                cont += 1
            self.spawn_time = 0

        if self.spawn_time < rand_time:
            self.spawn_time += 1
 
#-------------------- Clase de items d
class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image_item = pygame.image.load(os.path.join('./assets/items/{}.png'.format(self.type)))
        self.image = pygame.transform.scale(self.image_item, (SIZE_X, SIZE_Y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.time = 0

    def update(self, player):
        if player.rect.colliderect(self.rect):
            if self.type == 'maxhealth':
                maxhealth_sound.play()
                player.life = 100
                self.kill()

            if self.type == 'maxammo':
                Max_Ammo_sound.play()
                player.max_ammo = 260
                player.guncharger = 60
                self.kill()

            if self.type == 'maxdamage':
                maxdamage_sound.play()
                player.damage = 40
                self.kill()
                print('damga')

            if self.type == 'maxspeed':
                player.speed = 4
                self.kill()
            
    def draw(self):
        WIN.blit(self.image, (self.rect.x, self.rect.y))
   
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
                if space == 0:
                    wall = Wall(x * SIZE_X, y * SIZE_Y)
                    walls_group.add(wall)
                if space == 1:
                    player1 = Player( x * SIZE_X, y * SIZE_Y, 2, 1)
                    
                if space == 2:
                    player2 = Player(x * SIZE_X, y * SIZE_Y, 2, 2)
    
                if space == 3:
                    spawn = Z_spawn(x * SIZE_X,y * SIZE_Y)
                    z_spawn_group.add(spawn)
                if space == 4:
                    type = ''
                    i = random.randint(1, 4)
                    if i == 1:
                        type = 'maxhealth'
                    if i == 2:
                        type = 'maxammo'
                    if i == 3:
                        type = 'maxdamage'
                    if i == 4:
                        type= 'maxspeed'
                    item = Item(x * SIZE_X, y * SIZE_Y, type)
                    items_group.add(item)
                
        return player1, player2


# ------ Creamos los grupos de sprites -------#
walls_group = pygame.sprite.Group()
zombies_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
z_spawn_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()

def clear_sprites():
    pygame.sprite.Group.empty(walls_group)
    pygame.sprite.Group.empty(bullets_group)
    
# ------ Timepo en un instante --- #
time = pygame.time.get_ticks() // 1000
print(time)

def main():
    global SCORE_GAME
    global LEVEL
    DIFICULTY = 1
     # score
    SCORE_GAME = 0
    LEVEL = 1
    running = True
    #Definir variable de movimiento para jugardor 1
    moving_left_p1 = False
    moving_right_p1 = False
    moving_up_p1 = False
    moving_down_p1 = False
    shotting_p1 = False
    shoot = False
    reloading_p1 = False
    
    #Definir variable de movimiento para jugardor 2
    moving_left_p2 = False
    moving_right_p2 = False
    moving_up_p2 = False
    moving_down_p2 = False
    shotting_p2 = False
    reloading_p2 = False

    # --------- Cargando el mapa ----------#
    def loadingmap():
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
        return player1, player2
    
    player1, player2 = loadingmap()
    

    # varible para seleccionar un boton
    button_selected = 0

    #--- MUSICA ---#
    if button_selected == 0:
        menu_song.set_volume(0.2)
        menu_song.play(-1)
        final_song.set_volume(0.0)
        final_song.play(-1)
    
    # desaparecemos el puntero
    pygame.mouse.set_visible(False)
    
#-------------------- Bucle Principal del juego --------------------------#
    active = False
    txt = ''
    numplayers = 0
    mute = False
    while running:
        # levels #

        if SCORE_GAME == 0:
            LEVEL = 1
        if SCORE_GAME == 1000:
            LEVEL = 2
            SCORE_GAME = 1100
            button_selected = 10
        if SCORE_GAME == 2000:
            LEVEL = 3
            SCORE_GAME = 2100
            button_selected = 10
        if SCORE_GAME == 3000:
            LEVEL = 4
            SCORE_GAME = 3100
            button_selected = 10
        if SCORE_GAME == 6000:
            LEVEL = 5
            SCORE_GAME = 6100
            button_selected = 10
        if SCORE_GAME >= 7000:
            button_selected = 11

        
        #---- Clock ----#
        clock.tick(FPS)
        
        #menu song
        if mute:
            menu_song.set_volume(0.0)
        else:
            menu_song.set_volume(0.2)

        #-------------- Main menu ----------------#
        def main_menu(button, numplayers):
            #--- Se pinta la pantalla ---#
            WIN.fill(WHITE)
            draw_background(image_background_menu)
            text('DANGER ZONE',YELLOW , WIDTH//2 - 400, HEIGHT//2 - 300, 150, -1)
            button1 = text('1 PLAYER',WHITE, WIDTH//2 - 250, HEIGHT//2 - 100, 60, -1)
            button2 = text('2 PLAYERS',WHITE, WIDTH//2 , HEIGHT//2 - 100, 60, -1)
            button3 = text('LEADERBOARD',WHITE, WIDTH//2 - 200, HEIGHT//2, 60, -1)
            button4 = text('OPTIONS',WHITE, WIDTH//2 - 130, HEIGHT//2 + 100, 60, -1)
            button5 = text('EXIT',WHITE, WIDTH//2 - 80, HEIGHT//2 + 200, 60, -1)
            
           
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
                        numplayers = 2
                        player1.life = 100
                        player2.life = 100
                        button = 9
                    if button1.collidepoint(pygame.mouse.get_pos()):
                        print('1 player')
                        player1.life = 100
                        numplayers = 1
                        button = 9
                    
            return button, numplayers

        
        if button_selected == 0:
            final_song.set_volume(0.0)
            button_selected, numplayers = main_menu(button_selected, numplayers)

        elif button_selected == 1:
            menu_song.set_volume(0.1)
            final_song.set_volume(0.0)
            walls_group.update()
            walls_group.draw(WIN)
            SCORE_GAME, button_selected = in_game_singleplayer(SCORE_GAME, button_selected)
            
        elif button_selected == 2:
            menu_song.set_volume(0.1)
            final_song.set_volume(0.0)
            SCORE_GAME, button_selected = in_game_multiplayer( SCORE_GAME, button_selected)
        
        elif button_selected == 3:
            menu_song.set_volume(0.1)
            final_song.set_volume(0.0)
            button_selected = leaderboard(button_selected)

        elif button_selected == 4:
            final_song.set_volume(0.0)
            button_selected, mute = show_options(button_selected, mute)

        elif button_selected == 5:
            final_song.set_volume(0.0)
            button_selected = pause_oneplayer(button_selected)

        elif button_selected == 6:
            final_song.set_volume(0.0)
            button_selected = pause_twoplayers(button_selected)

        elif button_selected == 7:
            menu_song.set_volume(0.0)
            final_song.set_volume(0.2)
            button_selected = gameover(button_selected)

        elif button_selected == 8:
            menu_song.set_volume(0.0)
            final_song.set_volume(0.2)
            button_selected, active, txt = save_score(button_selected, active, txt)

        elif button_selected == 9:
            menu_song.set_volume(0.1)
            final_song.set_volume(0.0)
            button_selected, DIFICULTY = dificulties(button_selected, DIFICULTY)

        elif button_selected == 10:
            menu_song.set_volume(0.3)
            player1, player2, button_selected  = pass_level(player1, player2, button_selected)

        elif button_selected == 11:
            button_selected = win(button_selected)

        def win(button):
            draw_background(image_menu_pause)
            text('CONGRATULATIONS', WHITE, WIDTH//2 - 200, HEIGHT//2 -100, 90, -1)
            button2 = text('BACK TO MENU', WHITE, WIDTH - 350, HEIGHT - 100, 60, -1)
            button3 = text('SAVE SCORE', WHITE, 100, HEIGHT - 100, 60, -1)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button3.collidepoint(pygame.mouse.get_pos()):
                        button = 8                  
                    if button2.collidepoint(pygame.mouse.get_pos()):
                        button = 0

            return button

        def pass_level(player1, player2, button_selected ):
            WIN.fill(BLACK)
            boton1=text('PASS LEVEL', WHITE, WIDTH//2- 200, HEIGHT//2, 80, -1 )
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if boton1.collidepoint(pygame.mouse.get_pos()):
                        clear_sprites()
                        button_selected = 1

            return player1, player2, button_selected 

        def dificulties(button_selected, dificulty):
            draw_background(image_background_menu)
            boton1 = text('EASY', WHITE, WIDTH//3-300, HEIGHT//3, 70, -1)
            boton2 = text('SURVIVOR', WHITE, WIDTH//3+50, HEIGHT//3, 70, -1)
            boton3 = text('APOCALYPSE', WHITE, WIDTH//3+500, HEIGHT//3, 70, -1)
            boton4 = text('START', WHITE, WIDTH-200, HEIGHT - 100, 70, -1)
            boton5 = text('RETURN', WHITE, 50, HEIGHT - 100, 70, -1)

            # ----- FUNCION DE LOS BOTONES ----- #
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if boton1.collidepoint(pygame.mouse.get_pos()):
                        
                        dificulty = 0
                    elif boton2.collidepoint(pygame.mouse.get_pos()):
                        
                        dificulty = 1
                        
                    elif boton3.collidepoint(pygame.mouse.get_pos()):
                        
                        dificulty = 2
                        

                    if boton4.collidepoint(pygame.mouse.get_pos()):
                        button_selected = numplayers

                    if boton5.collidepoint(pygame.mouse.get_pos()):
                        button_selected = 0
                        


            return button_selected, dificulty

        def leaderboard(button_selected):
            draw_background(image_background_menu)
            file = open('./scores/allscores.txt', 'r')
            dic_scores = {
            }
            list_score = []
            for line in file:
                if line != '':
                    list = line.split(' ')
                    name = list[0]
                    score = list[1]
                    list_score.append(score)
                    dic_scores[name] = score

            dic_sorted = {}
            list_score.sort(reverse=True)
            for i  in range(len(list_score)):
                for name in dic_scores:
                    if list_score[i] == dic_scores[name]:
                        dic_sorted[name] = list_score[i]

            # -------- IMPRIMIR LOS PUNTAJES ------#
            text('LEADERBOARD', WHITE, WIDTH//2 - 200, 200, 80, -1)
            for i, name in enumerate(dic_sorted):
                if 300 + i*20 <= HEIGHT - 100:
                    text(name + '   ' + dic_sorted[name], WHITE, WIDTH//2 - 250, 300 + i*80, 60, -1)

            # BOTONES ---#
            boton1 = text('RETURN', WHITE, 10, HEIGHT- 100, 50, -1)

            # ----- FUNCION DE LOS BOTONES ----- #
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:   
                    if boton1.collidepoint(pygame.mouse.get_pos()):
                        button_selected = 0

            return button_selected
    
        def saving_score(text, score):
            file = open('./scores/allscores.txt', 'a+')
            file.write('\n{} {}'.format(text, score))

        def save_score(button_selected, active, txt):
            
            WIN.fill(BLACK)

            text('WHAT IS YOUR NAME?'.format(SCORE_GAME), WHITE, 10, 100, 70, -1)
            text('      ', (100, 100, 100) , 10, 210, 80, 5)
            input_box = text(txt, WHITE, 10, 200, 80, -1)
            text('YOUR SCORE WAS {}'.format(SCORE_GAME), WHITE, 10, 600, 50, -1)
            boton1 = text('BACK TO MENU',WHITE, 10, 800, 50, -1)
            boton2 = text('SAVE',WHITE, 10, 290, 50, -1)
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(pygame.mouse.get_pos()):
                        active = not active
                    if boton1.collidepoint(pygame.mouse.get_pos()):
                        button_selected = 0
                    if boton2.collidepoint(pygame.mouse.get_pos()):
                        saving_score(txt, SCORE_GAME)
                        button_selected = 0
                
                if event.type == pygame.KEYDOWN:
                    print(active)
                    if active:
                        if event.key == pygame.K_RETURN:
                            txt = ''
                        elif event.key == pygame.K_BACKSPACE:
                            txt = txt[:-1]
                        else:
                            if len(txt) <= 8:
                                txt += event.unicode
                                print(event.unicode)
                        if event.key == pygame.K_KP_ENTER:
                            active = not active
                    
            return button_selected, active, txt
     
        def show_options(button, mute):
            #--- Se pinta la pantalla ---#
            WIN.fill(WHITE)
            draw_background(image_background_menu)

            rect = image_mute.get_rect()
            WIN.blit(image_mute, (WIDTH//2- 50, HEIGHT//2 - 100))

            text('OPTIONS',YELLOW, WIDTH//2 - 250, HEIGHT//2 - 250, 90, -1)

            button1 = text('RETURN',WHITE, WIDTH//2 - 250, HEIGHT - 300, 60, -1)
            button2 = text('MUTE',WHITE, WIDTH//2 - 250, HEIGHT//2 - 100, 60, -1)
            #--- Se actualiza la pantalla ---#
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                    if button1.collidepoint(pygame.mouse.get_pos()):
                        print('return')
                        button = 0
                    if rect.collidepoint(pygame.mouse.get_pos()) or button2.collidepoint(pygame.mouse.get_pos()):
                        mute = not mute

            return button, mute

        def pause_oneplayer(button):
            image_fondo_negro.set_alpha(100) # BACKGROUND TRANSPARENTE
            draw_background(image_fondo_negro)
            
            text('PAUSE', WHITE, WIDTH//2 - 500, HEIGHT//2 - 300, 120, -1)
            button1 = text('RETURN MENU', WHITE, WIDTH//2 - 500, HEIGHT//2 + 100, 60, -1)
            button2 = text('PLAY', WHITE, WIDTH//2 - 500, HEIGHT//2 + 200, 60, -1)
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                    if button1.collidepoint(pygame.mouse.get_pos()):
                        print('volver al menu')
                        player1.life = 100
                        player2.life = 100
                        button = 0
                    if button2.collidepoint(pygame.mouse.get_pos()):
                        print('PLAY')
                        button = 1
                        

            return button

        def pause_twoplayers(button):
            image_fondo_negro.set_alpha(100) # BACKGROUND TRANSPARENTE
            pygame.mouse.set_visible(False)
            draw_background(image_fondo_negro)
            
            text('PAUSE', WHITE, WIDTH//2 - 500, HEIGHT//2 - 300, 120, -1)
            button1 = text('RETURN MENU', WHITE, WIDTH//2 - 500, HEIGHT//2 + 100, 60, -1)
            button2 = text('PLAY', WHITE, WIDTH//2 - 500, HEIGHT//2 + 200, 60, -1)
            
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
            button1 = text('SAVE YOUR SCORE', WHITE, 0, HEIGHT - 100, 60, -1)
            button2 = text('BACK TO MENU', WHITE, WIDTH - 350, HEIGHT - 100, 60, -1)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                    if button1.collidepoint(pygame.mouse.get_pos()):
                        print('guardar score')
                        button = 8
                    if button2.collidepoint(pygame.mouse.get_pos()):
                        player1.life = 100
                        player2.life = 100
                        button = 0

            return button

        def in_game_multiplayer(SCORE_GAME,button):
            
            #--- Se pinta la pantalla ---#
            draw_background(pygame.image.load(os.path.join('./assets/levels/level{}.jpg'.format(LEVEL))))
            
            # ---Sonidos del mapa ---#
            # zombie_sound2.play()
            

            # ---Comprobar si el jugador está vivo ---#
            if player1.life <= 0 and player2.life <= 0:
                button = 7
            
            # ------- creamos los zombies ----------#
            # NO OLVIDAR PONER LOS SPAWNS DE ZOMBIES EN EL EXCEL DEL PMAP
            
            #--- Dibujamos a los jugadores y actualizamos---#
            player1.update(moving_left_p1, moving_right_p1, moving_up_p1, moving_down_p1, shotting_p1, reloading_p1, walls_group)
            player2.update(moving_left_p2, moving_right_p2, moving_up_p2, moving_down_p2, shotting_p2, reloading_p2, walls_group)
            
            
            # bullets_group.update() # Balas
            z_spawn_group.update()
            zombies_group.update(player1, walls_group, DIFICULTY) # Zombies
            
            #actualizamos los items
            items_group.update(player1)
            items_group.update(player2)

            # ---- barra de vida de los zombies---#
            
            for zombie in zombies_group:
                health_bar(WIN, zombie.rect.x, zombie.rect.y, zombie.life)
                if zombie.life <= 0:
                    SCORE_GAME +=  100
                    zombie.kill()
                
            for bullet in bullets_group:
                bullet.update()
                
            # Colision de zombies con los jugadores
            hits = pygame.sprite.groupcollide(zombies_group, bullets_group, False, True)

            for hit in hits:
                hit.bleed(player1)
                
            attacks = pygame.sprite.spritecollide(player1, zombies_group, True)

            for attack in attacks:
                player1.life -= attack.damage
                attack.kill()
            
            attacks = pygame.sprite.spritecollide(player2, zombies_group, True)

            for attack in attacks:
                player2.life -= attack.damage
                attack.kill()

            
            bullets_group.draw(WIN) # Balas
            zombies_group.draw(WIN) #  Zombies
            walls_group.draw(WIN) #muros
            items_group.draw(WIN) #items
            player1.draw()
            player2.draw()



            # ------- Barra de vida y balas de los jugadores ---------- #
            text('P2', WHITE, WIDTH - 500, HEIGHT - 60, 50, -1)
            text('P1', WHITE, 5, HEIGHT - 60, 50, -1)
            
            
            life_bar(WIN, 70, HEIGHT - 25, player1.life)
            life_bar(WIN, WIDTH - 400, HEIGHT - 25, player2.life)

            text('{}/{}'.format(player1.guncharger, player1.max_ammo), WHITE, 350, HEIGHT - 60, 50, -1)
            text('{}/{}'.format(player2.guncharger, player2.max_ammo), WHITE, WIDTH-100, HEIGHT - 60, 50, -1)

            text('{}'.format(SCORE_GAME), WHITE, WIDTH//2, 0, 45, -1)
            
    

            return SCORE_GAME, button

        def in_game_singleplayer(SCORE_GAME,button):
            

            #--- Se pinta la pantalla ---#
            draw_background(pygame.image.load(os.path.join('./assets/levels/level{}.jpg'.format(LEVEL))))
            
            # ---Sonidos del mapa ---#
            # zombie_sound2.play()
            

            # ---Comprobar si el jugador está vivo ---#

            if player1.life <= 0:
                button = 7

            # ------- creamos los zombies ----------#
            # NO OLVIDAR PONER LOS SPAWNS DE ZOMBIES EN EL EXCEL DEL PMAP
            

            #--- Dibujamos a los jugadores y actualizamos---#
            player1.update(moving_left_p1, moving_right_p1, moving_up_p1, moving_down_p1, shotting_p1, reloading_p1, walls_group)
            
            
            walls_group.update()
            z_spawn_group.update()
            zombies_group.update(player1, walls_group, DIFICULTY) # Zombies
            
            
            

            #actualizamos los items
            items_group.update(player1)

            # ---- barra de vida de los zombies---#
            for zombie in zombies_group:
                health_bar(WIN, zombie.rect.x, zombie.rect.y, zombie.life)
                
                if zombie.life <= 0:
                    SCORE_GAME +=  100
                    zombie.kill()
                

            for bullet in bullets_group:
                bullet.update_oneplayer()
                # if bullet.rect.colliderect(player1.rect):
                #     player1.life -= 1  
                

    

            # Colision de zombies con los jugadores
            hits = pygame.sprite.groupcollide(zombies_group, bullets_group, False, True)

            for hit in hits:
                hit.bleed(player1)
                
            attacks = pygame.sprite.spritecollide(player1, zombies_group, True)

            for attack in attacks:
                player1.life -= attack.damage
                attack.kill()

            
            bullets_group.draw(WIN) # Balas
            zombies_group.draw(WIN) #  Zombies
            walls_group.draw(WIN) #muros
            items_group.draw(WIN) #items
            player1.draw()


            # ------- Barra de vida y balas de los jugadores ---------- #
            text('P1', WHITE, 5, HEIGHT - 60, 50, -1)
            
            
            life_bar(WIN, 70, HEIGHT - 25, player1.life)
            

            text('{}/{}'.format(player1.guncharger, player1.max_ammo), WHITE, 350, HEIGHT - 60, 50, -1)
           

            text('{}'.format(SCORE_GAME), WHITE, WIDTH//2, 5, 48, -1)


            # puntero #
            posx, posy = pygame.mouse.get_pos()
            draw_pointer(image_ponter1, posx, posy )
            # hitbox(player1)

            return SCORE_GAME, button

        
        posx, posy = pygame.mouse.get_pos()
        draw_pointer(image_ponter1, posx, posy)
        

        # #--- Se actualiza la pantalla ---#
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
                if event.key == pygame.K_r:
                    reloading_p1 = True
                if button_selected == 2:
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
                if event.key == pygame.K_m:
                    reloading_p2 = True
                    

            # ---- Player 1 --- #
            if button_selected == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    shoot = True
                    player1.oneplayershoot(reloading_p1, shoot)
                if event.type == pygame.MOUSEBUTTONUP:
                    shoot = False

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
                if event.key == pygame.K_r:
                    reloading_p1 = False

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