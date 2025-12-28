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


ships = []
ships_set = [1, 1, 1, 2, 2, 2, 3, 3, 3]

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

def restart():
        ships.clear()
        global play
        play = False
        global state
        state = 'None'
        global collides_with
        collides_with= None
        
#END OF UTILITY FUNCTIONS

class info: #correct
    def __init__(self):
        self.width = WIDTH//2
        self.height = int(HEIGHT*0.9)
        self.body = pygame.Surface((convert(180, 'W'), convert(100, 'H'))).get_rect(center=(self.width, self.height))
        self.text = pygame.font.SysFont('Arial', convert(20, 'H')).render('START GAME', True, "white")
        self.text_rect = self.text.get_rect(center=(self.width, self.height))
        
    def start_button(self, game_map): #I'm not sure weather it was good idea to move it into info class
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
            if pygame.mouse.get_pressed(num_buttons=3)[0] and all_set == len(ships):
                play = True
                for s in ships:
                    game_map.your_segments += s.size_unit
                    for i in game_map.your_tiles:
                        if i.body.colliderect(s.body):
                            i.unit_num = s.size_unit
                for index,i in enumerate(game_map.your_tiles):
                    print(i.unit_num, end='')
                    if index%10 == 9:
                        print()
                random_placement(ships_set, game_map)
            elif pygame.mouse.get_pressed(num_buttons=3)[0]:
                info.hit_msg("put all ships onto the grid", "player")
                
        pygame.draw.rect(SCREEN, info_color, self.body)
        SCREEN.blit(self.text, self.text_rect)

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
        
    def hit_msg(msg, state): #msg has to be text
        color = "green"
        if state == 'player':
            color = "red"
        text = pygame.font.SysFont('Arial', convert(100, 'H')).render(msg, True, color)
        surface = pygame.Surface((convert(1000, 'W'), convert(400, 'H')))#
        mid_pos_1 = surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        mid_pos_2 = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        surface.fill(info_color)
        SCREEN.blit(surface, mid_pos_1)
        SCREEN.blit(text, mid_pos_2)
        
    def fin_msg(msg, color):
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
        if self.state == g_state:
            mouse = pygame.mouse.get_pos()
            if not self.clicked:
                self.color = self.colors['normal'] # dosn't work as should
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

    
class g_map():
    def __init__(self):
        self.your_segments = 0
        self.enemy_segments = 0
        self.your_hits = 0 #it's a bad name XD It means how many times you were hit
        self.enemy_hits = 0
        self.enemy_tiles = []
        self.your_tiles = []
        self.game_state = None
        x = 0
        y = convert(166, 'H')
        for i in range(1, 101): #i need to start it from 2880 1800 but it starts here from 1920 1080
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
        for i in range(0, 9):
            ship(i, z, x, y, convert(36, 'H'), convert(36, 'H')) #IT SHOULD BE 2 TIMES 'H'
            if i == 2 or i == 5:
                z +=1
            y += 80
        
    def start_game(self):
        if self.game_state == None:
            self.game_state = 'enemy'
    def change_state(self):
        if self.game_state == 'player':
            self.game_state = 'enemy'
        else:
            self.game_state = 'player'
    def interact(self):
        ret = None
        if self.game_state == None:
            return
        elif self.game_state == 'player': 
            for tile in self.your_tiles:
                ret = tile.interact(self.game_state)
                if ret != None:
                    break

        else:
            for tile in self.enemy_tiles:
                ret = tile.interact(self.game_state)
                if ret != None:
                    break
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
    def ending(self):
        if self.game_state == None:
            return
        if self.your_segments == self.your_hits:
            return 'YOU LOSE!!!'
        elif self.enemy_segments == self.enemy_hits:
            return 'YOU WIN!!!'
        else:
            return None
        
class ship():
    def __init__(self, number, size_unit, x, y, width, height):
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

            if event.type == pygame.MOUSEMOTION:
                if collides_with == self.number:
                    self.body.move_ip(event.rel)

def random_placement(ships_set, game_map):
    for i in ships_set:
        rotation = random.randint(0,1)
        while True:
            no = False
            placement = random.randint(0, 99) 
            if not rotation and placement%10 < (11 - i): 
                j = i
                while j > 0:
                    if game_map.enemy_tiles[placement + j-1].unit_num != 0:
                        no = True
                        break
                    j-=1
                if no:
                    continue
                j = i
                while j > 0:
                    game_map.enemy_tiles[placement + j-1].unit_num = i
                    j-=1
                game_map.enemy_segments += i
                break     
            if rotation and placement < 99 - 10*i:
                j = i
                while j > 0:
                    if game_map.enemy_tiles[placement + 10*(j-1)].unit_num != 0:
                        no = True
                        break
                    j-=1
                if no:
                    continue
                j = i
                while j > 0:
                    game_map.enemy_tiles[placement + 10*(j-1)].unit_num = i
                    j-=1
                game_map.enemy_segments += i
                break            
    print()
    print('enemy map')
    for index,i in enumerate(game_map.enemy_tiles):
                    print(i.unit_num, end='')
                    if index%10 == 9:
                        print()
    print('enemy segments', game_map.enemy_segments)
    print('yoru segments', game_map.your_segments)
        


#start = start_button()
game_map = g_map()
while True:
    #info.fin_msg("YOU WIN!!", "green")
    for event in pygame.event.get(): #everything is dependent on user actions if nothing happens nothing is updated tragic...
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        msg = game_map.interact()
        game_map.draw_map()

        for s in ships:
            s.interact(event, game_map)
            s.draw()
        if msg != None:
            game_map.change_state()
            info.hit_msg(msg[0], msg[1])

        info().start_button(game_map)
        info.right_message()
        msg = game_map.ending()
        if msg != None:
            if info.fin_msg(msg, "green") == 'restart':#have to do restart ... D:
                restart()
                game_map = g_map()
                    
    pygame.display.flip()
    CLOCK.tick(FPS)        

