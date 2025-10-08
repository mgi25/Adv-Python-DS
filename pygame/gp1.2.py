import pygame, random
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Catch the Circle")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

# Player (rectangle)
player = pygame.Rect(400, 500, 80, 30)
speed = 7

# Circle
circle_x = random.randint(50, 750)
circle_y = random.randint(50, 550)
radius = 25

score = 0
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_UP]:
        player.y -= speed
    if keys[pygame.K_DOWN]:
        player.y += speed

    # Boundaries
    player.x = max(0, min(800 - player.width, player.x))
    player.y = max(0, min(600 - player.height, player.y))

    # Check collision
    dx = abs(circle_x - (player.x + player.width // 2))
    dy = abs(circle_y - (player.y + player.height // 2))
    if dx < radius + player.width // 2 and dy < radius + player.height // 2:
        score += 1
        circle_x = random.randint(50, 750)
        circle_y = random.randint(50, 550)

    # Draw
    screen.fill(white)
    pygame.draw.rect(screen, blue, player)
    pygame.draw.circle(screen, red, (circle_x, circle_y), radius)
    text = font.render(f"Score: {score}", True, black)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
 