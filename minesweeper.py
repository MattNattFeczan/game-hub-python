import pygame
import random
import sys

pygame.init()

# Gra zawiera 4 typy rozgrywki:

    #Początkujący – plansza 8×8 pól, 10 min, ryzyko trafienia na minę: 15,625%
    #Zaawansowany – plansza 16×16 pól, 40 min, ryzyko trafienia na minę: 15,625%
    #Ekspert – plansza 30×16 pól, 99 min, ryzyko trafienia na minę: 20,625%
    #Plansza użytkownika – gracz sam wybiera rozmiary planszy (od 8×8 do 30×24 pól) i liczbę min (od 10 do 240).

#Możliwa maksymalna liczba min zależna jest od rozmiarów planszy. Dla planszy o rozmiarach A×B maksymalna liczba #wynosi A×B/3, czyli np. na planszy o rozmiarach 12×16 pól może być najwyżej 12×16/3=64 miny.

#obsługa pierwszego kliknięcia

def deltas():
  return ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

class Button():

    def __init__(self, game, i, j, image_normal, image_dark):
    
        self.game = game
        self.i = i
        self.j = j
    
        self.x = 50 + (i*50)
        self.y = 50 + (j*50)
    
        self.image1 = image_normal
        self.image2 = image_dark
        self.image = image_normal
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.clicked = False
        self.is_mine = False
        self.mines_around = 0
        self.is_visited = False
        self.is_flagged = False
        self.mines_around = 0
        
    
    def draw(self):
    
        self.game.screen.blit(self.image, (self.rect.x, self.rect.y))
        
        if self.is_visited:
        
            text = self.game.font.render(str(self.mines_around), True, (0, 0, 0))
            self.game.screen.blit(text, (self.rect.x, self.rect.y))
            
        
        
    def check_event(self):
        
        
        #mouse position
        pos = pygame.mouse.get_pos()
        
        #check if the mouse is pointing on the buttons
        
        if self.rect.collidepoint(pos):
        
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            
                self.clicked = True
                
                self.game.FirstClick(self.i, self.j)
                
                self.game.Dfs(self.i, self.j)



class Game():

    first_click = False
    SCREEN_HEIGHT = 500
    SCREEN_WIDTH = 800

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT));

    #pygame.image.load().convert_alpha()

    #button class

    #przycisk_png = pygame.image.load('button.png').convert_alpha()

    przycisk_png = pygame.Surface((40, 40))
    przycisk_ciemny_png = pygame.Surface((40, 40))
    font = pygame.font.SysFont(None, 48)

    przycisk_png.fill((0, 200, 100)) # Kolor zielony
    przycisk_ciemny_png.fill((0, 255, 40))
    
    #przycisk = Button(10, 10, przycisk_png, przycisk_ciemny_png)
    buttons_list = []
    rows = 8
    columns = 5
    number_of_mines = 5
    mines_on_tab = 0
    tab = []
    
    def mainLoop(self):
    
        running = True
        while running:
             for event in pygame.event.get():
             
                 if event.type == pygame.QUIT:
                     
                     running = False
                     
             for button in self.buttons_list:
                
                button.check_event()
                
                     
             self.screen.fill((30, 30, 30))
                 
             for button in self.buttons_list:
                 button.draw()
                 
           
                 
             pygame.display.flip()
             pygame.time.wait(10)  # 10ms

    def CreateButtons(self):
    
        for i in range(self.columns):

            row = []

            for j in range(self.rows):
                
                new_button = Button(self, i, j, self.przycisk_png, self.przycisk_ciemny_png)
                self.buttons_list.append(new_button)
                row.append(new_button)

            self.tab.append(row)
    
    def InitializeRandom(self):
    
                    
        ##### USTAWIENIE POZYCJI MIN #################################

        while self.mines_on_tab < self.number_of_mines:
            #print(self.mines_on_tab, self.number_of_mines)
            ran_i = random.randint(0, self.columns-1)
            ran_j = random.randint(0, self.rows-1)
            
            if self.tab[ran_i][ran_j].is_mine == False:
                self.tab[ran_i][ran_j].is_mine = True
                self.mines_on_tab += 1
            
    def CountMines(self):
    
        ###### PRZYPISANIE NUMERÓW W TABLICY #########################

        for button in self.buttons_list:
                
                for di, dj in deltas():
                    ni, nj = button.i + di, button.j + dj
                    # Sprawdzamy czy sąsiad istnieje i czy jest miną
                    if 0 <= ni < self.columns and 0 <= nj < self.rows:
                        if self.tab[ni][nj].is_mine:
                            button.mines_around += 1 
                            
    def Dfs(self, x, y):
    
        #print(f'dfs: {x} {y}')
        
        #czy nie wychodzimy poza zakres tablicy 
        if x < 0 or x >= self.columns or y < 0 or y >= self.rows:
        
            #print("wyjechalo")
            return
            
        #czy jest mina   
        if self.tab[x][y].is_mine == True:
        
            #print("mina")
            return
         
        #czy już jest odsłonięte   
        if self.tab[x][y].is_visited:
        
            #print("bylo")
            
            return
        
        
        self.tab[x][y].is_visited = True

        if self.tab[x][y].mines_around == 0:
            for dx, dy in deltas():
                # Wywołujemy rekurencyjnie dla sąsiadów
                self.Dfs(x + dx, y + dy)
                
                
    def FirstClick(self, i, j):
    
        if self.first_click:
            return
            
        self.first_click = True
    
        if self.tab[i][j].is_mine:
                
                    ran_i = random.randint(0, self.columns-1)
                    ran_j = random.randint(0, self.rows-1)

                    while (( ran_i == i and ran_j == j ) or self.tab[ran_i][ran_j].is_mine):
                        ran_i = random.randint(0, self.game.columns-1)
                        ran_j = random.randint(0, rows-1)
                    
                    
                    self.is_mine = False
                    self.tab[ran_i][ran_j].is_mine = True

        self.CountMines()
               
game = Game()
game.CreateButtons()
game.InitializeRandom()
###### GŁÓWNA PĘTLA GRY ####################################
game.mainLoop()

             
pygame.quit()
