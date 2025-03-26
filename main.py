import pygame
import random
import sys
import json
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from assets import *
from menu import show_main_menu, show_game_over, show_leaderboard

pygame.init()

# Font setup (make sure to define this before using it)
font = pygame.font.Font(None, 32)

# Game screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")

# Load background music
pygame.mixer.init()
pygame.mixer.music.load("assets/game_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop indefinitely

# Load sound effects
shoot_sound = pygame.mixer.Sound("assets/shoot.wav")  # Ensure this file exists
shoot_sound.set_volume(0.5)  # Adjust volume if needed

# Load background image
background_image = pygame.image.load("assets/background.png").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    except FileNotFoundError:
        return []  # If the file doesn't exist, return an empty list

def save_leaderboard(leaderboard):
    with open("leaderboard.json", "w") as file:
        json.dump(leaderboard, file)
    show_leaderboard(screen, font, leaderboard)  # Show leaderboard after saving

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 4

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def shoot(self):
        # Adjust bullet spawn to start just above the ship, aligning with the center
        bullet = Bullet(self.rect.right, self.rect.centery)  # Spawn a bit higher to avoid the bullet colliding with the ship
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7  # Speed of the bullet

    def update(self):
        self.rect.x += self.speed  # Moves the bullet to the right
        if self.rect.left > SCREEN_WIDTH:  # Remove bullet when it exits the screen
            self.kill()

# Game Setup
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for _ in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

def get_initials():
    # Function to prompt for initials using a text input box
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text[:3]  # Limit to 3 characters for initials
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        # Render the prompt text for entering initials
        prompt_text = font.render("Enter your initials:", True, (0, 0, 0))
        screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Center the text inside the input box
        screen.blit(txt_surface, (input_box.x + (input_box.w - txt_surface.get_width()) // 2, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

def main_game():
    clock = pygame.time.Clock()
    running = True
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()

        for bullet in bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)
            for hit in hit_enemies:
                score += 10
                bullet.kill()
                new_enemy = Enemy()
                all_sprites.add(new_enemy)
                enemies.add(new_enemy)

        if pygame.sprite.spritecollide(player, enemies, False):
            initials = get_initials()  # Get initials after game ends
            leaderboard = load_leaderboard()
            leaderboard.append({"initials": initials, "score": score})
            leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
            save_leaderboard(leaderboard)
            show_leaderboard(screen, font, leaderboard)
            
            # Wait for user input to continue (e.g., pressing any key to return to the main menu)
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        # After any key press, return to the main menu
                        show_main_menu(screen, font)
                        waiting_for_input = False
            return

        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(60)

show_main_menu(screen, font)
main_game()
