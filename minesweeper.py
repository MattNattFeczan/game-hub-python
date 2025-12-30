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

    def __init__(self, game, i, j, image_normal, image_flag, image_question, image_v, image_kabum):
    
        self.game = game
        self.i = i
        self.j = j
    
        self.x = 50 + (i*50)
        self.y = 50 + (j*50)
        self.image_v = image_v
        self.image = image_normal
        self.image_flag = image_flag
        self.image_question = image_question
        self.image_kabum = image_kabum
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.clicked = False
        self.is_mine = False
        self.mines_around = 0
        self.mines_around_flagged = 0
        self.is_visited = False
        self.is_flagged = False
        self.is_question_mark = False
        self.is_kabum = False
        self.mines_around = 0
        
    
    def draw(self):
    
        self.game.screen.blit(self.image, (self.rect.x, self.rect.y))
        
        
        if self.is_kabum:
        
            self.game.screen.blit(self.image_kabum, (self.rect.x, self.rect.y))
        
        elif self.is_visited:
        
            self.game.screen.blit(self.image_v, (self.rect.x, self.rect.y))
            text = self.game.font.render(str(self.mines_around), True, (0, 0, 0))
            self.game.screen.blit(text, (self.rect.x, self.rect.y))
            
            
        elif self.is_question_mark:
        
            self.game.screen.blit(self.image_question, (self.rect.x, self.rect.y))
            #text = self.game.font.render(str("?"), True, (0, 0, 0))
            #self.game.screen.blit(text, (self.rect.x, self.rect.y))
            
        elif self.is_flagged:
        
            self.game.screen.blit(self.image_flag, (self.rect.x, self.rect.y))
            #text = self.game.font.render(str("-1"), True, (0, 0, 0))
            #self.game.screen.blit(text, (self.rect.x, self.rect.y))
            
            
        
        
    def check_event(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
        
        
            if pygame.mouse.get_pressed()[0] and self.is_visited:
                
                count_mines = 0;
                
                delta = deltas()
                
                for dx, dy in delta:
                
                    if 0 <= self.i+dx < self.game.columns and 0 <= self.j + dy < self.game.rows:
                        if self.game.tab[self.i+dx][self.j+dy].is_flagged:
                            count_mines+=1    
                        
                self.mines_around_flagged = count_mines
                        
                if count_mines == self.mines_around:
                    
                    #tutaj dfs
                    
                    self.is_visited = False
                    
                    print("aaa")
                    
                    self.game.Dfs(self.i, self.j)
            
            # --- LEWY PRZYCISK (Odkrywanie) ---
            # Dodajemy warunek: nie można odkryć, jeśli jest flaga! (zasada sapera)
            elif pygame.mouse.get_pressed()[0] == 1 and not self.clicked and not self.is_flagged:
                self.clicked = True
                self.is_question_mark = False # Kasujemy znak zapytania przy odkryciu
                
                self.game.FirstClick(self.i, self.j)
                self.game.Dfs(self.i, self.j)

            # --- PRAWY PRZYCISK (Flagowanie) ---
            # Ważne: To zadziała poprawnie tylko jeśli używasz events (MOUSEBUTTONDOWN)
            # Jeśli używasz get_pressed(), to będzie "mrugać" i zmieniać się bardzo szybko.
            elif pygame.mouse.get_pressed()[2] and not self.is_visited: # Używamy ELIF żeby nie klikać obu naraz
                
                # Tworzymy cykl: Puste -> Flaga -> Znak zapytania -> Puste
                
                if not self.is_flagged and not self.is_question_mark:
                    # Stan 1: Było puste -> Robimy Flagę
                    self.is_flagged = True
                    self.is_question_mark = False
                    
                elif self.is_flagged:
                    # Stan 2: Była Flaga -> Robimy Znak zapytania
                    self.is_flagged = False
                    self.is_question_mark = True
                    
                elif self.is_question_mark:
                    # Stan 3: Był Znak -> Czyścimy wszystko
                    self.is_flagged = False
                    self.is_question_mark = False
                
                # Tutaj przydałoby się małe opóźnienie (sleep) albo flaga blokująca,
                # bo get_pressed() wykona to 10 razy w ciągu jednego kliknięcia.
                pygame.time.delay(150) # BRZYDKI SPOSÓB, ale zadziała "na szybko"
                
                    
                    
            elif pygame.mouse.get_pressed()[0] and not self.is_flagged and self.is_mine:
                
                self.is_kabum = True
                        

class Game():

    first_click = False
    SCREEN_HEIGHT = 1000
    SCREEN_WIDTH = 1000

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT));

    #pygame.image.load().convert_alpha()

    #button class

    przycisk_png = pygame.image.load('pixil-frame-0.png').convert_alpha()
    flaga_png = pygame.image.load('pixil-frame-0(2).png').convert_alpha()
    question_png = pygame.image.load('pixil-frame-0(1).png').convert_alpha()
    kabum_png = pygame.image.load('pixil-frame-0(4).png').convert_alpha()
    
    #przycisk_png = pygame.Surface((40, 40))
    
    font = pygame.font.SysFont(None, 48)
    przycisk_v = pygame.Surface((40, 40))

    
    przycisk_v.fill((200, 200, 200))
    
    #przycisk = Button(10, 10, przycisk_png, przycisk_ciemny_png)
    buttons_list = []
    rows = 16
    columns = 16
    number_of_mines = 40
    mines_on_tab = 0
    tab = []
    
    przegrana = False
    
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
                
                new_button = Button(self, i, j, self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png)
                self.buttons_list.append(new_button)
                row.append(new_button)

            self.tab.append(row)
    
    def InitializeRandom(self, i, j):
    
                    
        ##### USTAWIENIE POZYCJI MIN #################################

        while self.mines_on_tab < self.number_of_mines:
            #print(self.mines_on_tab, self.number_of_mines)
            ran_i = random.randint(0, self.columns-1)
            ran_j = random.randint(0, self.rows-1)
            
            deltas_temp = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1), (0, 0))
            # Sprawdzamy, czy wylosowane pole koliduje z którymkolwiek przesunięciem
            
            is_forbidden = any(ran_i == i + dx and ran_j == j + dy for dx, dy in deltas_temp)

            if not is_forbidden:
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
    
        if not self.przegrana:
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

            if self.tab[x][y].mines_around == 0 or self.tab[x][y].mines_around == self.tab[x][y].mines_around_flagged:
                for dx, dy in deltas():
                    # Wywołujemy rekurencyjnie dla sąsiadów
                    if self.tab[x][y].is_flagged and not self.tab[x][y].is_mine:
                        self.przegrana = True
                        print("Aaaaa")
                        
                    elif not self.tab[x][y].is_mine:
                        self.Dfs(x + dx, y + dy)
                    
                        
        else:
            print("xd")            
                
    def FirstClick(self, i, j):
    
        if self.first_click:
            return
            
        self.first_click = True
    
        self.InitializeRandom(i, j)

        self.CountMines()
               
game = Game()
game.CreateButtons()
###### GŁÓWNA PĘTLA GRY ####################################
game.mainLoop()

             
pygame.quit()
