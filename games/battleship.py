import pygame
import sys
import random
import time
import bisect

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
info_color_2 = (100,130,140)
collides_with = None
play = False
state = 'None'
shake=0

#UTILITY FUNCTIONS

def convert(number: int , dimension: str) -> int:
    if dimension == 'H':
        return int(number*HEIGHT/BASE_HEIGHT)
    elif dimension == 'W':
        return int(number*WIDTH/BASE_WIDTH)
    else:
        return 0

def button(msg, size, x, y, width, height, color, color2, interact: bool):
    ret = False
    surface = pygame.Surface((width, height))
    font = pygame.font.SysFont('Arial', convert(size, 'H')).render(msg, True, "white")
    mid_pos = font.get_rect(center=(width//2, height//2))
    ret_rect = pygame.Rect(x, y, width, height)
    if ret_rect.collidepoint(pygame.mouse.get_pos()) and interact:
        color = color2
        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            ret = True
             
    surface.fill(color)
    surface.blit(font, mid_pos)
    SCREEN.blit(surface, (x,y))

    return ret

def restart(game_map, bot):
        game_map.ships.clear()
        bot.reset()
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

def isnt_touching(tile_array, index) -> bool:
    base_index= index-10 #debatable decision
    for r in range(0, 3):
        index = base_index+10*r
        comp = index%10
        if index < 0:
            continue
        if index > 99:
            continue
        if tile_array[index].unit_num != 0:
            return False
        if 0 < comp and tile_array[index-1].unit_num != 0:
            return False
        if comp < 9 and tile_array[index+1].unit_num != 0:
            return False
    return True
        
               
#END OF UTILITY FUNCTIONS
'''------------------FIRE------------------'''
class Particle:
    def __init__(self, x, y):
	    self.x=x
	    self.y=y
	    self.lifespan=random.randint(60,80)
	    self.size=random.randint(3,9)
	    self.movex=random.randint(-1,1)
	    self.movey=random.randint(-2,-1)
    def move_it(self):
	    self.x=self.x+self.movex+random.randint(-1,1)
	    self.y=self.y+self.movey+random.randint(-1,1)
	    if self.lifespan>0:
	        self.lifespan-=2
	    if self.size>0:
	        self.size-=0.1
    def draw(self):
	    colour=0
	    if self.lifespan>60:
	        colour=255, 165, 0, 255
	    elif self.lifespan>50:
	        colour=255, 255, 0, 255
	    elif self.lifespan>45:
	        colour=255, 165, 0, 255
	    elif self.lifespan>30:
	        colour=205, 0, 0, 255
	    else:
	        colour=139, 125, 107, 255 #bisque 4
	    pygame.draw.rect(SCREEN, colour, (self.x, self.y, self.size, self.size))
	    
class Fire:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.on=True
        self.particles=[]
    def manage_particles(self):
        if self.on:
            for i in range(3):
                self.particles.append(Particle(self.x+random.randint(-10,10),self.y+random.randint(-1,1)))
        for p in self.particles:
            if p.lifespan<=0 or p.size<=0:
                self.particles.remove(p)
        for p in self.particles:
            p.draw()
            p.move_it()


'''---------------------------------BOT-----------------------------------------------'''
class Bot:
    def __init__(self):
        self.plansza=[[0]*10 for i in range(10)] #0 gdy pole nieodkryte -1 gdy pudlo -2 gdy trafiony 
        self.pozostale_statki=[0, 3, 3, 3, 0, 0] # indeks to dlugosc, wartosc to liczba pozostalych statkow o danej dlugosci
        self.statek=[] #posortowane wspolrzedne trafionych pol konkretnego statku, ktory nalezy dobic
        self.ktory=0
        self.trafione_pola=0 #ile zatopionych pol
        self.sprawdz_obok_x=[1,-1,0,0]
        self.sprawdz_obok_y=[0,0,1,-1]
        
    def reset(self):
        self.plansza=[[0]*10 for i in range(10)] 
        self.pozostale_statki=[0, 3, 3, 3, 0, 0]
        self.statek=[]
        self.ktory=0
        self.trafione_pola=0
        
    def zaktualizuj_pozostale_pola(self):
        pozostale=[]
        szachownica=self.czy_zostaly_statki(2)
        for i in range (10):
            for j in range (10):
                if self.plansza[i][j]==0:
                    if szachownica:
                        if not (i+j)%2:
                            pozostale.append((i,j))
                    else:
                        pozostale.append((i,j))   
        if not pozostale: # na wszelki wypadek chociaz to raczej niemozliwe
            for i in range (10):
                for j in range (10):
                    if self.plansza[i][j]==0:
                        pozostale.append((i,j))
        return pozostale

    def czy_zostaly_statki(self, od): #czy sa jeszcze jakies statki dluzsze lub rowne od
        for i in range (od, 6):
            if(self.pozostale_statki[i]):
                return True
        return False  
        
    def zatop(self):
        x_pocz, y_pocz=self.statek[0]
        x_kon, y_kon=self.statek[-1]
        for i in range(x_pocz-1, x_kon+2):
            for j in range(y_pocz-1, y_kon+2):
                if -1<i<10 and -1<j<10:
                    if self.plansza[i][j]!=-2:
                        self.plansza[i][j]=-1

    def kontynuuj(self): #jesli trafiony strzelaj dalej
        if len(self.statek)==1:
            i,j=self.statek[0]
            while self.ktory<4:
                test_i=i+self.sprawdz_obok_x[self.ktory]
                test_j=j+self.sprawdz_obok_y[self.ktory] 
                self.ktory+=1
                if -1<test_i<10 and -1<test_j<10 and self.plansza[test_i][test_j]==0:
                    return test_i, test_j  
            return None, None
        else:
            x_pocz, y_pocz=self.statek[0]
            x_kon, y_kon=self.statek[-1]
            if x_pocz-x_kon==0:
                if y_pocz-1>-1 and self.plansza[x_pocz][y_pocz-1]==0:
                    return x_pocz, y_pocz-1
                elif y_kon+1<10 and self.plansza[x_pocz][y_kon+1]==0:
                    return x_pocz, y_kon+1
            elif y_pocz-y_kon==0:
                if x_pocz-1>-1 and self.plansza[x_pocz-1][y_pocz]==0:
                    return x_pocz-1, y_pocz
                elif x_kon+1<10 and self.plansza[x_kon+1][y_pocz]==0:
                    return x_kon+1, y_pocz
            return None, None

    def shoot(self):
        losowanie=self.zaktualizuj_pozostale_pola() #czy moze byc puste?
        i,j=(None, None)
        if self.statek:
            i,j=self.kontynuuj()
        if i is None: #jesli zamiast if wstawic else nie sprawdzalby czy kontynuuj zwrocilo none
            self.ktory=0
            self.statek=[]
            if not losowanie: 
                print('brak wolnych pol', file=sys.stderr)
                return 0
            i,j=random.choice(losowanie)
        return i*10+j
            
            
    def deal_with_it(self, trafiony, x, y): #trafiony powinno byc rowne dlugosci trafionego statku
        if not trafiony:
            self.plansza[x][y]=-1
        else:
            self.ktory=0
            self.trafione_pola+=1
            self.plansza[x][y]=-2
            bisect.insort(self.statek, (x, y))
            if len(self.statek)==trafiony or not self.czy_zostaly_statki(len(self.statek)+1):
                self.zatop()
                self.pozostale_statki[len(self.statek)]-=1
                self.statek=[]
                #print('fiony zatopiony')
'''------------------------------------------------------------------------------'''               

class info: #correct
    def __init__(self):
        self.w = convert(400, 'W')
        self.h = convert(100, 'H')
        self.clock = 0
        self.message = None
        self.last_state = None
    def start_button(self, game_map): #I'm not sure weather it was good idea to move it into info class
        ret = False
        global play
        if play == True:
            game_map.start_game()
            return
        ret = button('START GAME', convert(60, 'H'), WIDTH//2 -self.w//2, int(HEIGHT*0.9), self.w, self.h, info_color, info_color_2, True)
        if ret == True:
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
                self.hit_msg(("put all ships onto the grid", "player"))

    def hit_msg(self, message):
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
        text = pygame.font.SysFont('Arial', convert(100, 'H'))
        width, height = text.size(msg)
        text = text.render(msg, True, color)

        surface = pygame.Surface((convert(width*2, 'W'), convert(height*4, 'H')))
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
        button_0 = button(msg, convert(100, 'H'), WIDTH//2-h_width//2, HEIGHT//2-h_height//2, h_width, h_height, info_color, info_color, False)
        #because button is not created around the point x,y but x,y is top right corner we get small problem
        ret = button('RESTART', text_size, WIDTH//2-h_width_2-int(h_width*0.05), HEIGHT//2+int(h_height*1/4), h_width_2, h_height_2, color, info_color_2, True)
        if ret == True:
            return 'restart'
        ret = button('QUIT', text_size, WIDTH//2+int(h_width*0.05), HEIGHT//2+int(h_height*1/4), h_width_2, h_height_2, color, info_color_2, True)
        if ret == True:       
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
        self.s_list = None
        self.s_pos = 0
        self.colors = {
            'normal': (88,135,183),
            'hover': (219, 145, 140),
            'hit': (76, 219, 87),
            'miss': (255, 75, 0),
            'sunk': (149, 194, 160)
        }
        self.name = None
        self.color = self.colors['normal']
        self.surface = pygame.Surface((self.width, self.height))
        self.body = pygame.Rect(self.x, self.y, self.width, self.height)
        self.burning=None
        tile_map.append(self)

    def update_name(self):
        if self.unit_num == 1:
            self.name = 'DESTROYER'
        elif self.unit_num == 2:
            self.name = 'SUBMARINE'
        elif self.unit_num == 3:
            self.name = 'BATTLESHIP'

    def draw(self):
        if self.s_list != None:
            if self.s_list[self.s_pos] == 0:
                self.color = self.colors['sunk']
        self.surface.fill(self.color) 
        SCREEN.blit(self.surface, self.body)
        pygame.draw.rect(SCREEN, (0, 0, 0), [self.x+3, self.y+3, self.width-6, self.height-6], width=3)
        if self.color==self.colors['sunk']: 
            if self.burning is not None: self.burning.on=False
        if self.burning is not None:
            if not self.burning.on and not self.burning.particles: self.burning=None
        if self.burning is not None: self.burning.manage_particles()
    def interact(self, g_state, event):
        if self.state != g_state:
            mouse = pygame.mouse.get_pos()
            if not self.clicked:
                self.color = self.colors['normal'] 
                if self.body.collidepoint(mouse):
                    if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                        self.clicked = True
                        if self.unit_num != 0:
                            print(self.s_list)
                            if self.s_list[self.s_pos] > 1:
                                self.s_list[self.s_pos]-=1
                                self.burning=Fire(self.x+self.width//2,self.y+self.height//2) #position still needs some work...
                                msg = 'HIT!!!'
                            else:
                                self.s_list[self.s_pos]-=1
                                msg = self.name + ' SUNKEN!!!'

                            self.color = self.colors['hit']
                            return (msg, self.state, 1)
                        else:
                            self.color = self.colors['miss']
                            return ('MISS!!!', self.state, 0)
                    else:
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
        self.waves=[(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for i in range (70)]
        self.bot_thought_process=0
        self.delay = 0
        
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
    def change_state(self):
        if self.game_state == 'player':
            self.game_state = 'enemy'
        else:
            self.game_state = 'player'
    def player_interact(self, mouse_event):
        global shake
        for s in self.ships:
            s.interact(mouse_event, game_map)
        ret = None
        #print(self.game_state)
        if self.game_state == 'player': 
            for tile in self.enemy_tiles:
                ret = tile.interact(self.game_state, mouse_event)
                if ret != None:
                    if ret[2]==1:
                        self.enemy_hits+=1
                        shake=20
                    else:
                        self.delay = 1
                        self.change_state()
                        self.bot_thought_process=60
                    return ret
        return ret
        
    def bot_interact(self):
        global shake
        ret=None
        if self.game_state=='enemy':
            if self.bot_thought_process>0:
                self.bot_thought_process-=1
            else:
                position = bot.shoot() 
                bot.deal_with_it(self.your_tiles[position].unit_num, position//10, position%10)
                ret = self.your_tiles[position].set_tile()
                if ret[2]==1:
                    self.your_hits+=1
                    self.bot_thought_process=60
                    shake=20
                else:
                    self.change_state() 
        return ret

    def delay_check(self):
        if self.delay == 0:
            return True
        if self.delay == 30:
            self.delay = 0
            return False
        else:
            self.delay+=1
            return False

    def draw_map(self):
        global shake
        shift_x=0
        shift_y=0
        SCREEN.fill(base_color)
        if shake>0:
            shift_x=random.randint(-10,10)
            shift_y=random.randint(-10,10)
            shake-=1
        for x, y in self.waves: pygame.draw.line(SCREEN, (150, 190, 200), (x+shift_x, y+shift_y), (x+30+shift_x, y+shift_y), 2)
        self.waves = [((x + 0.5) % WIDTH, y) for x, y in self.waves]
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
        for index,ii in enumerate(self.ships_set):
            rotation = random.randint(0,1)
            while True:
                no = False
                placement = random.randint(0, 99)
                if not rotation and placement%10 < (11 - ii): 
                    j = ii
                    while j > 0:
                        if isnt_touching(self.enemy_tiles, placement+j-1) == False:
                            no = True
                            break
                        j-=1
                    if no:
                        continue
                    j = ii
                    while j > 0:
                        self.enemy_tiles[placement + j-1].unit_num = ii
                        self.enemy_tiles[placement + j-1].s_list = self.ships_set
                        self.enemy_tiles[placement + j-1].s_pos = index
                        self.enemy_tiles[placement + j-1].update_name()
                        j-=1
                    self.enemy_segments += ii
                    break     
                if rotation and placement < 99 - 10*ii:
                    j = ii
                    while j > 0:
                        if isnt_touching(self.enemy_tiles, placement + 10*(j-1)) == False:
                            no = True
                            break
                        j-=1
                    if no:
                        continue
                    j = ii
                    while j > 0:
                        self.enemy_tiles[placement + 10*(j-1)].unit_num = ii
                        self.enemy_tiles[placement + 10*(j-1)].s_list = self.ships_set
                        self.enemy_tiles[placement + 10*(j-1)].s_pos = index
                        self.enemy_tiles[placement + 10*(j-1)].update_name()
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
        if self.size_unit == 1:
            self.name = 'destroyer'
        elif self.size_unit == 2:
            self.name = 'submarine'
        else:
            self.name = 'battleship'
        self.body = pygame.Rect(x, y, width, height)
        self.befx = self.body.x
        self.befy = self.body.y
        self.color = (255, 255, 255)
        self.rotation = 0
        self.hits = 0
        self.collides = False
        ships.append(self)
    def sunken(self):
        if self.hits != self.size_unit:
            return None
        return self.name
    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.body)
    def interact(self, event, game_map):
        global collides_with
        if play == False:
            check = False
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
                            check = True
                            self.collides = True
                            break
                    elif i.body.colliderect(self.body) and self.rotation:
                        if (self.size_unit == 2 and index < 90) or (self.size_unit == 3 and index < 80):
                            self.body.x = i.body.x+convert(14, 'H')
                            self.body.y = i.body.y+convert(14, 'H')
                            check = True
                            self.collides = True
                            break
                if self.rotation:
                    width = game_map.your_tiles[0].width*3
                    height = game_map.your_tiles[0].width*(self.size_unit+2)
                else:
                    width =  game_map.your_tiles[0].width*(self.size_unit+2)
                    height = game_map.your_tiles[0].width*3
                    
                collision_detector = pygame.Rect(0, 0, width, height)
                collision_detector.center = self.body.center
                #collision_detector = collision_detector.center=(self.body.x + self.body.width//2, self.body.y + self.body.height//2)
                for s in game_map.ships:
                    if collision_detector.colliderect(s.body) and s != self:
                        check = False
                        
                if check == False:
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
bot=Bot()
msg=None
#GAME LOOP
while True:
    #msg = None
    ended = game_map.ending()
    events=pygame.event.get()
    for event in events: 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_map.game_state=='enemy' and ended is None:
            msg = game_map.player_interact(event)
    if game_map.delay_check():
        if game_map.game_state=='enemy' and ended is None:
            msg=game_map.bot_interact()
            
    game_map.draw_map()
    info_i.start_button(game_map)
    right_message()
    info_i.hit_msg(msg) 
    if info_i.clock>0:
        msg=None
    #info_i.fin_msg('YOU WIN!!!', "green") 
    if ended != None:
        if info_i.fin_msg(ended, "green") == 'restart':
            restart(game_map, bot)
            game_map = g_map()    
    pygame.display.flip()
    CLOCK.tick(FPS)        
