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
