import pygame
import random
import sys

pygame.init()

# Gra zawiera 4 typy rozgrywki:

    #Początkujący – plansza 8×8 pól, 10 min
    #Zaawansowany – plansza 16×16 pól, 40 min
    #Ekspert – plansza 16×24 pól, 70 min
    
def deltas():
  return ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

class Button():

    def __init__(self, game, i, j, image_normal, image_flag, image_question, image_v, image_kabum, image_mine, image_blank, image_check, image_start, image_change, image_easy, image_medium, image_hard, image_easy_pointed, image_medium_pointed, image_hard_pointed, image_exit, image_exit_main, width=40, height=40, override_x=None, override_y=None):
    
        self.game = game
        self.i = i
        self.j = j
        
        if override_x is not None and override_y is not None:
            self.x = override_x
            self.y = override_y
            #dla przycisku check,start,change
        else:
            
            self.x = self.game.start_x + (i * (self.game.cell_size+10))
            self.y = self.game.start_y + (j * (self.game.cell_size+10))
            

        self.image_v = image_v
        self.image_blank = image_blank
        self.image = image_normal
        self.image_flag = image_flag
        self.image_question = image_question
        self.image_kabum = image_kabum
        self.image_mine = image_mine
        self.image_check = image_check
        self.image_start = image_start
        self.image_change = image_change
        self.image_easy = image_easy
        self.image_medium = image_medium
        self.image_hard = image_hard
        self.image_easy_pointed = image_easy_pointed
        self.image_medium_pointed = image_medium_pointed
        self.image_hard_pointed = image_hard_pointed
        self.image_exit = image_exit
        self.image_exit_main = image_exit_main
        
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.clicked = False
        self.is_mine = False
        self.mines_around = 0
        self.mines_around_flagged = 0
        self.is_visited = False
        self.is_flagged = False
        self.is_question_mark = False
        self.is_kabum = False
        self.mines_around = 0
        self.is_check = False
        self.is_start = False
        self.is_change = False
        self.is_easy = False
        self.is_medium = False
        self.is_hard = False
        self.is_exit = False
        self.is_exit_main = False
        
    
    def draw(self):
    
        if self.is_start:
        
            self.game.screen.blit(self.image_start, (self.rect.x, self.rect.y))
            
        elif self.is_change:
        
            self.game.screen.blit(self.image_change, (self.rect.x, self.rect.y))
            
        elif self.is_exit:
        
            self.game.screen.blit(self.image_exit, (self.rect.x, self.rect.y))
            
        elif self.is_exit_main:
        
            self.game.screen.blit(self.image_exit_main, (self.rect.x, self.rect.y))
            
        elif self.is_easy:
        
            if not self.game.is_easy_pointed:
                
                self.game.screen.blit(self.image_easy, (self.rect.x, self.rect.y))
                
            else:
                
                self.game.screen.blit(self.image_easy_pointed, (self.rect.x, self.rect.y))
            
        elif self.is_medium:
        
            if not self.game.is_medium_pointed:
                
                self.game.screen.blit(self.image_medium, (self.rect.x, self.rect.y))
                
            else:
                
                self.game.screen.blit(self.image_medium_pointed, (self.rect.x, self.rect.y))
            
        elif self.is_hard:
        
            if not self.game.is_hard_pointed:
                
                self.game.screen.blit(self.image_hard, (self.rect.x, self.rect.y))
                
            else:
                
                self.game.screen.blit(self.image_hard_pointed, (self.rect.x, self.rect.y))
            
            
        
        
            
    
        else:
        
            self.game.screen.blit(self.image, (self.rect.x, self.rect.y))
            
            
            if self.is_kabum:
            
                self.game.screen.blit(self.image_kabum, (self.rect.x, self.rect.y))
            
            elif self.is_visited:
            
                if self.mines_around!=0:
                    self.game.screen.blit(self.image_v, (self.rect.x, self.rect.y))
                    text = self.game.font.render(str(self.mines_around), True, (0, 0, 0))
                    self.game.screen.blit(text, (self.rect.x+8, self.rect.y+3))
                    
                else:
                    self.game.screen.blit(self.image_blank, (self.rect.x, self.rect.y))
                
                
            elif self.is_question_mark:
            
                self.game.screen.blit(self.image_question, (self.rect.x, self.rect.y))
                #text = self.game.font.render(str("?"), True, (0, 0, 0))
                #self.game.screen.blit(text, (self.rect.x, self.rect.y))
                
            elif self.is_flagged:
            
                self.game.screen.blit(self.image_flag, (self.rect.x, self.rect.y))
                #text = self.game.font.render(str("-1"), True, (0, 0, 0))
                #self.game.screen.blit(text, (self.rect.x, self.rect.y))
                
            elif self.is_mine and self.game.przegrana and not self.is_kabum:
                
                self.game.screen.blit(self.image_v, (self.rect.x, self.rect.y))
                self.game.screen.blit(self.image_mine, (self.rect.x, self.rect.y))
                
                
            elif self.is_check:
            
                self.game.screen.blit(self.image_check, (self.rect.x, self.rect.y))
                
            #tutaj dla przyciskow na poczatku
            
            
                
            
        
        
    def check_event(self):
    
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
        
            if pygame.mouse.get_pressed()[0] and self.is_check:
            
                #print("sprawdz")
                
                self.game.Check()
                
            elif pygame.mouse.get_pressed()[0] and self.is_easy:
            
                self.game.is_easy_pointed = True
                self.game.is_medium_pointed = False
                self.game.is_hard_pointed = False
                
            elif pygame.mouse.get_pressed()[0] and self.is_medium:
            
                self.game.is_easy_pointed = False
                self.game.is_medium_pointed = True
                self.game.is_hard_pointed = False
               
            elif pygame.mouse.get_pressed()[0] and self.is_hard:
            
                self.game.is_easy_pointed = False
                self.game.is_medium_pointed = False
                self.game.is_hard_pointed = True
            
            # tutaj dla innych przyciskow w menu
            
            elif pygame.mouse.get_pressed()[0] and self.is_start:
            
                self.game.update_settings()
                
                self.game.CreateButtons()
                
                while pygame.mouse.get_pressed()[0]:
                    pygame.event.pump()
            
                self.game.beggining_of_the_game = False
                
            #elif pygame.mouse.get_pressed()[0] and self.is_change:
            
            elif pygame.mouse.get_pressed()[0] and self.is_change:
            
                self.game.changing_difficulty = True
                
                self.game.beggining_of_the_game = False
                
            elif pygame.mouse.get_pressed()[0] and self.is_exit:
            
                self.game.beggining_of_the_game = True
                self.game.changing_difficulty = False
                self.game.back_to_menu()
                
            elif pygame.mouse.get_pressed()[0] and self.is_exit_main:
            
                self.game.running = False
                
        
        
            elif pygame.mouse.get_pressed()[0] and self.is_visited:
                
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
                    
                   # print("aaa")
                    
                    self.game.Dfs(self.i, self.j)
            
            # --- LEWY PRZYCISK (Odkrywanie) ---
            # Dodajemy warunek: nie można odkryć, jeśli jest flaga! (zasada sapera)
            elif pygame.mouse.get_pressed()[0] == 1 and not self.clicked and not self.is_flagged and not self.is_change and not self.is_start:
            
                self.clicked = True
                self.is_question_mark = False # Kasujemy znak zapytania przy odkryciu
                
                self.game.FirstClick(self.i, self.j)
                self.game.Dfs(self.i, self.j)

            # --- PRAWY PRZYCISK (Flagowanie) ---
            # Ważne: To zadziała poprawnie tylko jeśli używasz events (MOUSEBUTTONDOWN)
            # Jeśli używasz get_pressed(), to będzie "mrugać" i zmieniać się bardzo szybko.
            elif pygame.mouse.get_pressed()[2] and not self.is_visited and not self.is_check: # Używamy ELIF żeby nie klikać obu naraz
                
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
                pygame.time.delay(150)
                
                    
                    
            elif pygame.mouse.get_pressed()[0] and not self.is_flagged and self.is_mine:
                
                self.is_kabum = True
                self.game.przegrana = True


class Game():

    first_click = False
    #SCREEN_HEIGHT = 900
    #SCREEN_WIDTH = 900
    
    info = pygame.display.Info()
    
    SCREEN_WIDTH = info.current_w
    SCREEN_HEIGHT = info.current_h

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE);

    #pygame.image.load().convert_alpha()

    #button class

    przycisk_png = pygame.image.load('pixil-frame-0.png').convert_alpha()
    flaga_png = pygame.image.load('pixil-frame-0(2).png').convert_alpha()
    question_png = pygame.image.load('pixil-frame-0(1).png').convert_alpha()
    kabum_png = pygame.image.load('pixil-frame-0(4).png').convert_alpha()
    mine_png = pygame.image.load('pixil-frame-0(3).png').convert_alpha()
    check_png = pygame.image.load('pixil-frame-0(6).png').convert_alpha()
    start_png = pygame.image.load('pixil-frame-0(8).png').convert_alpha()
    change_dif_png = pygame.image.load('pixil-frame-0(7).png').convert_alpha()
    exit_png = pygame.image.load('pixil-frame-0(26).png').convert_alpha()
    
    minesweeper_png = pygame.image.load('pixil-frame-0(10).png').convert_alpha()
    chosen_difficulty_png = pygame.image.load('pixil-frame-0(24).png').convert_alpha()
    
    easy_png = pygame.image.load('pixil-frame-0(16).png').convert_alpha()
    medium_png = pygame.image.load('pixil-frame-0(20).png').convert_alpha()
    hard_png = pygame.image.load('pixil-frame-0(18).png').convert_alpha()
    
    easy_pointed_png = pygame.image.load('pixil-frame-0(17).png').convert_alpha()
    medium_pointed_png = pygame.image.load('pixil-frame-0(21).png').convert_alpha()
    hard_pointed_png = pygame.image.load('pixil-frame-0(19).png').convert_alpha()
    
    easy_numbers_png = pygame.image.load('pixil-frame-0(30).png').convert_alpha()
    medium_numbers_png = pygame.image.load('pixil-frame-0(29).png').convert_alpha()
    hard_numbers_png = pygame.image.load('pixil-frame-0(28).png').convert_alpha()
    
    you_won_png = pygame.image.load('pixil-frame-0(31).png').convert_alpha()
    you_lost_png = pygame.image.load('pixil-frame-0(32).png').convert_alpha()
    
    exit_main_png = pygame.image.load('pixil-frame-0(34).png').convert_alpha()
    
    font = pygame.font.SysFont(None, 48)
    przycisk_v = pygame.Surface((40, 40))
    przycisk_blank = pygame.Surface((40,40))

    
    przycisk_v.fill((200, 200, 200))
    przycisk_blank.fill((140, 170, 180))
    
    def __init__(self):
    
        # Inicjalizacja zmiennych dla tej konkretnej gry
        
        
        self.rows = 8
        self.columns = 8
        
        self.number_of_mines = 10
        
        self.beggining_of_the_game = True
        self.changing_difficulty = False
        self.buttons_list = []
        self.tab = []
        self.cell_size = 40 
        self.gap = 10 #odstęp między przyciskami
        self.board_pixel_width = self.columns * (self.cell_size + 2*self.gap) #ile zajmuje miejsca przycisk wraz z odstępem
        self.board_pixel_height = self.rows * (self.cell_size + 2*self.gap)
        self.start_x = (self.SCREEN_WIDTH - self.board_pixel_width) // 2 #gdzie zacząć tworzenie planszy (wsp. x)
        self.start_y = (self.SCREEN_HEIGHT - self.board_pixel_height) // 2 #gdzie zacząć tworzenie planszy (wsp. y)
        self.mines_on_tab = 0
        self.przegrana = False
        self.button_check_width = 160
        self.button_check_height = 80
        self.button_start_width = 320
        self.button_start_height = 160
        self.button_change_width = 320
        self.button_change_height = 160
        self.button_difficulty_width = 200
        self.button_difficulty_height = 120
        self.button_difficulty_medium_width = 300
        self.button_exit_height = 200
        self.button_exit_width = 200
        self.button_exit_main_height = 350
        self.button_exit_main_width = 200
        
        self.is_easy_pointed = True
        self.is_medium_pointed = False
        self.is_hard_pointed = False
        
        self.is_win = False
        self.is_lost = False
        
        #self.difficulty = 0 # easy - 0, medium - 1, hard - 2
        
        self.button_check = Button(
            self, 0, 0, 
            self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png,
            width=self.button_check_width,       # Nowa szerokość
            height=self.button_check_height,       # Nowa wysokość
            override_x = self.SCREEN_WIDTH//2 + self.board_pixel_width//2.5,  # Dokładna pozycja X w oknie
            override_y = (self.SCREEN_HEIGHT - self.button_check_height)//2    # Dokładna pozycja Y w oknie
        )
        
        self.button_start = Button(
            self, 0, 0,
            self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png,
            width=self.button_start_width,       # Nowa szerokość
            height=self.button_start_height,       # Nowa wysokość
            override_x = (self.SCREEN_WIDTH - self.button_start_width)//2,  # Dokładna pozycja X w oknie
            override_y = (self.SCREEN_HEIGHT - self.button_start_height)//2 + 1.8*self.button_change_height   # Dokładna pozycja Y w oknie
        )
        
        self.button_change = Button(
            self, 0, 0,
            self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png,
            width=self.button_change_width,       # Nowa szerokość
            height=self.button_change_height,       # Nowa wysokość
            override_x = (self.SCREEN_WIDTH - self.button_change_width)//2,  # Dokładna pozycja X w oknie
            override_y = (self.SCREEN_HEIGHT - self.button_change_height)//2  # Dokładna pozycja Y w oknie
        )
        
        self.button_easy = Button(
            self, 0, 0,
            self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png,
            width=self.button_change_width,       # Nowa szerokość
            height=self.button_change_height,       # Nowa wysokość
            override_x = self.button_difficulty_width,  # Dokładna pozycja X w oknie
            override_y = self.button_difficulty_height*2  # Dokładna pozycja Y w oknie
        )
        
        self.button_medium = Button(
            self, 0, 0,
            self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png,
            width=self.button_change_width,       # Nowa szerokość
            height=self.button_change_height,       # Nowa wysokość
            override_x = (self.button_difficulty_width + self.button_difficulty_medium_width)//2 + self.button_difficulty_width*2.6,
            override_y = self.button_difficulty_height*2
        )
        
        self.button_hard = Button(
            self, 0, 0,
            self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png,
            width=self.button_change_width,       # Nowa szerokość
            height=self.button_change_height,       # Nowa wysokość
            override_x = self.button_difficulty_width*5.6 + (self.button_difficulty_width + self.button_difficulty_medium_width)//2,
            override_y = self.button_difficulty_height*2
        )
        
        #tutaj jest przycisk do menu sapera
        self.button_exit = Button(
            self, 0, 0, 
            self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png,
            width=self.button_exit_width,       # Nowa szerokość
            height=self.button_exit_height,       # Nowa wysokość
            override_x = self.SCREEN_WIDTH - 2*self.button_exit_width,  # Dokładna pozycja X w oknie
            override_y = self.SCREEN_HEIGHT - 2*self.button_exit_height    # Dokładna pozycja Y w oknie
        )
        
        #tutaj jest przycisk do menu głównego
        self.button_exit_main = Button(
            self, 0, 0, 
            self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png,
            width=self.button_exit_main_width,
            height=self.button_exit_main_height,
            override_x = self.SCREEN_WIDTH - 2.5*self.button_exit_main_width,
            override_y = self.SCREEN_HEIGHT - self.button_exit_main_height
        )
        
        self.button_check.is_check = True
        self.button_start.is_start = True
        self.button_change.is_change = True
        self.button_easy.is_easy = True
        self.button_medium.is_medium = True
        self.button_hard.is_hard = True
        self.button_exit.is_exit = True
        self.button_exit_main.is_exit_main = True
        
    
    def mainLoop(self):
    
        self.running = True
        
        while self.running:
        
            if self.beggining_of_the_game:
            
                for event in pygame.event.get():
                 
                   if event.type == pygame.QUIT:
                         
                         self.running = False
                         
                self.screen.fill((30, 30, 30))
                
                self.screen.blit(self.minesweeper_png, (self.SCREEN_WIDTH/4.4, 0))
                
                self.button_start.draw()
                
                self.button_start.check_event()
                
                self.button_change.draw()
                
                self.button_change.check_event()
                
                self.button_exit_main.draw()
                
                self.button_exit_main.check_event()
                
                
            elif self.changing_difficulty:
            
                for event in pygame.event.get():
                 
                   if event.type == pygame.QUIT:
                         
                         self.running = False
                         
                self.screen.fill((30, 30, 30))
                
                self.screen.blit(self.chosen_difficulty_png, (self.SCREEN_WIDTH/4.6, self.SCREEN_HEIGHT/2))
                
                if self.is_easy_pointed:
                
                    self.screen.blit(self.easy_numbers_png, (self.SCREEN_WIDTH/4, self.SCREEN_HEIGHT/1.4))
                    
                if self.is_medium_pointed:
                
                    self.screen.blit(self.medium_numbers_png, (self.SCREEN_WIDTH/4, self.SCREEN_HEIGHT/1.4))
                    
                if self.is_hard_pointed:
                
                    self.screen.blit(self.hard_numbers_png, (self.SCREEN_WIDTH/4, self.SCREEN_HEIGHT/1.4))
                    
                
                self.button_easy.draw()
                
                self.button_easy.check_event()
                
                self.button_medium.draw()
                
                self.button_medium.check_event()
                
                self.button_hard.draw()
                
                self.button_hard.check_event()
                
                self.button_exit.draw() 
                
                self.button_exit.check_event()               
        
            elif not self.przegrana:
        
                for event in pygame.event.get():
                 
                   if event.type == pygame.QUIT:
                         
                         self.running = False
                         
                for button in self.buttons_list:
                    
                   button.check_event()
                    
                         
                self.screen.fill((30, 30, 30))
                     
                for button in self.buttons_list:
                
                    button.draw()
                    
                self.button_check.draw()
                
                self.button_check.check_event()
                
                if self.is_win:
                
                    self.button_exit.draw()
                    self.button_exit.check_event()
                    self.screen.blit(self.you_won_png, (self.SCREEN_WIDTH/4.4, 0))
                    
            else:
             
                for event in pygame.event.get():
                 
                   if event.type == pygame.QUIT:
                         
                         self.running = False
                         
                self.Reveal()
                
                self.button_exit.draw()
                self.button_exit.check_event()
                self.screen.blit(self.you_lost_png, (self.SCREEN_WIDTH/4.4, 0))
                
                         
                #print("koniec")
                 
            pygame.display.flip()
            pygame.time.wait(10)  # 10ms

    def CreateButtons(self):
    
        for i in range(self.columns):

            row = []

            for j in range(self.rows):
                
                new_button = Button(self, i, j, self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png, width=40, height=40, override_x=None, override_y=None)
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
                
            if self.tab[x][y].is_flagged:
                return
                  
            if self.tab[x][y].is_mine == True:
            
                if not self.przegrana: # Żeby nie zapętlić wybuchów
                    self.przegrana = True
                    self.tab[x][y].is_visited = True
                    self.tab[x][y].is_kabum = True  
            
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
                        
                    if not self.tab[x][y].is_mine:
                        self.Dfs(x + dx, y + dy)
                    
                        
        else:
            print("xd")            
                
    def FirstClick(self, i, j):
    
        if self.first_click:
            return
            
        self.first_click = True
    
        self.InitializeRandom(i, j)

        self.CountMines()
        
    def Reveal(self):
    
        for button in self.buttons_list:
            #print("AAAA")
            button.draw()
            
    def Check(self):
    
        count_flags = 0
    
        for button in self.buttons_list:
        
            if button.is_flagged:
                
                count_flags+=1
            
        #print(count_flags)
    
        if count_flags == self.number_of_mines:
        
            #print(count_flags)
        
            for button in self.buttons_list:
            
                if button.is_mine and not button.is_flagged:
                
                    print("źle")
                    
                    self.przegrana = True
                    
                    self.Reveal()
                    
            if not self.przegrana:
            
                #print("dobrze!")
                
                self.is_win = True
                
                #przełącz na stronę z wygraną i owrotem do początku gry
                
                
    def update_settings(self):
        # Sprawdzamy, ktory poziom jest "pointed" (wybrany) i ustawiamy dane
        if self.is_easy_pointed:
            self.rows = 8
            self.columns = 8
            self.number_of_mines = 10
        elif self.is_medium_pointed:
            self.rows = 16
            self.columns = 16
            self.number_of_mines = 40
        elif self.is_hard_pointed:
            self.rows = 16
            self.columns = 24
            self.number_of_mines = 78

        # WAŻNE: Musimy przeliczyć rozmiar planszy i jej pozycję na ekranie!
        self.board_pixel_width = self.columns * (self.cell_size + 2*self.gap)
        self.board_pixel_height = self.rows * (self.cell_size + 2*self.gap)
        self.start_x = (self.SCREEN_WIDTH - self.board_pixel_width) // 2 
        self.start_y = (self.SCREEN_HEIGHT - self.board_pixel_height) // 2
        
        # Resetujemy listy przycisków, żeby stworzyć nowe dla nowej wielkości
        self.buttons_list = []
        self.tab = []
        self.mines_on_tab = 0
        
        
        # --- TUTAJ JEST NOWA POPRAWKA ---
        
        new_check_x = self.SCREEN_WIDTH // 2 + self.board_pixel_width // 2.5

        new_check_y = self.start_y + self.board_pixel_height/2
        
        # Przypisujemy nowe wartości do obiektu przycisku
        self.button_check.rect.x = new_check_x
        self.button_check.rect.y = new_check_y
        
        # Aktualizujemy też atrybuty x i y w samym obiekcie (dla porządku, choć draw korzysta z rect)
        self.button_check.x = new_check_x
        self.button_check.y = new_check_y
        
        
    def reset_game(self):
        # 1. Resetujemy flagi logiczne gry
        self.przegrana = False
        self.first_click = False  # Ważne: dzięki temu miny wylosują się na nowo!
        self.mines_on_tab = 0
        
        # 2. Czyścimy listy (tablica logiczna i lista obiektów przycisków)
        self.tab = []
        self.buttons_list = []
        
        # 3. Tworzymy nowe, czyste przyciski
        # (korzysta z aktualnych wymiarów rows/columns ustawionych w update_settings)
        self.CreateButtons()
        
        # 4. Resetujemy stan przycisku buźki/check (opcjonalne, dla porządku)
        self.button_check.is_kabum = False
        self.button_check.is_mine = False
        
        print("Gra zresetowana!")
        
        
        
    def back_to_menu(self):
        # Resetujemy flagi
        self.przegrana = False
        self.first_click = False
        self.mines_on_tab = 0
        self.tab = []
        self.buttons_list = []
        
        # Kluczowe: Przełączamy stan, żeby pętla while wyświetliła menu
        self.beggining_of_the_game = True
        self.changing_difficulty = False
                    
            
                
# --- KONIEC KLASY GAME ---

def launch():
    """Funkcja startowa dla Menu"""
    game = Game()
    game.mainLoop()

if __name__ == "__main__":
    launch()
    pygame.quit() 
