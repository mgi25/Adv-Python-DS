# Q7. Using PyGame, design a mini interactive window where:
# • A small circle moves using arrow keys.
# • Background color changes when the circle hits window borders.
# • The window closes on pressing the Escape key.

import pygame
import random
import sys

# Initialize PyGame
pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 600, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Circle Game")

# --- Circle setup ---
circle_radius = 20
x, y = WIDTH // 2, HEIGHT // 2
speed = 5

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
background_color = WHITE
circle_color = (0, 120, 255)

# --- Main Game Loop ---
running = True
clock = pygame.time.Clock()

while running:
    window.fill(background_color)

    for event in pygame.event.get():
        # Exit on close window or ESC key
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Key states
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    # --- Collision with borders ---
    hit_border = False

    if x - circle_radius <= 0:
        x = circle_radius
        hit_border = True
    elif x + circle_radius >= WIDTH:
        x = WIDTH - circle_radius
        hit_border = True

    if y - circle_radius <= 0:
        y = circle_radius
        hit_border = True
    elif y + circle_radius >= HEIGHT:
        y = HEIGHT - circle_radius
        hit_border = True

    # Change background color when hitting borders
    if hit_border:
        background_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

    # --- Draw the circle ---
    pygame.draw.circle(window, circle_color, (x, y), circle_radius)

    # Update display
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

# --- Exit PyGame safely ---
pygame.quit()
sys.exit()
