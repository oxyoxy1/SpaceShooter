# menu.py

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Initialize pygame
pygame.init()

# Title Image
title = pygame.image.load("assets/title.png")
title = pygame.transform.scale(title, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale title to fit screen
font = pygame.font.Font(None, 40)

def show_main_menu(screen, font):
    screen.fill((255, 255, 255))
    
    # Show the title centered on the screen
    screen.blit(title, (0, 0))  # Title image now covers the whole screen

    # Show instructions
    start_text = font.render("Press ENTER to Start", True, (0, 0, 0))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
    
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

def show_game_over(screen, font):
    screen.fill((0, 0, 0))  # Fill the screen with black for Game Over
    
    game_over_text = font.render("Game Over", True, (255, 0, 0))  # Red Game Over text
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))

    # Show the option to restart or quit
    restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False  # Restart the game
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()  # Quit the game

def show_leaderboard(screen, font, leaderboard):
    # Clear the screen
    screen.fill((0, 0, 0))  # Fill the screen with black color
    
    # Display the title
    title = font.render("Leaderboard", True, (255, 255, 255))  # White color
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))  # Center the title

    # Loop through leaderboard data and render each player's initials and score
    y_offset = 100  # Starting Y position for the leaderboard list
    for player in leaderboard:
        initials = player.get("initials", "")
        score = player.get("score", 0)
        text = f"{initials}: {score}"
        rendered_text = font.render(text, True, (255, 255, 255))  # White color
        screen.blit(rendered_text, (screen.get_width() // 2 - rendered_text.get_width() // 2, y_offset))
        y_offset += 40  # Increase Y offset for the next player

    # Update the display
    pygame.display.flip()

