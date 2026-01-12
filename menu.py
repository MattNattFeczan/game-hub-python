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
