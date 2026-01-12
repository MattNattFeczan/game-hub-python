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
    background_img = pygame.Surface((width, height))
    background_img.fill((15, 15, 25))

# ladowanie czcionek systemowych
try:
    font_title = pygame.font.SysFont('impact', 95)
    font_btn   = pygame.font.SysFont('verdana', 22, bold=True)
except Exception:
    font_title = pygame.font.SysFont('arial', 95, bold=True)
    font_btn   = pygame.font.SysFont('arial', 22, bold=True)
    
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

# kontroler muzyki w tle
is_muted = False
try:
    pygame.mixer.music.load("lobby.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
except Exception:
    pass

def toggle_audio():
    global is_muted
    is_muted = not is_muted
    pygame.mixer.music.set_volume(0 if is_muted else 0.4)
