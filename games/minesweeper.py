import pygame
import random
import sys

# Gra zawiera 4 typy rozgrywki:
# Początkujący – plansza 8×8 pól, 10 min
# Zaawansowany – plansza 16×16 pól, 40 min
# Ekspert – plansza 16×24 pól, 70 min

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
        else:
            self.x = self.game.start_x + (i * (self.game.cell_size + self.game.gap))
            self.y = self.game.start_y + (j * (self.game.cell_size + self.game.gap))

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
            
                if self.mines_around != 0:
                
                    self.game.screen.blit(self.image_v, (self.rect.x, self.rect.y))
                    
                    if self.game.cell_size < 30:
                        text = self.game.small_font.render(str(self.mines_around), True, (0, 0, 0))
                        self.game.screen.blit(text, (self.rect.x + 8, self.rect.y + 3))
                    else:
                        text = self.game.font.render(str(self.mines_around), True, (0, 0, 0))
                        self.game.screen.blit(text, (self.rect.x + 8, self.rect.y + 3))
                        
                else:
                    self.game.screen.blit(self.image_blank, (self.rect.x, self.rect.y))
                    
            elif self.is_question_mark:
                self.game.screen.blit(self.image_question, (self.rect.x, self.rect.y))
                
            elif self.is_flagged:
                self.game.screen.blit(self.image_flag, (self.rect.x, self.rect.y))
                
            elif self.is_mine and self.game.przegrana and not self.is_kabum:
                self.game.screen.blit(self.image_v, (self.rect.x, self.rect.y))
                self.game.screen.blit(self.image_mine, (self.rect.x, self.rect.y))
                
            elif self.is_check:
                self.game.screen.blit(self.image_check, (self.rect.x, self.rect.y))

    def check_event(self):
    
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.is_check:
                self.game.Check()
                pygame.time.delay(150)
                
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
            
            elif pygame.mouse.get_pressed()[0] and self.is_start:
                self.game.update_settings()
                self.game.CreateButtons()
                while pygame.mouse.get_pressed()[0]:
                    pygame.event.pump()
                self.game.beggining_of_the_game = False
                
            elif pygame.mouse.get_pressed()[0] and self.is_change:
                self.game.changing_difficulty = True
                self.game.beggining_of_the_game = False
                
            elif pygame.mouse.get_pressed()[0] and self.is_exit:
                self.game.beggining_of_the_game = True
                self.game.changing_difficulty = False
                self.game.back_to_menu()
                while pygame.mouse.get_pressed()[0]:
                    pygame.event.pump()
                
            elif pygame.mouse.get_pressed()[0] and self.is_exit_main:
                self.game.running = False 
                
            elif pygame.mouse.get_pressed()[0] and self.is_visited:
                count_mines = 0
                delta = deltas()
                for dx, dy in delta:
                    if 0 <= self.i+dx < self.game.columns and 0 <= self.j + dy < self.game.rows:
                        if self.game.tab[self.i+dx][self.j+dy].is_flagged:
                            count_mines+=1    
                self.mines_around_flagged = count_mines
                if count_mines == self.mines_around:
                    self.is_visited = False
                    self.game.Dfs(self.i, self.j)
            
            elif pygame.mouse.get_pressed()[0] == 1 and not self.clicked and not self.is_flagged and not self.is_change and not self.is_start:
                self.clicked = True
                self.is_question_mark = False
                self.game.FirstClick(self.i, self.j)
                self.game.Dfs(self.i, self.j)

            elif pygame.mouse.get_pressed()[2] and not self.is_visited and not self.is_check:
                if not self.is_flagged and not self.is_question_mark:
                    self.is_flagged = True
                    self.is_question_mark = False
                elif self.is_flagged:
                    self.is_flagged = False
                    self.is_question_mark = True
                elif self.is_question_mark:
                    self.is_flagged = False
                    self.is_question_mark = False
                pygame.time.delay(150)
                    
            elif pygame.mouse.get_pressed()[0] and not self.is_flagged and self.is_mine:
                self.is_kabum = True
                self.game.przegrana = True

class Game():
    first_click = False

    def __init__(self, screen=None):
        if screen:
            self.screen = screen
            self.SCREEN_WIDTH = screen.get_width()
            self.SCREEN_HEIGHT = screen.get_height()
        else:
            pygame.init()
            self.SCREEN_WIDTH = 800
            self.SCREEN_HEIGHT = 600
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        #WYMIARY DLA ROZDZIELCZOŚCI 800x600
        self.cell_size = 25  
        self.gap = 1         
        
        self.button_check_width = 80
        self.button_check_height = 40
        self.button_start_width = 200
        self.button_start_height = 80
        self.button_change_width = 200
        self.button_change_height = 80
        self.button_difficulty_width = 120
        self.button_difficulty_height = 60
        self.button_exit_width = 100
        self.button_exit_height = 80
        self.button_exit_main_width = 100
        self.button_exit_main_height = 50

        #ładowanie grafik w zależności skąd uruchomiony 
        try:
            self.przycisk_png = pygame.image.load('assets/images/pixil-frame-0.png').convert_alpha()
            self.flaga_png = pygame.image.load('assets/images/pixil-frame-0(2).png').convert_alpha()
            self.question_png = pygame.image.load('assets/images/pixil-frame-0(1).png').convert_alpha()
            self.kabum_png = pygame.image.load('assets/images/pixil-frame-0(4).png').convert_alpha()
            self.mine_png = pygame.image.load('assets/images/pixil-frame-0(3).png').convert_alpha()
            self.check_png = pygame.image.load('assets/images/pixil-frame-0(6).png').convert_alpha()
            self.start_png = pygame.image.load('assets/images/pixil-frame-0(8).png').convert_alpha()
            self.change_dif_png = pygame.image.load('assets/images/pixil-frame-0(7).png').convert_alpha()
            self.exit_png = pygame.image.load('assets/images/pixil-frame-0(26).png').convert_alpha()
            self.minesweeper_png = pygame.image.load('assets/images/pixil-frame-0(10).png').convert_alpha()
            self.chosen_difficulty_png = pygame.image.load('assets/images/pixil-frame-0(24).png').convert_alpha()
            self.easy_png = pygame.image.load('assets/images/pixil-frame-0(16).png').convert_alpha()
            self.medium_png = pygame.image.load('assets/images/pixil-frame-0(20).png').convert_alpha()
            self.hard_png = pygame.image.load('assets/images/pixil-frame-0(18).png').convert_alpha()
            self.easy_pointed_png = pygame.image.load('assets/images/pixil-frame-0(17).png').convert_alpha()
            self.medium_pointed_png = pygame.image.load('assets/images/pixil-frame-0(21).png').convert_alpha()
            self.hard_pointed_png = pygame.image.load('assets/images/pixil-frame-0(19).png').convert_alpha()
            self.easy_numbers_png = pygame.image.load('assets/images/pixil-frame-0(30).png').convert_alpha()
            self.medium_numbers_png = pygame.image.load('assets/images/pixil-frame-0(29).png').convert_alpha()
            self.hard_numbers_png = pygame.image.load('assets/images/pixil-frame-0(28).png').convert_alpha()
            self.you_won_png = pygame.image.load('assets/images/pixil-frame-0(31).png').convert_alpha()
            self.you_lost_png = pygame.image.load('assets/images/pixil-frame-0(32).png').convert_alpha()
            self.exit_main_png = pygame.image.load('assets/images/pixil-frame-0(34).png').convert_alpha()
            
        except FileNotFoundError:
        
            self.przycisk_png = pygame.image.load('../assets/images/pixil-frame-0.png').convert_alpha()
            self.flaga_png = pygame.image.load('../assets/images/pixil-frame-0(2).png').convert_alpha()
            self.question_png = pygame.image.load('../assets/images/pixil-frame-0(1).png').convert_alpha()
            self.kabum_png = pygame.image.load('../assets/images/pixil-frame-0(4).png').convert_alpha()
            self.mine_png = pygame.image.load('../assets/images/pixil-frame-0(3).png').convert_alpha()
            self.check_png = pygame.image.load('../assets/images/pixil-frame-0(6).png').convert_alpha()
            self.start_png = pygame.image.load('../assets/images/pixil-frame-0(8).png').convert_alpha()
            self.change_dif_png = pygame.image.load('../assets/images/pixil-frame-0(7).png').convert_alpha()
            self.exit_png = pygame.image.load('../assets/images/pixil-frame-0(26).png').convert_alpha()
            self.minesweeper_png = pygame.image.load('../assets/images/pixil-frame-0(10).png').convert_alpha()
            self.chosen_difficulty_png = pygame.image.load('../assets/images/pixil-frame-0(24).png').convert_alpha()
            self.easy_png = pygame.image.load('../assets/images/pixil-frame-0(16).png').convert_alpha()
            self.medium_png = pygame.image.load('../assets/images/pixil-frame-0(20).png').convert_alpha()
            self.hard_png = pygame.image.load('../assets/images/pixil-frame-0(18).png').convert_alpha()
            self.easy_pointed_png = pygame.image.load('../assets/images/pixil-frame-0(17).png').convert_alpha()
            self.medium_pointed_png = pygame.image.load('../assets/images/pixil-frame-0(21).png').convert_alpha()
            self.hard_pointed_png = pygame.image.load('../assets/images/pixil-frame-0(19).png').convert_alpha()
            self.easy_numbers_png = pygame.image.load('../assets/images/pixil-frame-0(30).png').convert_alpha()
            self.medium_numbers_png = pygame.image.load('../assets/images/pixil-frame-0(29).png').convert_alpha()
            self.hard_numbers_png = pygame.image.load('../assets/images/pixil-frame-0(28).png').convert_alpha()
            self.you_won_png = pygame.image.load('../assets/images/pixil-frame-0(31).png').convert_alpha()
            self.you_lost_png = pygame.image.load('../assets/images/pixil-frame-0(32).png').convert_alpha()
            self.exit_main_png = pygame.image.load('../assets/images/pixil-frame-0(34).png').convert_alpha()

        #### SKALOWANIE DO 800x600
        
        scale_size = (self.cell_size, self.cell_size)
        
        self.przycisk_png = pygame.transform.scale(self.przycisk_png, scale_size)
        self.flaga_png = pygame.transform.scale(self.flaga_png, scale_size)
        self.question_png = pygame.transform.scale(self.question_png, scale_size)
        self.kabum_png = pygame.transform.scale(self.kabum_png, scale_size)
        self.mine_png = pygame.transform.scale(self.mine_png, scale_size)
       
        self.start_png = pygame.transform.scale(self.start_png, (self.button_start_width, self.button_start_height))
        self.change_dif_png = pygame.transform.scale(self.change_dif_png, (self.button_change_width, self.button_change_height))
        
        self.check_png = pygame.transform.scale(self.check_png, (self.button_check_width, self.button_check_height))
        
        diff_size = (self.button_difficulty_width, self.button_difficulty_height)
        self.easy_png = pygame.transform.scale(self.easy_png, diff_size)
        self.medium_png = pygame.transform.scale(self.medium_png, diff_size)
        self.hard_png = pygame.transform.scale(self.hard_png, diff_size)
        self.easy_pointed_png = pygame.transform.scale(self.easy_pointed_png, diff_size)
        self.medium_pointed_png = pygame.transform.scale(self.medium_pointed_png, diff_size)
        self.hard_pointed_png = pygame.transform.scale(self.hard_pointed_png, diff_size)
        
        self.exit_png = pygame.transform.scale(self.exit_png, (self.button_exit_width, self.button_exit_height))
        self.exit_main_png = pygame.transform.scale(self.exit_main_png, (self.button_exit_main_width, self.button_exit_main_height))
        
        self.minesweeper_png = pygame.transform.scale(self.minesweeper_png, (400, 100)) # Logo tytułowe
        self.chosen_difficulty_png = pygame.transform.scale(self.chosen_difficulty_png, (400, 100))
        self.you_won_png = pygame.transform.scale(self.you_won_png, (400, 100))
        self.you_lost_png = pygame.transform.scale(self.you_lost_png, (400, 100))
        
        self.easy_numbers_png = pygame.transform.scale(self.easy_numbers_png, (300, 150))
        self.medium_numbers_png = pygame.transform.scale(self.medium_numbers_png, (300, 150))
        self.hard_numbers_png = pygame.transform.scale(self.hard_numbers_png, (300, 150))

        self.przycisk_v = pygame.Surface(scale_size)
        self.przycisk_blank = pygame.Surface(scale_size)
        self.przycisk_v.fill((200, 200, 200))
        self.przycisk_blank.fill((140, 170, 180))
        
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 24)
        
        self.rows = 8
        self.columns = 8
        self.number_of_mines = 10
        
        self.beggining_of_the_game = True
        self.changing_difficulty = False
        self.buttons_list = []
        self.tab = []
        
        ## ROZMIARY PLANSZY
        self.board_pixel_width = self.columns * (self.cell_size + self.gap)
        self.board_pixel_height = self.rows * (self.cell_size + self.gap)
        self.start_x = (self.SCREEN_WIDTH - self.board_pixel_width) // 2 
        self.start_y = (self.SCREEN_HEIGHT - self.board_pixel_height) // 2
        
        self.mines_on_tab = 0
        self.przegrana = False
        
        self.is_easy_pointed = True
        self.is_medium_pointed = False
        self.is_hard_pointed = False
        self.is_win = False
        self.is_lost = False


        self.button_check = Button(
            self, 0, 0, 
            self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png,
            width=self.button_check_width,
            height=self.button_check_height,
            override_x = (self.SCREEN_WIDTH - self.button_check_width) // 2, 
            override_y = 60
        )
        
        self.button_start = Button(
            self, 0, 0,
            self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png,
            width=self.button_start_width,
            height=self.button_start_height,
            override_x = (self.SCREEN_WIDTH - self.button_start_width) // 2,
            override_y = 200
        )
        
        self.button_change = Button(
            self, 0, 0,
            self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png,
            width=self.button_change_width,
            height=self.button_change_height,
            override_x = (self.SCREEN_WIDTH - self.button_change_width) // 2,
            override_y = 300
        )
        
        spacing = 20
        total_width = 3 * self.button_difficulty_width + 2 * spacing
        start_x_diff = (self.SCREEN_WIDTH - total_width) // 2

        self.button_easy = Button(
            self, 0, 0,
            self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png,
            width=self.button_difficulty_width,
            height=self.button_difficulty_height,
            override_x = start_x_diff,
            override_y = 300
        )
        
        self.button_medium = Button(
            self, 0, 0,
            self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png,
            width=self.button_difficulty_width,
            height=self.button_difficulty_height,
            override_x = start_x_diff + self.button_difficulty_width + spacing,
            override_y = 300
        )
        
        self.button_hard = Button(
            self, 0, 0,
            self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png,
            width=self.button_difficulty_width,
            height=self.button_difficulty_height,
            override_x = start_x_diff + 2 * (self.button_difficulty_width + spacing),
            override_y = 300
        )
        
        self.button_exit = Button(
            self, 0, 0, 
            self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png,
            width=self.button_exit_width,
            height=self.button_exit_height,
            override_x = self.SCREEN_WIDTH - self.button_exit_width - 20,
            override_y = self.SCREEN_HEIGHT - self.button_exit_height - 20
        )
        
        self.button_exit_main = Button(
            self, 0, 0, 
            self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png,
            width=self.button_exit_main_width,
            height=self.button_exit_main_height,
            override_x = self.SCREEN_WIDTH - self.button_exit_main_width - 20,
            override_y = self.SCREEN_HEIGHT - self.button_exit_main_height - 20
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
                         sys.exit()
                self.screen.fill((30, 30, 30))
                
                logo_x = (self.SCREEN_WIDTH - self.minesweeper_png.get_width()) // 2
                self.screen.blit(self.minesweeper_png, (logo_x, 50))
                
                self.button_start.draw()
                self.button_start.check_event()
                self.button_change.draw()
                self.button_change.check_event()
                self.button_exit_main.draw()
                self.button_exit_main.check_event()
                
            elif self.changing_difficulty:
        
                for event in pygame.event.get():
                   if event.type == pygame.QUIT:
                         sys.exit()
                self.screen.fill((30, 30, 30))
                
                title_x = (self.SCREEN_WIDTH - self.chosen_difficulty_png.get_width()) // 2
                self.screen.blit(self.chosen_difficulty_png, (title_x, 50))
                
                nums_y = 150
                nums_x = (self.SCREEN_WIDTH - self.easy_numbers_png.get_width()) // 2
                
                if self.is_easy_pointed:
                
                    self.screen.blit(self.easy_numbers_png, (nums_x, nums_y))
                    
                if self.is_medium_pointed:
                
                    self.screen.blit(self.medium_numbers_png, (nums_x, nums_y))
                    
                if self.is_hard_pointed:
                
                    self.screen.blit(self.hard_numbers_png, (nums_x, nums_y))
                    
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
                         sys.exit()
                
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
                    
                    win_x = (self.SCREEN_WIDTH - self.you_won_png.get_width()) // 2
                    self.screen.blit(self.you_won_png, (win_x, 0))
                    
            else:
                for event in pygame.event.get():
                   if event.type == pygame.QUIT:
                         sys.exit()
                         
                self.screen.fill((30, 30, 30)) 
                self.Reveal()
                self.button_exit.draw()
                self.button_exit.check_event()
                
                lost_x = (self.SCREEN_WIDTH - self.you_lost_png.get_width()) // 2
                self.screen.blit(self.you_lost_png, (lost_x, 0))
                 
            pygame.display.flip()
            pygame.time.wait(10)

    def CreateButtons(self):
        self.buttons_list = []
        self.tab = []
        
        self.board_pixel_width = self.columns * (self.cell_size + self.gap)
        self.board_pixel_height = self.rows * (self.cell_size + self.gap)
        self.start_x = (self.SCREEN_WIDTH - self.board_pixel_width) // 2 
        self.start_y = (self.SCREEN_HEIGHT - self.board_pixel_height) // 2
        
        for i in range(self.columns):
            row = []
            for j in range(self.rows):
                new_button = Button(self, i, j, self.przycisk_png, self.flaga_png, self.question_png, self.przycisk_v, self.kabum_png, self.mine_png, self.przycisk_blank, self.check_png, self.start_png, self.change_dif_png, self.easy_png, self.medium_png, self.hard_png, self.easy_pointed_png, self.medium_pointed_png, self.hard_pointed_png, self.exit_png, self.exit_main_png, width=self.cell_size, height=self.cell_size)
                self.buttons_list.append(new_button)
                row.append(new_button)
            self.tab.append(row)
            
    def InitializeRandom(self, i, j):
    
        while self.mines_on_tab < self.number_of_mines:
            ran_i = random.randint(0, self.columns-1)
            ran_j = random.randint(0, self.rows-1)
            
            deltas_temp = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1), (0, 0))
            is_forbidden = any(ran_i == i + dx and ran_j == j + dy for dx, dy in deltas_temp)

            if not is_forbidden:
                if self.tab[ran_i][ran_j].is_mine == False:
                    self.tab[ran_i][ran_j].is_mine = True
                    self.mines_on_tab += 1  
                  
    def CountMines(self):
        for button in self.buttons_list:
                for di, dj in deltas():
                    ni, nj = button.i + di, button.j + dj
                    if 0 <= ni < self.columns and 0 <= nj < self.rows:
                        if self.tab[ni][nj].is_mine:
                            button.mines_around += 1 
                            
    def Dfs(self, x, y):
        if not self.przegrana:
            if x < 0 or x >= self.columns or y < 0 or y >= self.rows:
                return
            if self.tab[x][y].is_flagged:
                return
            if self.tab[x][y].is_mine == True:
                if not self.przegrana:
                    self.przegrana = True
                    self.tab[x][y].is_visited = True
                    self.tab[x][y].is_kabum = True  
                return
            if self.tab[x][y].is_visited:
                return
            
            self.tab[x][y].is_visited = True

            if self.tab[x][y].mines_around == 0 or self.tab[x][y].mines_around == self.tab[x][y].mines_around_flagged:
                for dx, dy in deltas():
                    if not self.tab[x][y].is_mine:
                        self.Dfs(x + dx, y + dy)
                    
    def FirstClick(self, i, j):
        if self.first_click:
            return
        self.first_click = True
        self.InitializeRandom(i, j)
        self.CountMines()
        
    def Reveal(self):
        for button in self.buttons_list:
            button.draw()
            
    def Check(self):
        count_flags = 0
        for button in self.buttons_list:
            if button.is_flagged:
                count_flags+=1
        if count_flags == self.number_of_mines:
            for button in self.buttons_list:
                if button.is_mine and not button.is_flagged:
                    self.przegrana = True
                    self.Reveal()
            if not self.przegrana:
                self.is_win = True
                
    def update_settings(self):
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

        self.board_pixel_width = self.columns * (self.cell_size + self.gap)
        self.board_pixel_height = self.rows * (self.cell_size + self.gap)
        self.start_x = (self.SCREEN_WIDTH - self.board_pixel_width) // 2 
        self.start_y = (self.SCREEN_HEIGHT - self.board_pixel_height) // 2
        
        self.buttons_list = []
        self.tab = []
        self.mines_on_tab = 0
        
        new_check_x = (self.SCREEN_WIDTH - self.button_check_width) // 2
        new_check_y = self.start_y - self.button_check_height - 10
        
        if new_check_y < 0: new_check_y = 5
        
        self.button_check.rect.x = new_check_x
        self.button_check.rect.y = new_check_y
        self.button_check.x = new_check_x
        self.button_check.y = new_check_y
        
    def back_to_menu(self):
        self.przegrana = False
        self.first_click = False
        self.mines_on_tab = 0
        self.tab = []
        self.buttons_list = []
        self.beggining_of_the_game = True
        self.changing_difficulty = False
        self.is_win = False
        self.is_lost = False

def run_game(screen):
    game = Game(screen)
    game.mainLoop()

if __name__ == "__main__":
    run_game(None)
    pygame.quit()
