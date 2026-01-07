# change background color on boundary collision

import sys
import pygame

pygame.init()

WIDTH, HEIGHT = 900, 560
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Border Touch Color Cycle")

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 18)

rect = pygame.Rect((WIDTH - 70) // 2, (HEIGHT - 50) // 2, 70, 50)
speed = 7

bg_cycle = [
    (220, 60, 60),   
    (70, 120, 255),  # Blue
    (60, 200, 120),  # Green
    (255, 170, 60),  # Orange (extra)
    (170, 90, 220),  # Purple (extra)
]
bg_index = 0
bg_color = (18, 18, 22)  # start dark

panel_color = (0, 0, 0, 120)  # translucent overlay
rect_color = (235, 235, 245)
rect_border = (20, 20, 30)

def draw_hud():
    # Top translucent bar
    hud = pygame.Surface((WIDTH, 44), pygame.SRCALPHA)
    hud.fill(panel_color)
    screen.blit(hud, (0, 0))

    text1 = font.render("Move: Arrow Keys", True, (240, 240, 240))
    text2 = font.render(f"Background RGB: {bg_color}", True, (240, 240, 240))
    text3 = font.render("Touch border to change background color", True, (240, 240, 240))

    screen.blit(text1, (14, 12))
    screen.blit(text2, (220, 12))
    screen.blit(text3, (520, 12))

def draw_soft_grid():
    grid_color = (255, 255, 255, 20)
    grid = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for x in range(0, WIDTH, 40):
        pygame.draw.line(grid, grid_color, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(grid, grid_color, (0, y), (WIDTH, y))
    screen.blit(grid, (0, 0))

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement input
    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_LEFT]:
        dx -= speed
    if keys[pygame.K_RIGHT]:
        dx += speed
    if keys[pygame.K_UP]:
        dy -= speed
    if keys[pygame.K_DOWN]:
        dy += speed

    # Move
    rect.x += dx
    rect.y += dy

    before_x, before_y = rect.x, rect.y

    rect.x = max(0, min(rect.x, WIDTH - rect.w))
    rect.y = max(0, min(rect.y, HEIGHT - rect.h))

    touched_border = (rect.x != before_x) or (rect.y != before_y)
    if touched_border:
        bg_color = bg_cycle[bg_index]
        bg_index = (bg_index + 1) % len(bg_cycle)

    screen.fill(bg_color)
    draw_soft_grid()

    shadow = rect.copy()
    shadow.x += 6
    shadow.y += 6
    pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=10)

    pygame.draw.rect(screen, rect_color, rect, border_radius=10)
    pygame.draw.rect(screen, rect_border, rect, width=2, border_radius=10)

    draw_hud()
    pygame.display.flip()

pygame.quit()
sys.exit()
