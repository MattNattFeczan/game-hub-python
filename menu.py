import pygame
import sys

# inicjalizacja srodowiska i dzwieku
pygame.init()
pygame.mixer.init()

# ustawienia okna i wyswietlania
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("game hub")
clock = pygame.time.Clock()

# ladowanie obrazu tla z pliku
try:
    background_img = pygame.image.load("background.png").convert()
    background_img = pygame.transform.scale(background_img, (width, height))
except Exception:
    # jesli nie ma pliku, ustawiamy ciemne tlo zastepcze
    background_img = pygame.Surface((width, height))
    background_img.fill((15, 15, 25))

# kontroler muzyki w tle
is_muted = False
try:
    pygame.mixer.music.load("lobby.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1) # odtwarzanie w petli
except Exception:
    pass # ciche pominiecie bledu braku muzyki

# definicja kolorystyki interfejsu (rgba)
btn_color   = (0, 0, 0, 200)   # czarny z przezroczystoscia
hover_clr   = (35, 35, 45, 230) # jasniejszy przy najechaniu
text_white  = (250, 250, 250)
border_clr  = (180, 180, 180)

# ladowanie czcionek systemowych
try:
    font_title = pygame.font.SysFont('impact', 95)
    font_btn   = pygame.font.SysFont('verdana', 22, bold=True)
except Exception:
    font_title = pygame.font.SysFont('arial', 95, bold=True)
    font_btn   = pygame.font.SysFont('arial', 22, bold=True)

# generatory ikonek dla przyciskow (rysowane wektorowo)

def get_ttc_icon():
    # ikonka kolko i krzyzyk - siatka i symbole
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.line(surf, (150, 150, 150), (14, 2), (14, 38), 2)
    pygame.draw.line(surf, (150, 150, 150), (26, 2), (26, 38), 2)
    pygame.draw.line(surf, (150, 150, 150), (2, 14), (38, 14), 2)
    pygame.draw.line(surf, (150, 150, 150), (2, 26), (38, 26), 2)
    pygame.draw.line(surf, (230, 70, 60), (4, 4), (12, 12), 3)
    pygame.draw.line(surf, (230, 70, 60), (12, 4), (4, 12), 3)
    pygame.draw.circle(surf, (50, 200, 110), (20, 20), 5, 3)
    return surf

def get_ship_icon():
    # ikonka statku - kadlub i wieza
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (140, 150, 160), [(5, 32), (28, 32), (38, 25), (32, 18), (5, 18)])
    pygame.draw.rect(surf, (140, 150, 160), (12, 10, 10, 8))
    pygame.draw.line(surf, (50, 50, 60), (26, 20), (36, 17), 4)
    return surf

def get_mine_icon():
    # ikonka sapera - mina morska z kolcami
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    center = (20, 20)
    offsets = [(-15, 0), (15, 0), (0, -15), (0, 15), (-11, -11), (11, 11)]
    for off in offsets:
        pygame.draw.circle(surf, (40, 45, 50), (center[0]+off[0], center[1]+off[1]), 4)
    pygame.draw.circle(surf, (65, 75, 85), center, 14)
    pygame.draw.ellipse(surf, (100, 110, 120), (10, 10, 10, 7))
    return surf

def get_speaker_icon(muted):
    # ikonka glosnika - kolor zmienia sie przy wyciszeniu
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    clr = (220, 60, 50) if muted else (230, 230, 230)
    pygame.draw.rect(surf, clr, (10, 15, 8, 10))
    pygame.draw.polygon(surf, clr, [(18, 15), (28, 8), (28, 32), (18, 25)])
    if muted: pygame.draw.line(surf, clr, (32, 10), (32, 30), 3)
    return surf

# klasa odpowiedzialna za przyciski interfejsu
class Button:
    def __init__(self, text, x, y, w, h, icon, callback, is_mini=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.icon = icon
        self.callback = callback
        self.hover = False
        self.is_mini = is_mini

    def render(self, target):
        # sprawdzanie czy mysz znajduje sie nad przyciskiem
        self.hover = self.rect.collidepoint(pygame.mouse.get_pos())
        color = hover_clr if self.hover else btn_color
        
        # tworzenie warstwy przycisku z przezroczystoscia
        s = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        pygame.draw.rect(s, color, s.get_rect(), border_radius=10)
        pygame.draw.rect(s, border_clr, s.get_rect(), 2, border_radius=10)
        target.blit(s, self.rect.topleft)

        # rysowanie ikony na przycisku
        if self.icon:
            ix = self.rect.x + (self.rect.w//2 if self.is_mini else 25)
            target.blit(self.icon, self.icon.get_rect(center=(ix, self.rect.centery)))

        # rysowanie tekstu przycisku
        if self.text:
            t_surf = font_btn.render(self.text, True, text_white)
            target.blit(t_surf, t_surf.get_rect(center=(self.rect.centerx + 20, self.rect.centery)))

    def update(self, event):
        # obsługa klikniecia lewym przyciskiem myszy
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hover:
            self.callback()

# funkcje wywolywane przez przyciski

def toggle_audio():
    # przelaczanie wyciszenia muzyki
    global is_muted
    is_muted = not is_muted
    pygame.mixer.music.set_volume(0 if is_muted else 0.4)


def run_ttc():
    try:
        from games import tic_tac_toe_10x10
        tic_tac_toe_10x10.launch_tictactoe(screen)
    except Exception:
        pass

def run_battleships():
    # uruchomienie gry statki
    try:
        from games import battleship
        battleship.launch_battleship(screen, clock, 60)
    except Exception: pass

def run_minesweeper():
    # uruchomienie gry saper
    try:
        from games import minesweeper
        minesweeper.run_game(screen)
    except Exception: pass

# glowna petla wykonawcza menu
def main_exec():
    b_w, b_h = 350, 75
    center_x = width // 2 - b_w // 2
    
    # przycisk kontroli dzwieku w gornym rogu
    mute_ctrl = Button("", width - 65, 20, 45, 45, get_speaker_icon(is_muted), toggle_audio, True)

    # lista przyciskow nawigacyjnych
    nav_btns = [
        Button("tic-tac-toe", center_x, 220, b_w, b_h, get_ttc_icon(), run_ttc),
        Button("battleships", center_x, 315, b_w, b_h, get_ship_icon(), run_battleships),
        Button("minesweeper", center_x, 410, b_w, b_h, get_mine_icon(), run_minesweeper),
        Button("exit hub",    center_x, 510, b_w, b_h, None,          lambda: sys.exit())
    ]

    while True:
        # wyswietlanie tla
        screen.blit(background_img, (0, 0))

        # rysowanie naglowka z cieniem
        t_main = font_title.render("game hub", True, text_white)
        t_shadow = font_title.render("game hub", True, (10, 10, 10))
        t_rect = t_main.get_rect(center=(width//2, 100))
        screen.blit(t_shadow, (t_rect.x + 4, t_rect.y + 4))
        screen.blit(t_main, t_rect)

        # obsluga zdarzen systemowych i wejscia
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            mute_ctrl.update(e)
            for b in nav_btns: b.update(e)

        # aktualizacja stanu ikon i renderowanie interfejsu
        mute_ctrl.icon = get_speaker_icon(is_muted)
        mute_ctrl.render(screen)
        for b in nav_btns: b.render(screen)

        # odswiezenie ekranu
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_exec()
