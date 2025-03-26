import pygame
import os

# Set up pygame and initialize the window
pygame.init()

# Game screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
def load_image(image_name):
    return pygame.image.load(os.path.join("assets", image_name))

# Load fonts
def load_font(font_name, size):
    return pygame.font.Font(os.path.join("assets", font_name), size)

# Asset loading (Example)
player_img = load_image("player.png")
enemy_img = load_image("enemy.png")
bullet_img = load_image("bullet.png")
bg_img = load_image("background.png")
font = load_font("game_font.ttf", 32)
