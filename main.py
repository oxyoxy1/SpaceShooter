import pygame
import random
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from assets import *
from menu import show_main_menu, show_game_over

# Initialize pygame and set up the game
pygame.init()

# Game screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")

# Load background image from /assets folder
background_image = pygame.image.load("assets/background.png").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        # Adjust the player's hitbox by scaling the rect smaller than the image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.rect.width = self.rect.width // 1.5  # Reduce width
        self.rect.height = self.rect.height // 1.5  # Reduce height
        self.speed = 2  # Reduced speed by half

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:  # 'A' key for left
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:  # 'D' key for right
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.top > 0:  # 'W' key for up
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT:  # 'S' key for down
            self.rect.y += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery)  # Spawn bullet at center
        all_sprites.add(bullet)
        bullets.add(bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7  # Bullet speed

    def update(self):
        # Change bullet movement to the right (increasing x-coordinate)
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH:  # If the bullet goes off the screen to the right
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH  # Start from the right
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)  # Random vertical position
        self.speed = random.randint(2, 5)  # Reduced speed by half

    def update(self):
        self.rect.x -= self.speed  # Move leftward
        if self.rect.right < 0:  # If it goes off the screen, reset it to the right side
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

# Game setup
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Add enemies
for _ in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

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
                if event.key == pygame.K_r:  # Detect 'R' to restart the game
                    return main_game()  # Recursively call main_game to restart

        # Update
        all_sprites.update()

        # Check for collisions
        for bullet in bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)
            for hit in hit_enemies:
                score += 10
                bullet.kill()
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)

        # Check if player hits enemy
        if pygame.sprite.spritecollide(player, enemies, False):
            if show_game_over(screen, font):
                return main_game()  # Restart the game
            return

        # Drawing
        screen.fill(WHITE)

        # Draw background
        screen.blit(background_image, (0, 0))  # Draw background image

        # Draw all sprites (player, enemies, bullets)
        all_sprites.draw(screen)

        # Display score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

# Start screen
show_main_menu(screen, font)

# Start the game loop
main_game()
