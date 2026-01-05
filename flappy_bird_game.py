import pygame
import random
import os
import sys
import subprocess

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird with a Twist")
clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

game_active = False
game_over_handled = False
score = 0
gravity = 0.25
bird_movement = 0

try:
    bird_surface = pygame.image.load(os.path.join('assets', 'bird.png')).convert_alpha()
    background_surface = pygame.image.load(os.path.join('assets', 'background.png')).convert()
    pipe_surface = pygame.image.load(os.path.join('assets', 'pipe.png')).convert_alpha()
except pygame.error as e:
    print(f"Error loading images: {e}")
    print("Please make sure you have the 'assets' folder with the required images.")
    pygame.quit()
    sys.exit()

background_surface = pygame.transform.scale(background_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
pipe_surface = pygame.transform.scale(pipe_surface, (50, SCREEN_HEIGHT))

bird_rect = bird_surface.get_rect(center=(50, SCREEN_HEIGHT / 2))

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

game_font = pygame.font.SysFont("Arial", 40)
message_font = pygame.font.SysFont("Arial", 20)

def create_pipe():
    pipe_height = random.choice([200, 300, 400])
    bottom_pipe = pipe_surface.get_rect(midtop=(SCREEN_WIDTH + 50, pipe_height))
    top_pipe = pipe_surface.get_rect(midbottom=(SCREEN_WIDTH + 50, pipe_height - 150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -50 or bird_rect.bottom >= 550:
        return False
    
    return True

def show_game_over_screen():
    game_over_text = game_font.render("Game Over", True, BLACK)
    message_text = message_font.render("Press SPACE to Play Again", True, BLACK)
    
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(message_text, message_rect)

def show_start_screen():
    title_text = game_font.render("Flappy Bird", True, BLACK)
    message_text = message_font.render("Press SPACE to Start", True, BLACK)
    
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    screen.blit(title_text, title_rect)
    screen.blit(message_text, message_rect)

def handle_game_over():
    global game_active, game_over_handled
    
    if not game_over_handled:
        game_active = False
        game_over_handled = True
        
        try:
            subprocess.Popen([sys.executable, 'lyrics_window.py'])
        except Exception as e:
            print(f"Failed to open lyrics window: {e}")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_movement = 0
                    bird_movement -= 6
                else:
                    game_active = True
                    game_over_handled = False
                    bird_rect.center = (50, SCREEN_HEIGHT / 2)
                    pipe_list.clear()
                    bird_movement = 0
                    score = 0

        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())

    screen.blit(background_surface, (0, 0))

    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface, bird_rect)
        
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        if not check_collision(pipe_list):
            handle_game_over()
    
    elif game_over_handled:
        show_game_over_screen()
    else:
        show_start_screen()

    pygame.display.update()
    clock.tick(FPS)