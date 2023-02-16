import pygame
import os #libreria que te ayuda con el sistema operativo
import sys
import random
import math
import time

pygame.init()
pygame.mixer.init()

# pantalla
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

#Imagenes
background_menu = pygame.image.load(os.path.join('./assets/menuDangerZone45.png'))
background_lvl1 = pygame.image.load(os.path.join('./assets/backgroundlvl1.png'))

#personajes
player_width, player_height  = 120, 120
image_player1 = pygame.image.load(os.path.join('./assets/player1.gif'))
img_player1 = pygame.transform.scale(image_player1, (player_width, player_height))
player1_health = 100
player1_velocity = 10


# Zombies
zombie_default_image = pygame.image.load(os.path.join('./assets/zombie_default.gif'))
zombie_width = 100
zombie_height = 100
zombie_default_img = pygame.transform.scale(zombie_default_image, (zombie_width,zombie_height))
zombie_velocity = 2
zombie_default_health = 50

#bullets
image_bullets = pygame.image.load(os.path.join('./assets/bullet.png'))
bullet_width, bullet_height = 100, 100
img_bullets = pygame.transform.scale(image_bullets, (bullet_width, bullet_height))
#bullets settings
bullet_state = 'fire'
max_bullets_player1 = 1000
bullet_velocity = 8

#Sonidos / sound.play() para ejecutarlo
sound_select_button = pygame.mixer.Sound('./sounds/button-selected.wav')
menu_music = pygame.mixer.Sound('./sounds/Biological_Weapon.ogg')
channel=pygame.mixer.find_channel(True)
channel.set_volume(0.07)
bullets_sound = pygame.mixer.Sound('./sounds/raaaa.wav')


#Fuentes para texto
fontArial = pygame.font.SysFont('Arial', 30)


#Botones del menu
width_button, height_button  = 160, 50
button_1player = pygame.Rect(
        WIDTH/4 - width_button/4, HEIGHT/4, width_button,height_button)
text1_x, text1_y = WIDTH/4 - width_button/4 + 20, HEIGHT/4 + 5
button_2players = pygame.Rect(
        WIDTH/4 + 220 - width_button/4, HEIGHT/4, width_button,height_button)
text2_x, text2_y = WIDTH/4 + 220 - width_button/4 + 10, HEIGHT/4 + 5
button_LeaderBoard = pygame.Rect(
        WIDTH/2 - width_button/2, HEIGHT/4 + 70, width_button, height_button)
text3_x, text3_y = WIDTH/2 - width_button/4 - 30, HEIGHT/4 + 70 + 5
button_quit = pygame.Rect(
        WIDTH/2 - width_button/2, HEIGHT/4 + 140, width_button,height_button)
text4_x, text4_y = WIDTH/2 - width_button/4 + 10, HEIGHT/4 + 140 + 5

# boton para regresar
button_return = pygame.Rect(
    WIDTH/6 - width_button/2, HEIGHT - 70, width_button, height_button)
text5_x, text5_y = 65, 535
#boton para jugar
button_play = pygame.Rect(
    (WIDTH - width_button/2) - 100, HEIGHT - 70, width_button, height_button)
text6_x, text6_y = 470, 535

#Funcion para dibujar un boton
def draw_button(screen, button, word, txt_x, txt_y):
    if button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, BLACK, button, 10)
        text = fontArial.render(word, True, BLACK)
    else:
        pygame.draw.rect(screen, RED_WINE, button,10)
        text = fontArial.render(word, True, RED_WINE)
    WIN.blit(text, (txt_x, txt_y))
#Funcion para dibujar el menu
def draw_menu():
    WIN.fill(WHITE)
    WIN.blit(background_menu, (0,0))
    draw_button(WIN, button_1player, '1 jugador', text1_x, text1_y)
    draw_button(WIN, button_2players, '2 jugadores', text2_x, text2_y)
    draw_button(WIN, button_LeaderBoard, 'LeaderBoard', text3_x, text3_y)
    draw_button(WIN, button_quit, 'Salir', text4_x, text4_y)


    # WIN.blit(imagen1xd, (positionx,positiony))
    pygame.display.update()
#Funcion para dibujar la tabla de puntuaciones
def draw_LeaderBoard():
    WIN.fill(BLACK)
    draw_button(WIN, button_return, 'Volver', text5_x, text5_y)
    pygame.display.update()
#Funcion para dibujar la pantalla de seccion de 1 jugador
def draw_win_1player():
    WIN.fill(RED)
    draw_button(WIN, button_return, 'Volver', text5_x, text5_y)
    draw_button(WIN, button_play, 'Jugar', text6_x, text6_y)
    pygame.display.update()
#Funcion para dibujar la pantalla de seccion de 2 jugadores
def draw_win_2players():
    WIN.fill(BLACK)
    draw_button(WIN, button_return, 'Volver', text5_x, text5_y)
    draw_button(WIN, button_play, 'Jugar', text6_x, text6_y)
    pygame.display.update()
# dibujar niveles
def draw_level1(player_one, player_one_bullets, zombies_list, zombie_default_health_list):
    WIN.fill(WHITE)
    #dibujar el background del nivel
    WIN.blit(background_lvl1, (0, 0))
    #bibujar al jugador
    WIN.blit(img_player1, (player_one.x, player_one.y))
    # dibujar las balas
    for bullet in player_one_bullets:
        WIN.blit(img_bullets, (bullet.x, bullet.y))
    # dibujar los zombies
    draw_zombies(zombies_list, zombie_default_health_list)
    #dibujar las barras de vida del personaje
    pygame.draw.rect(WIN, RED, [player_one.x, player_one.y, 100, 15], 0)
    pygame.draw.rect(WIN, GREEN_DARK, [player_one.x, player_one.y, player1_health, 15], 0)
    # pass_level(zombies_list)
    pygame.display.update()
# pygame.time.delay(20)

player1_direction_x = 1
player1_direction_y = 1

#Funcion para el movimiento de los jugadores
def player_movement(key_pressed, player, velocity):
    global player1_direction_x, player1_direction_y
    if pygame.KEYDOWN and key_pressed[pygame.K_a]:
        player.x -= velocity
        player1_direction_x = -1
        player1_direction_y = 0
    if pygame.KEYDOWN and key_pressed[pygame.K_d]:
        player.x += velocity
        player1_direction_x = 1
        player1_direction_y = 0
    if pygame.KEYDOWN and key_pressed[pygame.K_w]:
        player.y -= velocity
        player1_direction_x = 0
        player1_direction_y = -1
    if pygame.KEYDOWN and key_pressed[pygame.K_s]:
        player.y += velocity
        player1_direction_x = 0
        player1_direction_y = 1
    # if pygame.KEYUP:
    #     player1_direction = 1
    return player1_direction_x, player1_direction_y

#funcion para las balas
def handle_bullets(list_bullets_p1, bullets_velocity_list, zombie_list, zombies_healt_list):
    

    if len(list_bullets_p1) != 0:
        # print(bullets_velocity_list)
        # print(list_bullets_p1)
        for j in range(len(list_bullets_p1)):
            
            for i in range(len(zombie_list)):
                list_bullets_p1[j].x += bullets_velocity_list[j][0] * bullet_velocity
                list_bullets_p1[j].y += bullets_velocity_list[j][1] * bullet_velocity
            
                # if (list_bullets_p1[j].x>=600 or list_bullets_p1[j].x<=0 or list_bullets_p1[j].y>=600 or list_bullets_p1[j].y<=0):
                if zombie_list[i].colliderect(list_bullets_p1[j]) and len(list_bullets_p1)<= max_bullets_player1:
                    # list_bullets_p1.remove(list_bullets_p1[j]) # quitar las balas al impactar con un zombie
                    # bullets_velocity_list.remove(bullets_velocity_list[j])
                    zombies_healt_list[i].w -= 10 #
                    
                if zombies_healt_list[i].w == 0: #muerte del zombie
                    
                    zombie_list[i].x = 8000
                    zombies_healt_list[i].x = 8000

    # for i in range(len(zombie_list)):
    #     if len(list_bullets_p1) != 0:
    #         if zombies_healt_list[i].colliderect(list_bullets_p1[0]):
    #             print('colision')
    #             zombies_healt_list[i].w -= 10 # bajar vida al zombie
    #             zombie_list.remove(list_bullets_p1[0])

        
                
    return zombies_healt_list

#Funcion para dibujar los zombies
def draw_zombies(list_zombies, zombie_health_list):
    for i in range(len(list_zombies)):
        WIN.blit(zombie_default_img, (list_zombies[i].x, list_zombies[i].y)) 
        pygame.draw.rect(WIN, RED, [list_zombies[i].x, list_zombies[i].y, 100, 15], 0)
        pygame.draw.rect(WIN, GREEN_LIFE, [list_zombies[i].x, list_zombies[i].y, zombie_health_list[i].w, 15], 0)

#Funcion para crear los zombies
def create_zombies(zombies_cuantitie):
    list_zombies = []
    zombies_healt_list = []
    for i in range(zombies_cuantitie):
        randint = random.randint(0,2)
        if randint == 0:
            zombie_spawn_x, zombie_spawn_y = WIDTH - 100, random.randint(0, HEIGHT)
        elif randint == 1:
            zombie_spawn_x, zombie_spawn_y = 0, random.randint(0, HEIGHT)
        elif randint == 2:
            zombie_spawn_x, zombie_spawn_y = random.randint(0, WIDTH), HEIGHT - 100

        zombie = pygame.Rect(zombie_spawn_x, zombie_spawn_y,zombie_width,zombie_height)
        
        list_zombies.append(zombie)
        #Barras de vida
        zombie_default_health_green=pygame.draw.rect(WIN, GREEN_LIFE, [zombie.x, zombie.y, 2*zombie_default_health, 15], 0)
        zombies_healt_list.append(zombie_default_health_green)
        # print(zombie_default_health_green)

    return list_zombies, zombies_healt_list

#Funcion para el movimiento de los zombies
def follow_player(zombie_list, player1):
    for zombie in zombie_list:
        dx, dy = player1.x - zombie.x, player1.y - zombie.y
        distancia = math.sqrt(dx * dx + dy * dy)
        dx, dy = dx / distancia, dy /  distancia
        zombie.x += dx * zombie_velocity
        zombie.y += dy * zombie_velocity

contador = 1000
def health_configurate(player1,zombie_list):
    global player1_health
    global contador
    hits = True
    for zombie in zombie_list:
        
        if zombie.colliderect(player1) and hits:
            start = time.time()
            hits = False
            player1_health -= 10

def pass_level(list_zombies):
    if len(list_zombies) == 0:
        WIN.blit(background_lvl1, (0,0))

def main():
    
    running = True
    channel.play(menu_music, -1)

    def menu():
        run = True
        select_button = ''
        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                    if button_1player.collidepoint(pygame.mouse.get_pos()):
                        # x, y = pygame.mouse.get_pos()
                        select_button = 'onePlayerSelected'
                        sound_select_button.play()
                        run = False
                        print('Presionaste el boton de un jugador')
                    if button_2players.collidepoint(pygame.mouse.get_pos()):
                        select_button = 'twoPlayerSelected'
                        sound_select_button.play()
                        run = False
                        print('Presionaste el boton de 2 jugadores')
                    if button_LeaderBoard.collidepoint(pygame.mouse.get_pos()):
                        select_button = 'leaderBoard'
                        sound_select_button.play()
                        run = False
                        print('Presionaste el boton ver la tabla de puntajes')
                    if button_quit.collidepoint(pygame.mouse.get_pos()):
                        sound_select_button.play()
                        pygame.quit()
            draw_menu()
        return select_button

    def select_onePlayer():
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_return.collidepoint(pygame.mouse.get_pos()):
                        sound_select_button.play()
                        select_button = menu()
                        run = False
                    if button_play.collidepoint(pygame.mouse.get_pos()):
                        sound_select_button.play()
                        select_button = play_lvl1()
                        run = False
            draw_win_1player()
        return select_button

    def select_twoPlayer():
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_return.collidepoint(pygame.mouse.get_pos()):
                        sound_select_button.play()
                        select_button = menu()
                        run = False
                    if button_play.collidepoint(pygame.mouse.get_pos()):
                        sound_select_button.play()
                        select_button = play_lvl1()
                        run = False
            draw_win_2players()
        return select_button

    def select_leaderBoard():
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_return.collidepoint(pygame.mouse.get_pos()):
                        sound_select_button.play()
                        select_button = menu()
                        run = False
            draw_LeaderBoard()
        return select_button

    def play_lvl1():
        start = time.time()
        player_one = pygame.Rect(250, 50, 120, 120)
        player_one_bullets = []
        bullets_velocity_list = []
    
        zombies_cuantitie = 15
        zombies_list, zombies_healt_list = create_zombies(zombies_cuantitie)
    
        # zombies_list,zombies_healt_list  = [], []

        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            
            key_pressed = pygame.key.get_pressed()
            player1_direction_x, player1_direction_y = player_movement(key_pressed, player_one, player1_velocity)
            
            # if player1_health == 0:
            #     run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t and len(player_one_bullets)<= max_bullets_player1:
                        if player1_direction_x == -1 and player1_direction_y == 0:
                        # bullets_sound.play()
                            bullet = pygame.Rect(
                                player_one.x + 60, player_one.y + 50, bullet_width, bullet_height)
                            player_one_bullets.append(bullet)
                            bullets_velocity_list.append([player1_direction_x, player1_direction_y])
                        if player1_direction_x == 1 and player1_direction_y == 0 :
                            bullet = pygame.Rect(
                                player_one.x + 60, player_one.y + 50, bullet_width, bullet_height)
                            player_one_bullets.append(bullet)
                            bullets_velocity_list.append([player1_direction_x, player1_direction_y])
                        if player1_direction_x == 0 and player1_direction_y == -1 :
                            bullet = pygame.Rect(
                                player_one.x + 60, player_one.y + 50, bullet_width, bullet_height)
                            player_one_bullets.append(bullet)
                            bullets_velocity_list.append([player1_direction_x, player1_direction_y])
                        if player1_direction_x == 0 and player1_direction_y == 1:
                            bullet = pygame.Rect(
                                player_one.x + 60, player_one.y + 50, bullet_width, bullet_height)
                            player_one_bullets.append(bullet)
                            bullets_velocity_list.append([player1_direction_x, player1_direction_y])
                        
            
            
            health_configurate(player_one, zombies_list)
            zombies_healt_list = handle_bullets(player_one_bullets, bullets_velocity_list, zombies_list, zombies_healt_list)
            follow_player(zombies_list, player_one)
            draw_level1(player_one, player_one_bullets, zombies_list, zombies_healt_list)
        
        return select_button

    select_button = menu()
    while True:
        if select_button == 'onePlayerSelected':
            select_button = select_onePlayer()
        if select_button == 'twoPlayerSelected':
            select_button = select_twoPlayer()
        if select_button == 'leaderBoard':
            select_button = select_leaderBoard()
        

    pygame.quit()

# __name__ es el nombre del archivo
# Solo ejecuta el programa el archivo se llama main
if __name__ == "__main__":
    main()
