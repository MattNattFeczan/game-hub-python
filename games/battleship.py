import pygame
import sys

pygame.init()
FPS = 60
CLOCK = pygame.time.Clock()
WIDTH, HEIGHT = 1180, 1440
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN.set_alpha(None)
pygame.display.set_caption("Battleship")

enemy_tiles = []
your_tiles = []
ships = []

base_color = (100, 180, 220)
collides_with = None
play = False

class tile():
    def __init__(self, x, y, tile_map):
        self.x = (WIDTH - 640)/2 + x
        self.y = y
        self.width = 64
        self.height = 64
        self.clicked = False
        self.colors = {
            'normal': base_color,
            'hover': (219, 145, 140),
            'hit': (76, 219, 87),
            'miss': ()
        }
        
        self.surface = pygame.Surface((self.width, self.height))
        self.body = pygame.Rect(self.x, self.y, self.width, self.height)
        tile_map.append(self)

    def draw(self):

        global play
        self.surface.fill(self.colors['normal']) # we have problem here it makes it so that marking isn't permament
        if play != False:
            mouse = pygame.mouse.get_pos()


            if self.body.collidepoint(mouse) and not self.clicked:
                self.surface.fill(self.colors['hover'])

                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.clicked = True
                    self.surface.fill(self.colors['hit'])
                elif not self.clicked:
                    self.surface.fill(self.colors['normal'])
            

        SCREEN.blit(self.surface, self.body)
        pygame.draw.rect(SCREEN, (0, 0, 0), [self.x+3, self.y+3, self.width-6, self.height-6], width=3)

        
class ship():
    def __init__(self, number, size_unit, x, y, width, height):
        self.number = number
        self.size_unit = size_unit
        self.body = pygame.Rect(x, y, self.size_unit*width, height)
        self.color = (255, 255, 255)
        ships.append(self)
    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.body)
    def interact(self, event):
        global collides_with
        if play == False:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                        if self.body.collidepoint(event.pos):
                            collides_with = self.number
                if self.size_unit != 1 and event.button == 3 and self.body.collidepoint(event.pos):
                    k = self.body.width
                    self.body.width = self.body.height
                    self.body.height = k

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    collides_with = None

            if event.type == pygame.MOUSEMOTION:
                if collides_with == self.number:
                    self.body.move_ip(event.rel)


class start_button():
    def __init__(self):
        self.body = pygame.Rect(WIDTH/2, HEIGHT-40, 120, 60) #to do make it better
        self.text = pygame.font.SysFont('Arial', 20).render('START GAME', True, "white")
    def interact(self):
        mouse = pygame.mouse.get_pos()
        global play
        if self.body.collidepoint(mouse):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                play = True
        if play == False:
            SCREEN.blit(self.text, self.body)
            

x = 950
y = 500
z = 1
for i in range(0, 7):
    ship(i, z, x, y, 38, 38)
    if i == 2 or i == 5:
        z +=2
    y += 80
    
x = 0
y = 44      
for i in range(1, 101):
    tile(x, y, enemy_tiles)
    x+=64
    if i%10 == 0:
        y+=64
        x = 0

x = 0
y = 748
for i in range(1, 101):
    tile(x, y, your_tiles)
    x+=64
    if i%10 == 0:
        y+=64
        x = 0


start = start_button()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        SCREEN.fill(base_color)
        for ob in enemy_tiles:
            ob.draw()

        for ob in your_tiles:
            ob.draw()

        for s in ships:
            s.interact(event)
            s.draw()

        start_button().interact()


    pygame.display.flip()
    CLOCK.tick(FPS)        

