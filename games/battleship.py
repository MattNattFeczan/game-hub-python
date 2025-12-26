import pygame
import sys
import tkinter
import random

pygame.init()
FPS = 60
CLOCK = pygame.time.Clock()
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
FLAGS =  pygame.DOUBLEBUF | pygame.RESIZABLE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), FLAGS, vsync=1)
SCREEN.set_alpha(None)
pygame.display.set_caption("Battleship")


ships = []
ships_set = [1, 1, 1, 3, 3, 3, 5]

base_color = (100, 180, 220)
collides_with = None
play = False
state = 'None'

class tile():
    def __init__(self, x, y, tile_state, tile_map):
        self.x = (WIDTH - 640)/2 + x
        self.y = y
        self.width = 64
        self.height = 64
        self.clicked = False
        self.unit_num = 0
        self.state =  tile_state
        self.colors = {
            'normal': base_color,
            'hover': (219, 145, 140),
            'hit': (76, 219, 87),
            'miss': (255, 75, 0)
        }
        self.color = self.colors['normal']
        
        self.surface = pygame.Surface((self.width, self.height))
        self.body = pygame.Rect(self.x, self.y, self.width, self.height)
        tile_map.append(self)

    def draw(self):
        self.surface.fill(self.color) # we have problem here it makes it so that marking isn't permament
        SCREEN.blit(self.surface, self.body)
        pygame.draw.rect(SCREEN, (0, 0, 0), [self.x+3, self.y+3, self.width-6, self.height-6], width=3)
    def interact(self, g_state):
        if self.state == g_state:
            mouse = pygame.mouse.get_pos()
            if self.body.collidepoint(mouse) and not self.clicked:
                self.color = self.colors['hover'] # dosn't work as should

                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.clicked = True
                    if self.unit_num != 0:
                        self.color = self.colors['hit']
                    else:
                        self.color = self.colors['miss']
                    return True
                elif not self.clicked:
                    self.color = self.colors['normal']
        return False

class g_map():
    def __init__(self):
        self.enemy_tiles = []
        self.your_tiles = []
        self.game_state = None
        x = 0
        y = 44      
        for i in range(1, 101): #start player
            tile(x, y, 'enemy', self.enemy_tiles)
            x+=64
            if i%10 == 0:
                y+=64
                x = 0

        x = 0
        y = 748
        for i in range(1, 101):
            tile(x, y, 'player', self.your_tiles)
            x+=64
            if i%10 == 0:
                y+=64
                x = 0
    def start_game(self):
        self.game_state = 'player'
    @classmethod
    def change_state(self):
        if self.game_state == 'player':
            self.game_state = 'enemy'
        else:
            self.game_state = 'player'
    def interact(self):
        if self.game_state == None:
            return
        elif self.game_state == 'player': 
            for tile in self.your_tiles:
                if tile.interact(self.game_state):
                    print(self.game_state)
                    self.change_state()
                    print(self.game_state)
                    return
        else:
            for tile in self.enemy_tiles:
                if tile.interact(self.game_state):
                    self.change_state()
                    return
    def draw_map(self):
        for ob in self.enemy_tiles:
            ob.draw()

        for ob in self.your_tiles:
            ob.draw()


        
class ship():
    def __init__(self, number, size_unit, x, y, width, height):
        self.number = number
        self.size_unit = size_unit
        self.body = pygame.Rect(x, y, self.size_unit*width, height)
        self.befx = self.body.x
        self.befy = self.body.y
        self.color = (255, 255, 255)
        self.rotation = 0
        self.collides = False
        ships.append(self)
    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.body)
    def interact(self, event, game_map):
        global collides_with
        if play == False:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                        if self.body.collidepoint(event.pos):
                            collides_with = self.number
                if self.size_unit != 1 and event.button == 3 and self.body.collidepoint(event.pos):
                    self.rotation = not self.rotation
                    k = self.body.width
                    self.body.width = self.body.height
                    self.body.height = k

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    collides_with = None
                for s in ships:
                    if self.body.colliderect(s.body) and self != s:
                        self.body.x = self.befx
                        self.body.y = self.befy
                        return
                for index,i in enumerate(game_map.your_tiles):
                    if i.body.colliderect(self.body) and not self.rotation:
                        list_1 = [9]
                        list_2 = [8, 9]
                        num = index%10
                        if self.size_unit == 1 \
                           or (self.size_unit == 3 and num not in list_1) or (self.size_unit == 5 and num not in list_2): #to clean up
                            self.body.x = i.body.x+14
                            self.body.y = i.body.y+14
                            self.collides = True
                            return;
                    elif i.body.colliderect(self.body) and self.rotation:
                        if (self.size_unit == 3 and index < 90) or (self.size_unit == 5 and index < 80):
                            self.body.x = i.body.x+14
                            self.body.y = i.body.y+14
                            self.collides = True
                            return
                self.body.x = self.befx
                self.body.y = self.befy

            if event.type == pygame.MOUSEMOTION:
                if collides_with == self.number:
                    self.body.move_ip(event.rel)

def random_placement(ships_set, enemy_tiles):
    for i in ships_set:
        rotation = random.randint(0,1)
        while True:
            placement = random.randint(0, 99)
            if not rotation and placement%10 < 10 - i//2:
                j = i
                while j > 0:
                    if enemy_tiles[placement + j//2].unit_num != 0:
                        break
                    j-=2
                j = i
                while j > 0:
                    enemy_tiles[placement + j//2].unit_num = i
                    j-=2
            if rotation and placement < 99 - 10*(i//2):
                j = i
                while j > 0:
                    if enemy_tiles[placement + 10*(j//2)].unit_num != 0:
                        break
                    j-=2
                j = i
                while j > 0:
                    enemy_tiles[placement + 10*(j//2)].unit_num = i
                    j-=2
            break
    print()
    for index,i in enumerate(enemy_tiles):
                    print(i.unit_num, end='')
                    if index%10 == 9:
                        print()
        
class info: #correct
    def draw():
        text = pygame.font.SysFont('Arial', 40).render('Drag ships to map with left mouse button', True, "blue")
        #text_2 = pygame.font.SysFont('Arial', 50).render('Right click to rotate', True, "blue")
        surface = pygame.Rect(0, HEIGHT//6, 600, 400)
        pygame.draw.rect(SCREEN, 'orange', surface)
        SCREEN.blit(text, surface)
        #SCREEN.blit(text_2, surface)
    def hit_mess(msg): #msg has to be text
        text = pygame.font.SysFont('Arial', 100).render(msg, True, "red")
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        surface = pygame.Surface((800, 400)).get_rect(center=(WIDTH//2, HEIGHT//2))
        pygame.draw.rect(SCREEN, 'orange', surface)
        SCREEN.blit(text, text_rect)
    
                    
class start_button():
    def __init__(self):
        self.width = WIDTH//2
        self.height = int(HEIGHT*0.85)
        self.body = pygame.Surface((180, 100)).get_rect(center=(self.width, self.height))
        self.text = pygame.font.SysFont('Arial', 20).render('START GAME', True, "white")
        self.text_rect = self.text.get_rect(center=(self.width, self.height))
    def interact(self, game_map):
        global play
        if play == True:
            game_map.start_game()
            return
        mouse = pygame.mouse.get_pos()
        if self.body.collidepoint(mouse):
            all_set = 0
            for s in ships:
                if s.collides:
                    all_set+=1
            if pygame.mouse.get_pressed(num_buttons=3)[0] and all_set == 7:
                play = True
                for s in ships:
                    for i in game_map.your_tiles:
                        if i.body.colliderect(s.body):
                            i.unit_num = s.size_unit
                for index,i in enumerate(game_map.your_tiles):
                    print(i.unit_num, end='')
                    if index%10 == 9:
                        print()
                random_placement(ships_set, game_map.enemy_tiles)
                
        pygame.draw.rect(SCREEN, 'orange', self.body)
        SCREEN.blit(self.text, self.text_rect)

        
                        

x = WIDTH//4
y = HEIGHT*0.2
z = 1
for i in range(0, 7):
    ship(i, z, x, y, 36, 36)
    if i == 2 or i == 5:
        z +=2
    y += 80
    

start = start_button()
game_map = g_map()
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        SCREEN.fill(base_color)
        game_map.interact()
        game_map.draw_map()


        for s in ships:
            s.interact(event, game_map)
            s.draw()

        start_button().interact(game_map)
        info.draw()
        #info.hit_mess('HIT!!!')
        #info.hit_mess('MISS!!!')
        #info.hit_mess('YOU WIN!!!')
        #info.hit_mess('YOU LOSE!!!')

    pygame.display.flip()
    CLOCK.tick(FPS)        

