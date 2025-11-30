import pygame
import sys

pygame.init()
FPS = 60
CLOCK = pygame.time.Clock()
WIDTH, HEIGHT = 1080, 1440
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN.set_alpha(None)

enemy_tiles = []
your_tiles = []

class tile():
    def __init__(self, x, y, tile_map):
        self.x = (WIDTH - 640)/2 + x
        self.y = y
        self.width = 64
        self.height = 64
        self.clicked = False
        self.colors = {
            'normal': (120, 120, 120),
            'hover': (219, 145, 140),
            'hit': (76, 219, 87),
            'miss': ()
        }
        
        self.surface = pygame.Surface((self.width, self.height))
        self.body = pygame.Rect(self.x, self.y, self.width, self.height)

        tile_map.append(self)

    def draw(self):
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


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        SCREEN.fill((98, 99, 181))
        for ob in enemy_tiles:
            ob.draw()

        for ob in your_tiles:
            ob.draw()


    pygame.display.flip()
    CLOCK.tick(FPS)        
