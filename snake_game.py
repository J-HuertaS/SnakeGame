#Conjunto de modulos importados
import pygame, sys
from pygame.locals import *
from pathlib import Path
from pygame.math import Vector2
from random import randint,choices

#Inicio pygame and complements
pygame.mixer.pre_init(44100,-16,2,512)
pygame.font.init()
pygame.init()

# Base directory of this script (portable: Linux/Windows)
BASE_DIR = Path(__file__).resolve().parent

def resource_path(path: str) -> str:
    normalized_path = str(path).replace('\\', '/')
    legacy_root = 'C:/Python/Snake/'

    if normalized_path.startswith(legacy_root):
        normalized_path = normalized_path[len(legacy_root):]

    if Path(normalized_path).is_absolute():
        return normalized_path

    return str(BASE_DIR / normalized_path)


_pygame_image_load = pygame.image.load
_pygame_sound_load = pygame.mixer.Sound
_pygame_music_load = pygame.mixer.music.load
_pygame_font_load = pygame.font.Font


def _image_load(path, *args, **kwargs):
    return _pygame_image_load(resource_path(path), *args, **kwargs)


def _sound_load(path, *args, **kwargs):
    return _pygame_sound_load(resource_path(path), *args, **kwargs)


def _music_load(path, *args, **kwargs):
    return _pygame_music_load(resource_path(path), *args, **kwargs)


def _font_load(path, *args, **kwargs):
    if path is None:
        return _pygame_font_load(path, *args, **kwargs)
    return _pygame_font_load(resource_path(path), *args, **kwargs)


pygame.image.load = _image_load
pygame.mixer.Sound = _sound_load
pygame.mixer.music.load = _music_load
pygame.font.Font = _font_load

#Modo de juego
multiplayer, obstacles = False, True

#Color serpiente
snake_color = 'green'

#Mapa
mapa, map = (14,16,18), 'dark'

#Otras variables
num_fruits = 0
num_fruits2 = 0
des_obs = 0
des_obs2 = 0
cell_size, cell_number = 32, mapa[2] #Tamaños de mapa: 14 16 18

#Fuentes a utilizar
numbers = pygame.font.Font(resource_path('Graphics/interface/Lolicandy.ttf'),60)

#Colores
black = (0,0,0)
white = (255,255,255)
gray_w = (187,190,191)
gray_b = (120,120,120)
gray = (137,137,137)
pink = (202,129,213)
white_pink = (213,145,224)

#Evento manual para actualizar pantalla
UPDATE_SCREEN = pygame.USEREVENT
pygame.time.set_timer(UPDATE_SCREEN,150)

#functions to personalize the snake
def green_snake(self):
    #Head
    self.head_up = pygame.image.load('Graphics/green/head_up.png').convert_alpha()
    self.head_down = pygame.image.load('Graphics/green/head_down.png').convert_alpha()
    self.head_right = pygame.image.load('Graphics/green/head_right.png').convert_alpha()
    self.head_left = pygame.image.load('Graphics/green/head_left.png').convert_alpha()
    #Body
    self.body_vertical = pygame.image.load('Graphics/green/body_vertical.png').convert_alpha()
    self.body_horizontal = pygame.image.load('Graphics/green/body_horizontal.png').convert_alpha()
    #Tail
    self.tail_up = pygame.image.load('Graphics/green/tail_up.png').convert_alpha()
    self.tail_down = pygame.image.load('Graphics/green/tail_down.png').convert_alpha()
    self.tail_right = pygame.image.load('Graphics/green/tail_right.png').convert_alpha()
    self.tail_left = pygame.image.load('Graphics/green/tail_left.png').convert_alpha()
    #Turn moment
    self.body_tr = pygame.image.load('Graphics/green/body_tr.png').convert_alpha()
    self.body_tl = pygame.image.load('Graphics/green/body_tl.png').convert_alpha()
    self.body_br = pygame.image.load('Graphics/green/body_br.png').convert_alpha()
    self.body_bl = pygame.image.load('Graphics/green/body_bl.png').convert_alpha()

def blue_snake(self):
    #Head
    self.head_up = pygame.image.load('Graphics/blue/head_up.png').convert_alpha()
    self.head_down = pygame.image.load('Graphics/blue/head_down.png').convert_alpha()
    self.head_right = pygame.image.load('Graphics/blue/head_right.png').convert_alpha()
    self.head_left = pygame.image.load('Graphics/blue/head_left.png').convert_alpha()
    #Body
    self.body_vertical = pygame.image.load('Graphics/blue/body_vertical.png').convert_alpha()
    self.body_horizontal = pygame.image.load('Graphics/blue/body_horizontal.png').convert_alpha()
    #Tail
    self.tail_up = pygame.image.load('Graphics/blue/tail_up.png').convert_alpha()
    self.tail_down = pygame.image.load('Graphics/blue/tail_down.png').convert_alpha()
    self.tail_right = pygame.image.load('Graphics/blue/tail_right.png').convert_alpha()
    self.tail_left = pygame.image.load('Graphics/blue/tail_left.png').convert_alpha()
    #Turn moment
    self.body_tr = pygame.image.load('Graphics/blue/body_tr.png').convert_alpha()
    self.body_tl = pygame.image.load('Graphics/blue/body_tl.png').convert_alpha()
    self.body_br = pygame.image.load('Graphics/blue/body_br.png').convert_alpha()
    self.body_bl = pygame.image.load('Graphics/blue/body_bl.png').convert_alpha()

def yellow_snake(self):
    #Head
    self.head_up = pygame.image.load('Graphics/yellow/head_up.png').convert_alpha()
    self.head_down = pygame.image.load('Graphics/yellow/head_down.png').convert_alpha()
    self.head_right = pygame.image.load('Graphics/yellow/head_right.png').convert_alpha()
    self.head_left = pygame.image.load('Graphics/yellow/head_left.png').convert_alpha()
    #Body
    self.body_vertical = pygame.image.load('Graphics/yellow/body_vertical.png').convert_alpha()
    self.body_horizontal = pygame.image.load('Graphics/yellow/body_horizontal.png').convert_alpha()
    #Tail
    self.tail_up = pygame.image.load('Graphics/yellow/tail_up.png').convert_alpha()
    self.tail_down = pygame.image.load('Graphics/yellow/tail_down.png').convert_alpha()
    self.tail_right = pygame.image.load('Graphics/yellow/tail_right.png').convert_alpha()
    self.tail_left = pygame.image.load('Graphics/yellow/tail_left.png').convert_alpha()
    #Turn moment
    self.body_tr = pygame.image.load('Graphics/yellow/body_tr.png').convert_alpha()
    self.body_tl = pygame.image.load('Graphics/yellow/body_tl.png').convert_alpha()
    self.body_br = pygame.image.load('Graphics/yellow/body_br.png').convert_alpha()
    self.body_bl = pygame.image.load('Graphics/yellow/body_bl.png').convert_alpha()

def purple_snake(self):
    self.head_up = pygame.image.load('Graphics/purple/head_up.png').convert_alpha()
    self.head_down = pygame.image.load('Graphics/purple/head_down.png').convert_alpha()
    self.head_right = pygame.image.load('Graphics/purple/head_right.png').convert_alpha()
    self.head_left = pygame.image.load('Graphics/purple/head_left.png').convert_alpha()
    #Body
    self.body_vertical = pygame.image.load('Graphics/purple/body_vertical.png').convert_alpha()
    self.body_horizontal = pygame.image.load('Graphics/purple/body_horizontal.png').convert_alpha()
    #Tail
    self.tail_up = pygame.image.load('Graphics/purple/tail_up.png').convert_alpha()
    self.tail_down = pygame.image.load('Graphics/purple/tail_down.png').convert_alpha()
    self.tail_right = pygame.image.load('Graphics/purple/tail_right.png').convert_alpha()
    self.tail_left = pygame.image.load('Graphics/purple/tail_left.png').convert_alpha()
    #Turn moment
    self.body_tr = pygame.image.load('Graphics/purple/body_tr.png').convert_alpha()
    self.body_tl = pygame.image.load('Graphics/purple/body_tl.png').convert_alpha()
    self.body_br = pygame.image.load('Graphics/purple/body_br.png').convert_alpha()
    self.body_bl = pygame.image.load('Graphics/purple/body_bl.png').convert_alpha()

#Clase para la serpiente
class SNAKE:

    def __init__(self,vector,snake_color):
        self.body = vector
        self.direction = Vector2(0,-1)
        self.new_block = False

        #Snake sprites
        if snake_color == 'green': green_snake(self)
        elif snake_color == 'blue': blue_snake(self)
        elif snake_color == 'yellow': yellow_snake(self)
        else: purple_snake(self)

        self.crunch = pygame.mixer.Sound('Graphics/Sound_crunch.wav')
        self.die = pygame.mixer.Sound('Graphics/fail.wav')

    #update graphics to select an image
    def update_head_graphics(self):
        head_direction = self.body[1] - self.body[0]
        if head_direction == Vector2(1,0): self.head = self.head_left
        elif head_direction == Vector2(-1,0): self.head = self.head_right
        elif head_direction == Vector2(0,1): self.head = self.head_up
        elif head_direction == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_direction = self.body[-2] - self.body[-1]
        if tail_direction == Vector2(-1,0): self.tail = self.tail_left
        elif tail_direction == Vector2(1,0): self.tail = self.tail_right
        elif tail_direction == Vector2(0,-1): self.tail = self.tail_up
        elif tail_direction == Vector2(0,1): self.tail = self.tail_down

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            snake_part = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0: screen_on_game.blit(self.head,snake_part)
            elif index == len(self.body)-1: screen_on_game.blit(self.tail,snake_part)
            else:
                prev_block = self.body[index+1] - block
                next_block = self.body[index-1] - block

                if prev_block.x == next_block.x:
                    screen_on_game.blit(self.body_vertical,snake_part)
                elif prev_block.y == next_block.y:
                    screen_on_game.blit(self.body_horizontal,snake_part)
                else:
                    if prev_block.x == -1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == -1:
                        screen_on_game.blit(self.body_tl,snake_part)
                    if prev_block.x == 1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == 1:
                        screen_on_game.blit(self.body_br,snake_part)
                    if prev_block.x == 1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == 1:
                        screen_on_game.blit(self.body_tr,snake_part)
                    if prev_block.x == -1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == -1:
                        screen_on_game.blit(self.body_bl,snake_part)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,(body_copy[0] + self.direction))
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:]
            body_copy.insert(0,(body_copy[0] + self.direction))
            body_copy.pop()
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def fruit_sound(self):
        self.crunch.play()

    def die_sound(self):
        self.die.play()


class FRUIT:
    def __init__(self):
        self.randomize()

    def randomize(self):
        self.x = randint(0,cell_number-1)
        self.y = randint(0,cell_number-1)
        self.pos = Vector2(self.x,self.y)
        fruits = ['default','java','R']
        self.state = choices(fruits,weights = (70,25,5),k = 1)

    def draw_fruit(self):
        x_pos = int(self.pos.x * cell_size)
        y_pos = int(self.pos.y * cell_size)
        fruit_sqr = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

        if self.state == ['java']:
            fruit = pygame.image.load('Graphics/assets/java.png').convert_alpha()
        elif self.state == ['default']:
            fruit = pygame.image.load('Graphics/assets/apple.png').convert_alpha()
        else:
            fruit = pygame.image.load('Graphics/assets/R.png').convert_alpha()

        screen_on_game.blit(fruit,fruit_sqr)


class OBSTACLE:
    def __init__(self):
        self.randomize()

    def draw_obstacle(self):
        x_pos = int(self.pos.x * cell_size)
        y_pos = int(self.pos.y * cell_size)
        obstacle_sqr = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

        obstacle_img = pygame.image.load(
            'Graphics/assets/obstacle.png'
        ).convert_alpha()

        screen_on_game.blit(obstacle_img,obstacle_sqr)

    def randomize(self):
        self.x = randint(0,cell_number-1)
        self.y = randint(0,cell_number-1)
        self.pos = Vector2(self.x,self.y)


#Clase del juego principal
class MAIN:
    def __init__(self):
        self.fruit = FRUIT()
        self.obstacle = []
        self.obs_pos = []

        self.snake = [
            SNAKE(
                [
                    Vector2(cell_number-(cell_number//2),cell_number//2-1),
                    Vector2(cell_number-(cell_number//2),cell_number//2),
                    Vector2(cell_number-(cell_number//2),cell_number//2+1)
                ],
                snake_color
            )
        ]

        if multiplayer == True:
            self.snake = [
                SNAKE(
                    [
                        Vector2(cell_number-(cell_number//2),cell_number//2-1),
                        Vector2(cell_number-(cell_number//2),cell_number//2),
                        Vector2(cell_number-(cell_number//2),cell_number//2+1)
                    ],
                    'yellow'
                ),
                SNAKE(
                    [
                        Vector2(cell_number//4,cell_number//2-1),
                        Vector2(cell_number//4,cell_number//2),
                        Vector2(cell_number//4,cell_number//2+1)
                    ],
                    'blue'
                )
            ]

        self.controles = [
            Vector2(0,-1),Vector2(0,1),Vector2(1,0),Vector2(-1,0),
            Vector2(0,-1),Vector2(0,1),Vector2(1,0),Vector2(-1,0)
        ]

        self.inv_controls = [False,0]
        self.end = False
        self.delete_obs = pygame.mixer.Sound('Graphics/pop.wav')


    def sound_delete(self):
        self.delete_obs.play()


    def update(self):
        for snakes in self.snake:
            snakes.move_snake()

        self.check_collision()

        if not self.end:
            self.check_fail()

        self.destroy_obs()
        self.obstacle_pos()


    def controles_state(self,snake,invertir):
        self.controles = [
            [Vector2(0,-1),Vector2(0,1),Vector2(1,0),Vector2(-1,0)],
            [Vector2(0,-1),Vector2(0,1),Vector2(1,0),Vector2(-1,0)]
        ]

        if invertir:
            for i in range(4):
                if self.controles[snake][i].x != 0:
                    self.controles[snake][i] = Vector2(
                        self.controles[snake][i].x*-1,
                        self.controles[snake][i].y
                    )
                else:
                    self.controles[snake][i] = Vector2(
                        self.controles[snake][i].x,
                        self.controles[snake][i].y*-1
                    )


    def reducir_snake(self,player):
        snake_aux = []

        for i in range(2):
            snake_aux.append(self.snake[player].body[i])

        self.snake[player].body = snake_aux

    def draw_elements(self):
        self.draw_map()
        self.fruit.draw_fruit()
        for i in range(len(self.obstacle)):
            self.obstacle[i].draw_obstacle()
        for snakes in self.snake:
            snakes.draw_snake()

    def draw_map(self):
        if map == 'default': main_color, sec_color = white, gray_w
        elif map == 'dark': main_color, sec_color = gray_b, gray
        elif map == 'pink': main_color, sec_color = pink, white_pink
        screen_on_game.fill(sec_color)

        for fila in range(cell_number):
            if fila % 2 == 0:
                for columna in range(cell_number):
                    if columna % 2 == 0:
                        grass_rect = pygame.Rect(columna * cell_size, fila * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen_on_game, main_color, grass_rect)
            else:
                for columna in range(cell_number):
                    if columna % 2 != 0:
                        grass_rect = pygame.Rect(columna * cell_size, fila * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen_on_game, main_color, grass_rect)

    def check_collision(self):
        invertir, reducir = False, False
        if self.fruit.state == ['java']: invertir = True
        elif self.fruit.state == ['R']: reducir = True
        else: invertir, reducir = False, False

        for i in range(len(self.snake)):
            if self.fruit.pos == self.snake[i].body[0]:
                self.snake[i].fruit_sound()

                for j in range(len(self.snake)):
                    while True:
                        self.fruit.randomize()
                        if (self.fruit.pos in self.obs_pos or self.fruit.pos in self.snake[j].body):
                            self.fruit.randomize()
                        else:
                            break

                if i == 0:
                    if len(self.snake) == 2:
                        self.snake[1].add_block()
                        globals()['num_fruits'] += 1
                        self.controles_state(1, invertir)
                        self.inv_controls = [invertir,1]
                        if reducir: self.reducir_snake(1)
                    else:
                        self.snake[0].add_block()
                        globals()['num_fruits'] += 1
                        self.controles_state(0, invertir)
                        self.inv_controls = [invertir,0]
                        if reducir: self.reducir_snake(0)

                else:
                    self.snake[0].add_block()
                    globals()['num_fruits2'] += 1
                    self.controles_state(0, invertir)
                    self.inv_controls = [invertir,0]
                    if reducir: self.reducir_snake(0)

        # Removed - obstacle generation is now handled in snake_game() to prevent duplicate calls

    def add_obs(self):
        self.obstacle.append(OBSTACLE())

        for i in range(len(self.snake)):
            while (self.obstacle[-1].pos in self.snake[i].body or self.obstacle[-1].pos == self.fruit.pos):
                self.obstacle[-1].randomize()

            while (self.obstacle[-1].pos in self.obs_pos[:-1]):
                self.obstacle[-1].randomize()

    def destroy_obs(self):
        for j in range(len(self.snake)):
            for i in range(len(self.obstacle)):
                if (self.snake[j].body[0].x == self.obstacle[i].pos.x and
                    (self.snake[j].body[0].y == self.obstacle[i].pos.y+1 or
                     self.snake[j].body[0].y == self.obstacle[i].pos.y-1)):

                    if (self.snake[j].direction == Vector2(1,0) or
                        self.snake[j].direction == Vector2(-1,0)):

                        self.sound_delete()
                        del self.obstacle[i]

                        if j == 0:
                            globals()['des_obs'] += 1
                        else:
                            globals()['des_obs2'] += 1
                        break

                else:
                    if (self.snake[j].body[0].y == self.obstacle[i].pos.y and
                        (self.snake[j].body[0].x == self.obstacle[i].pos.x+1 or
                         self.snake[j].body[0].x == self.obstacle[i].pos.x-1)):

                        if (self.snake[j].direction == Vector2(0,1) or
                            self.snake[j].direction == Vector2(0,-1)):

                            self.sound_delete()
                            del self.obstacle[i]

                            if j == 0:
                                globals()['des_obs'] += 1
                            else:
                                globals()['des_obs2'] += 1
                            break

    def check_fail(self):
        multi_state = len(self.snake) == 2

        for i in range(len(self.snake)):
            if (not 0 <= self.snake[i].body[0].x < cell_number) or (not 0 <= self.snake[i].body[0].y < cell_number):
                self.end = True
                self.snake[i].die_sound()

            if (self.snake[i].body[0] in self.snake[i].body[1:]):
                self.end = True
                self.snake[i].die_sound()

            if multi_state:
                if self.snake[i].body[0] in self.snake[i-1].body:
                    self.end = True
                    self.snake[i].die_sound()

            for j in range(len(self.obstacle)):
                if (self.snake[i].body[0] == self.obstacle[j].pos):
                    self.end = True
                    self.snake[i].die_sound()

    def obstacle_pos(self):
        list_aux = []
        for i in self.obstacle:
            list_aux.append(i.pos)

        self.obs_pos = list_aux

    #definir funciones - escribir, menu y juego
#Escribir en pantalla
def draw_text(text,font,color,surface,x,y):
    textobj = font.render(text,1,color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj,textrect)


def main_menu():
    pygame.display.set_caption('Main menu :D')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.load('Graphics/menu_music.wav')
    pygame.mixer.music.play(-1)

    screen_on_menu = pygame.image.load('Graphics/interface/menu.png').convert_alpha()

    globals()['num_fruits'] = 0
    globals()['num_fruits2'] = 0
    globals()['des_obs'] = 0
    globals()['des_obs2'] = 0

    home = pygame.Rect(44,602,216,67)

    button_1 = pygame.Rect(374.5,299,531,80)
    button_2 = pygame.Rect(391.5,425,497,80)
    button_3 = pygame.Rect(470,542,335,100)

    menu_button = pygame.image.load('Graphics/interface/back.png').convert_alpha()

    while True:

        click = False

        screen.blit(screen_on_menu,(0,0))
        screen.blit(menu_button,(44,602))

        mx,my = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if button_1.collidepoint((mx,my)) and click:
            globals()['multiplayer'] = False
            color_selection()

        if button_2.collidepoint((mx,my)) and click:
            globals()['multiplayer'] = True
            map_selection()

        if button_3.collidepoint((mx,my)) and click:
            menu_controls()

        if home.collidepoint((mx,my)) and click:
            pygame.quit()
            sys.exit()

        pygame.display.update()


def snake_game():

    main_game = MAIN()
    
    # Initialize controles state to prevent IndexError
    if multiplayer:
        main_game.controles_state(0, False)
        main_game.controles_state(1, False)
    else:
        main_game.controles_state(0, False)

    pygame.mixer.music.set_volume(0.06)

    c = [1,1]
    
    # Flag to prevent obstacles from being created multiple times per frame
    last_fruit_total = 0

    if multiplayer:
        main = pygame.image.load('Graphics/interface/main2F.png').convert_alpha()
    else:
        main = pygame.image.load('Graphics/interface/main.png').convert_alpha()

    if obstacles and multiplayer:
        obstacles_img = pygame.image.load('Graphics/interface/danger_mul.png').convert_alpha()
    elif obstacles:
        obstacles_img = pygame.image.load('Graphics/interface/danger.png').convert_alpha()

    if cell_number == mapa[2]:
        final_img = pygame.image.load('Graphics/interface/map0.png').convert_alpha()
    elif cell_number == mapa[1]:
        final_img = pygame.image.load('Graphics/interface/map1.png').convert_alpha()
    else:
        final_img = pygame.image.load('Graphics/interface/map2.png').convert_alpha()
    
    # Scale final image to match the game board size
    game_board_size = cell_size * cell_number
    final_img = pygame.transform.scale(final_img, (game_board_size, game_board_size))

    menu_button = pygame.image.load('Graphics/interface/menu_button_ig.png').convert_alpha()
    menu_button_rect = pygame.Rect(750,447,100,100)

    timer = True

    while True:

        click = False

        mx,my = pygame.mouse.get_pos()

        if main_game.inv_controls[0] == True:

            if main_game.inv_controls[1] == 0:
                c[0] = -1
            else:
                c[1] = -1

        else:

            if main_game.inv_controls[1] == 0:
                c[0] = 1
            else:
                c[1] = 1

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == UPDATE_SCREEN:
                main_game.update()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    if main_game.end:
                        main_menu()

                if event.key == pygame.K_UP:
                    if main_game.snake[0].direction.y != 1*c[0]:
                        main_game.snake[0].direction = main_game.controles[0][0]

                if event.key == pygame.K_DOWN:
                    if main_game.snake[0].direction.y != -1*c[0]:
                        main_game.snake[0].direction = main_game.controles[0][1]

                if event.key == pygame.K_RIGHT:
                    if main_game.snake[0].direction.x != -1*c[0]:
                        main_game.snake[0].direction = main_game.controles[0][2]

                if event.key == pygame.K_LEFT:
                    if main_game.snake[0].direction.x != 1*c[0]:
                        main_game.snake[0].direction = main_game.controles[0][3]

                if len(main_game.snake) == 2:

                    if event.key == pygame.K_w:
                        if main_game.snake[1].direction.y != 1*c[1]:
                            main_game.snake[1].direction = main_game.controles[1][0]

                    if event.key == pygame.K_s:
                        if main_game.snake[1].direction.y != -1*c[1]:
                            main_game.snake[1].direction = main_game.controles[1][1]

                    if event.key == pygame.K_d:
                        if main_game.snake[1].direction.x != -1*c[1]:
                            main_game.snake[1].direction = main_game.controles[1][2]

                    if event.key == pygame.K_a:
                        if main_game.snake[1].direction.x != 1*c[1]:
                            main_game.snake[1].direction = main_game.controles[1][3]

        screen.blit(main,(0,0))

        if main_game.end:

            clock.tick(0)

            pygame.mixer.music.unload()

            while timer:
                pygame.time.wait(2000)
                timer = False

            screen_on_game.blit(final_img,(0,0))

            screen_on_game.blit(menu_button,
            (((cell_size*cell_number)/2)-50,((cell_size*cell_number)-((cell_size*cell_number)/3))+10))

            if menu_button_rect.collidepoint((mx,my)) and click:
                main_menu()

        else:

            main_game.draw_elements()
            clock.tick(60)

        # Check if obstacles should be added (only once per 3 fruits eaten)
        current_fruit_total = globals()['num_fruits'] + globals()['num_fruits2']
        if current_fruit_total % 3 == 0 and current_fruit_total > last_fruit_total and obstacles:
            main_game.add_obs()
            last_fruit_total = current_fruit_total
        
        if multiplayer:

            draw_text(str(num_fruits),numbers,black,screen,141,170)
            draw_text(str(num_fruits2),numbers,black,screen,141,352)

            if obstacles:
                draw_text(str(des_obs),numbers,black,screen,342,174)
                draw_text(str(des_obs2),numbers,black,screen,342,356)
                screen.blit(obstacles_img,(255,184))
                screen.blit(obstacles_img,(255,366))

        else:

            draw_text(str(num_fruits),numbers,black,screen,215,215)

            if obstacles:
                draw_text(str(des_obs),numbers,black,screen,215,345)
                screen.blit(obstacles_img,(95,345))

        if cell_number == mapa[0]:
            screen.blit(screen_on_game,(1025-(cell_size*cell_number),(720-(cell_size*cell_number))/2))

        elif cell_number == mapa[1]:
            screen.blit(screen_on_game,(1055-(cell_size*cell_number),(720-(cell_size*cell_number))/2))

        else:
            screen.blit(screen_on_game,(1083-(cell_size*cell_number),(720-(cell_size*cell_number))/2))

        pygame.display.update()

def menu_controls():

    screen_controls = pygame.image.load('Graphics/interface/controles.png').convert_alpha()
    menu_button = pygame.image.load('Graphics/interface/back.png').convert_alpha()
    home = pygame.Rect(10,10,250,90)

    while True:

        click = False
        mx,my = pygame.mouse.get_pos()

        screen.blit(screen_controls,(0,0))
        screen.blit(menu_button,(10,10))

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if home.collidepoint((mx,my)) and click:
            main_menu()

        pygame.display.update()

def color_selection():

    screen_color = pygame.image.load('Graphics/interface/color.jpeg').convert_alpha()

    home = pygame.Rect(44,602,210,67)

    button_1 = pygame.Rect(400,130,230,220)
    button_2 = pygame.Rect(680,130,230,220)
    button_3 = pygame.Rect(680,410,230,220)
    button_4 = pygame.Rect(400,410,230,220)

    aux = False

    while True:

        click = False

        mx,my = pygame.mouse.get_pos()

        screen.blit(screen_color,(0,0))

        mx,my = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if home.collidepoint((mx,my)) and click:
            main_menu()

        if button_1.collidepoint((mx,my)) and click:
            globals()['snake_color'] = 'green'
            aux = True

        if button_2.collidepoint((mx,my)) and click:
            globals()['snake_color'] = 'yellow'
            aux = True

        if button_3.collidepoint((mx,my)) and click:
            globals()['snake_color'] = 'purple'
            aux = True

        if button_4.collidepoint((mx,my)) and click:
            globals()['snake_color'] = 'blue'
            aux = True

        if aux:
            map_selection()

        pygame.display.update()

def map_selection():

    screen_map = pygame.image.load('Graphics/interface/map.jpeg').convert_alpha()

    home = pygame.Rect(44,602,210,67)

    button_1 = pygame.Rect(125,320,150,150)
    button_2 = pygame.Rect(405,270,255,255)
    button_3 = pygame.Rect(820,239,330,330)

    aux = False

    while True:

        click = False

        mx,my = pygame.mouse.get_pos()

        screen.blit(screen_map,(0,0))

        mx,my = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if home.collidepoint((mx,my)) and click:

            if multiplayer:
                main_menu()
            else:
                color_selection()

        if button_1.collidepoint((mx,my)) and click:
            globals()['cell_number'] = mapa[0]
            aux = True

        if button_2.collidepoint((mx,my)) and click:
            globals()['cell_number'] = mapa[1]
            aux = True

        if button_3.collidepoint((mx,my)) and click:
            globals()['cell_number'] = mapa[2]
            aux = True

        if aux:
            map_color_selection()

        pygame.display.update()

def map_color_selection():

    screen_map = pygame.image.load('Graphics/interface/map_color.jpeg').convert_alpha()

    globals()['screen_on_game'] = pygame.Surface((cell_size*cell_number,cell_size*cell_number))

    home = pygame.Rect(44,602,210,67)

    button_1 = pygame.Rect(100,225,290,290)
    button_2 = pygame.Rect(495,225,290,290)
    button_3 = pygame.Rect(900,225,290,290)

    aux = False

    while True:

        click = False

        mx,my = pygame.mouse.get_pos()

        screen.blit(screen_map,(0,0))

        mx,my = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if home.collidepoint((mx,my)) and click:
            map_selection()

        if button_1.collidepoint((mx,my)) and click:
            globals()['map'] = 'default'
            aux = True

        if button_2.collidepoint((mx,my)) and click:
            globals()['map'] = 'dark'
            aux = True

        if button_3.collidepoint((mx,my)) and click:
            globals()['map'] = 'pink'
            aux = True

        if aux:
            obstacle_selection()

        pygame.display.update()

def obstacle_selection():

    screen_obstacle = pygame.image.load('Graphics/interface/obstacles.jpeg').convert_alpha()

    home = pygame.Rect(44,602,210,67)

    button_1 = pygame.Rect(805,200,160,160)
    button_2 = pygame.Rect(805,390,160,160)

    aux = False

    while True:

        click = False

        mx,my = pygame.mouse.get_pos()

        screen.blit(screen_obstacle,(0,0))

        mx,my = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if home.collidepoint((mx,my)) and click:
            map_color_selection()

        if button_1.collidepoint((mx,my)) and click:
            globals()['obstacles'] = True
            aux = True

        if button_2.collidepoint((mx,my)) and click:
            globals()['obstacles'] = False
            aux = True

        if aux:
            snake_game()

        pygame.display.update()

screen = pygame.display.set_mode((1280,720),pygame.FULLSCREEN)

screen_on_game = pygame.Surface((cell_size*cell_number,cell_size*cell_number))

pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.load('Graphics/menu_music.wav')
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

#Menú principal para acceder a todo
main_menu()

