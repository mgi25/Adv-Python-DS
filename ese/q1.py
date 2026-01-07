# create a PyGame window with a rectangle controlled by arrow keys

import sys
import pygame

pygame.init()

WIDTH, HEIGHT = 900, 560
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arrow Key Rectangle")

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 18)

rect_w, rect_h = 70, 50
rect = pygame.Rect((WIDTH - rect_w) // 2, (HEIGHT - rect_h) // 2, rect_w, rect_h)
speed = 7


bg_color = (18, 18, 22)
rect_color = (235, 235, 245)
rect_border = (25, 25, 40)
panel_color = (0, 0, 0, 140)  
grid_line = (255, 255, 255, 18)  

def draw_soft_grid():
    grid = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for x in range(0, WIDTH, 40):
        pygame.draw.line(grid, grid_line, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(grid, grid_line, (0, y), (WIDTH, y))
    screen.blit(grid, (0, 0))

def draw_hud():
    hud = pygame.Surface((WIDTH, 44), pygame.SRCALPHA)
    hud.fill(panel_color)
    screen.blit(hud, (0, 0))

    t1 = font.render("Move: Arrow Keys", True, (245, 245, 245))
    t2 = font.render(f"Position: ({rect.x}, {rect.y})", True, (245, 245, 245))
    t3 = font.render("Press close button to exit", True, (245, 245, 245))

    screen.blit(t1, (14, 12))
    screen.blit(t2, (230, 12))
    screen.blit(t3, (520, 12))

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rect.x -= speed
    if keys[pygame.K_RIGHT]:
        rect.x += speed
    if keys[pygame.K_UP]:
        rect.y -= speed
    if keys[pygame.K_DOWN]:
        rect.y += speed

    rect.x = max(0, min(rect.x, WIDTH - rect.w))
    rect.y = max(0, min(rect.y, HEIGHT - rect.h))

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
