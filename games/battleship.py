import pygame
import sys
import random
import time

pygame.init()
FPS = 60
CLOCK = pygame.time.Clock()
WIDTH, HEIGHT = 1920, 1080 #base 2880, 1800
BASE_WIDTH, BASE_HEIGHT = 2800, 1800
FLAGS =  pygame.DOUBLEBUF | pygame.RESIZABLE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), FLAGS, vsync=1)
SCREEN.set_alpha(None)
pygame.display.set_caption("Battleship")

base_color = (68,112,156)
info_color = (138,161,185)
collides_with = None
play = False
state = 'None'

#UTILITY FUNCTIONS

def convert(number: int , dimension: str) -> int:
    if dimension == 'H':
        return int(number*HEIGHT/BASE_HEIGHT)
    elif dimension == 'W':
        return int(number*WIDTH/BASE_WIDTH)
    else:
        return 0

def button(msg, size, x, y, width, height, color): 
    surface = pygame.Surface((width, height))
    font = pygame.font.SysFont('Arial', convert(size, 'H')).render(msg, True, "white")
    mid_pos = font.get_rect(center=(width//2, height//2))
    surface.fill(color)
    surface.blit(font, mid_pos)
    SCREEN.blit(surface, (x,y))

    return pygame.Rect(x, y, width, height)

def restart(game_map):
        game_map.ships.clear()
        global play
        play = False
        global state
        state = 'None'
        global collides_with
        collides_with= None

def right_message():
    height = convert(300, 'H')
    width = convert(400, 'W')
    base_pos_2 = (width*0.05,height*0.1)
    x, y = base_pos_2
    font = pygame.font.SysFont('Arial', convert(40, 'H'))
    space_w = font.size(' ')[0]
    text_info = 'Drag ships to lower grid with left mouse button Right click to rotate'
    lines = text_info.split(' ')
    surface = pygame.Surface((width, height))
    max_x, max_y = surface.get_size()
    surface.fill(info_color)
        
    for word in lines:
        text_surface = font.render(word, 0, 'white')
        w_width, w_height = text_surface.get_size()
        if x + w_width >= max_x:
            x = base_pos_2[0]
            y += w_height+height*0.05
        surface.blit(text_surface, (x, y))
        x += w_width + space_w
    SCREEN.blit(surface, (WIDTH//6, HEIGHT//6))          
               
#END OF UTILITY FUNCTIONS

class info: #correct
    def __init__(self):
        self.width = WIDTH//2
        self.height = int(HEIGHT*0.9)
        self.body = pygame.Surface((convert(180, 'W'), convert(100, 'H'))).get_rect(center=(self.width, self.height))
        self.text = pygame.font.SysFont('Arial', convert(20, 'H')).render('START GAME', True, "white")
        self.text_rect = self.text.get_rect(center=(self.width, self.height))
        self.clock = 0
        self.message = None
        self.last_state = None
    def start_button(self, game_map): #I'm not sure weather it was good idea to move it into info class
        global play 
        if play == True:
            game_map.start_game()
            return
        mouse = pygame.mouse.get_pos()
        if self.body.collidepoint(mouse):
            all_set = 0
            for s in game_map.ships:
                if s.collides:
                    all_set+=1
            if pygame.mouse.get_pressed(num_buttons=3)[0] and all_set == len(game_map.ships):
                play = True
                for s in game_map.ships:
                    game_map.your_segments += s.size_unit
                    for i in game_map.your_tiles:
                        if i.body.colliderect(s.body):
                            i.unit_num = s.size_unit
                for index,i in enumerate(game_map.your_tiles):
                    print(i.unit_num, end='')
                    if index%10 == 9:
                        print()
                game_map.enemy_placement()
            elif pygame.mouse.get_pressed(num_buttons=3)[0]:
                info().hit_msg(("put all ships onto the grid", "player")) #have to create instance or something
                
        pygame.draw.rect(SCREEN, info_color, self.body)
        SCREEN.blit(self.text, self.text_rect)
        
    def hit_msg(self, message): #msg has to be text
        if message == None and self.clock != 0:
            msg, state = self.message, self.last_state
            self.clock-=1
        elif message == None:
            return
        else:
            msg, state = message[0], message[1]
            self.message = msg
            self.last_state = state
            self.clock = 30
        clock = self.clock
        color = "green"
        if state == 'player':
            color = "red"
        text = pygame.font.SysFont('Arial', convert(100, 'H')).render(msg, True, color)
        surface = pygame.Surface((convert(1000, 'W'), convert(400, 'H')))#
        mid_pos_1 = surface.get_rect(center=(WIDTH//2, HEIGHT//2+clock))
        mid_pos_2 = text.get_rect(center=(WIDTH//2, HEIGHT//2+clock))
        surface.fill(info_color)
        SCREEN.blit(surface, mid_pos_1)
        SCREEN.blit(text, mid_pos_2)
        if self.clock == 0:
            self.message = None
            self.last_state = None
        
    def fin_msg(self, msg, color):
        h_width = convert(800, 'W')
        h_height = convert(600, 'H')
        h_width_2 = convert(200, 'W')
        h_height_2 = convert(100, 'H')
        text_size = convert(80, 'H')
        button_0 = button(msg, convert(100, 'H'), WIDTH//2-h_width//2, HEIGHT//2-h_height//2, h_width, h_height, info_color)
        #because button is not created around the point x,y but x,y is top right corner we get small problem
        button_1 = button('RESTART', text_size, WIDTH//2-h_width_2-int(h_width*0.05), HEIGHT//2+int(h_height*1/4), h_width_2, h_height_2, color)
        button_2 = button('QUIT', text_size, WIDTH//2+int(h_width*0.05), HEIGHT//2+int(h_height*1/4), h_width_2, h_height_2, color)
        
        mouse = pygame.mouse.get_pos()
        if button_1.collidepoint(mouse):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                return 'restart'
        elif button_2.collidepoint(mouse):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                pygame.quit()
                sys.exit()
        
class tile():
    def __init__(self, x, y, tile_state, tile_map):
        self.width = convert(64, 'H') #don't change it should be like this
        self.height = convert(64, 'H')
        self.x = (WIDTH - 10*self.width)/2 + x
        self.y = y
        self.clicked = False
        self.unit_num = 0
        self.state =  tile_state
        self.colors = {
            'normal': (88,135,183),
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
        if self.state != g_state:
            mouse = pygame.mouse.get_pos()
            if not self.clicked:
                self.color = self.colors['normal'] 
            if self.body.collidepoint(mouse) and not self.clicked:
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.clicked = True
                    if self.unit_num != 0:
                        self.color = self.colors['hit']
                        return ('HIT!!!', self.state, 1)
                    else:
                        self.color = self.colors['miss']
                        return ('MISS!!!', self.state, 0)
                elif self.body.collidepoint(mouse):
                    self.color = self.colors['hover']
        return None
    def set_tile(self):
        if self.unit_num == 0:
            self.color = self.colors['miss']
            return ('MISS!!!', self.state, 0)
        else:
            self.color = self.colors['hit']
            return ('HIT!!!', self.state, 1)

    
class g_map():
    def __init__(self):
        self.your_segments = 0
        self.enemy_segments = 0
        self.your_hits = 0 #it's a bad name XD It means how many times you were hit
        self.enemy_hits = 0
        self.enemy_tiles = []
        self.your_tiles = []
        self.game_state = None
        self.ships_set = [1, 1, 1, 2, 2, 2, 3, 3, 3]
        self.ships = []
        x = 0
        y = convert(166, 'H')
        for i in range(1, 101):
            tile(x, y, 'enemy', self.enemy_tiles)
            x+=self.enemy_tiles[0].width
            if i%10 == 0:
                y+=self.enemy_tiles[0].height
                x = 0

        x = 0
        y+=convert(66, 'H')
        for i in range(1, 101):
            tile(x, y, 'player', self.your_tiles)
            x+=self.your_tiles[0].width
            if i%10 == 0:
                y+=self.your_tiles[0].height
                x = 0
        
        x = int(1900*WIDTH/BASE_WIDTH)
        y = HEIGHT*0.2
        z = 1
        for index,i in enumerate(self.ships_set):
            ship(index, i, x, y, convert(36, 'H'), convert(36, 'H'), self.ships) #IT SHOULD BE 2 TIMES 'H'
            y += convert(80, 'H')
        
    def start_game(self):
        if self.game_state == None:
            self.game_state = 'player'
    def change_state(self): #sometimes you get double turn i need to find out why
        if self.game_state == 'player':
            self.game_state = 'enemy'
        else:
            self.game_state = 'player'
    def interact(self):
        for s in self.ships:
            s.interact(event, game_map)
        ret = None
        print(self.game_state)
        if self.game_state == None:
            return
        elif self.game_state == 'player': 
            for tile in self.enemy_tiles:
                ret = tile.interact(self.game_state)
                if ret != None:
                    self.change_state()
                    break
        else:
            position = int(input()) #bot should return position
            ret = self.your_tiles[position].set_tile()
            self.change_state()
            
        if ret == None:
            return ret
        if ret[1] == 'player' and ret[2] == 1:
            self.your_hits += 1
        elif ret[1] == 'enemy' and ret[2] == 1:
            self.enemy_hits += 1
        return ret

    def draw_map(self):
        SCREEN.fill(base_color)
        for ob in self.enemy_tiles:
            ob.draw()
        for ob in self.your_tiles:
            ob.draw()
        for s in self.ships:
            s.draw()
    def ending(self):
        if self.game_state == None:
            return
        if self.your_segments == self.your_hits:
            return 'YOU LOSE!!!'
        elif self.enemy_segments == self.enemy_hits:
            return 'YOU WIN!!!'
        else:
            return None
    
    def enemy_placement(self):
        for ii in self.ships_set:
            rotation = random.randint(0,1)
            while True:
                no = False
                placement = random.randint(0, 99)
                if not rotation and placement%10 < (11 - ii): 
                    j = ii
                    while j > 0:
                        if self.enemy_tiles[placement + j-1].unit_num != 0:
                            no = True
                            break
                        j-=1
                    if no:
                        continue
                    j = ii
                    while j > 0:
                        self.enemy_tiles[placement + j-1].unit_num = ii
                        j-=1
                    self.enemy_segments += ii
                    break     
                if rotation and placement < 99 - 10*ii:
                    j = ii
                    while j > 0:
                        if self.enemy_tiles[placement + 10*(j-1)].unit_num != 0:
                            no = True
                            break
                        j-=1
                    if no:
                        continue
                    j = ii
                    while j > 0:
                        self.enemy_tiles[placement + 10*(j-1)].unit_num = ii
                        j-=1
                    self.enemy_segments += ii
                    break
        print()
        print('enemy map')
        for index,i in enumerate(self.enemy_tiles):
            print(i.unit_num, end='')
            if index%10 == 9:
                print()
        print('enemy segments', self.enemy_segments)
        print('your segments', self.your_segments)
        
class ship():
    def __init__(self, number, size_unit, x, y, width, height, ships):
        self.number = number
        self.size_unit = size_unit
        if self.size_unit == 1:
            width = width
        elif self.size_unit == 2:
            width = convert(100, 'H')
        else:
            width = convert(164, 'H')
        self.body = pygame.Rect(x, y, width, height)
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
                for s in game_map.ships:
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
                           or (self.size_unit == 2 and num not in list_1) or (self.size_unit == 3 and num not in list_2): #to clean up
                            self.body.x = i.body.x+convert(14, 'H')
                            self.body.y = i.body.y+convert(14, 'H')
                            self.collides = True
                            return;
                    elif i.body.colliderect(self.body) and self.rotation:
                        if (self.size_unit == 2 and index < 90) or (self.size_unit == 3 and index < 80):
                            self.body.x = i.body.x+convert(14, 'H')
                            self.body.y = i.body.y+convert(14, 'H')
                            self.collides = True
                            return
                self.body.x = self.befx
                self.body.y = self.befy
                self.collides = False

            if event.type == pygame.MOUSEMOTION:
                if collides_with == self.number:
                    self.body.move_ip(event.rel)

#CLASS INSTANCES                 
game_map = g_map()
info_i = info()
inner_clock = 0
#GAME LOOP
while True:
    msg = None
    for event in pygame.event.get(): #if you put and ship and take it away you can start playing
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        msg = game_map.interact()
                
    game_map.draw_map()
    info_i.start_button(game_map)
    right_message()
    #game_map.change_state(msg)
    info_i.hit_msg(msg)
    msg = game_map.ending()
    if msg != None:
        if info_i.fin_msg(msg, "green") == 'restart':
            restart(game_map)
            game_map = g_map()
    #info_i.fin_msg("YOU WIN!!", "green")                
    pygame.display.flip()
    CLOCK.tick(FPS)        
