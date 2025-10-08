# PyGame Basics — Q1..Q8 (no image, no sound)
# Q1 Window, Q2 Background, Q3 Shapes, Q4 Keyboard messages,
# Q5 Mouse circles, Q6 Color switcher, Q7 Moving ball, Q8 Bouncing ball

import pygame

pygame.init()

# Q1. Game Window (800x600) with title
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gp")
clock = pygame.time.Clock()

# Q2. Background Color (start blue)
bg_color = (0, 0, 255)

# Q3. Shapes (fixed)
rect_color = (255, 0, 0)        # red
rect_pos = (50, 50, 100, 50)    # x, y, w, h

green = (0, 200, 0)
circle_center = (250, 150)
circle_radius = 40

black = (0, 0, 0)               # line color

# Q5. Mouse circles
clicked_circles = []
mouse_circle_radius = 18
mouse_circle_color = (128, 0, 128)  # purple

# Q7. Moving Ball (arrow keys)
ball_color = (255, 165, 0)  # orange
ball_radius = 12
ball_x, ball_y = 20, HEIGHT // 2
ball_speed = 5

# Q8. Auto Bouncing Ball (left <-> right)
auto_ball_color = (30, 144, 255)  # dodger blue
auto_ball_radius = 16
auto_ball_x = auto_ball_radius
auto_ball_y = HEIGHT // 3
auto_ball_speed_x = 4

running = True
while running:
    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Q4. Keyboard messages + Q6. Color switcher
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                print("UP Arrow Pressed")
            if event.key == pygame.K_r:
                bg_color = (255, 0, 0)   # Red
            if event.key == pygame.K_g:
                bg_color = (0, 255, 0)   # Green
            if event.key == pygame.K_b:
                bg_color = (0, 0, 255)   # Blue

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                print("DOWN Arrow Released")

        # Q5. Mouse: draw circle at click position (left button)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_circles.append(event.pos)

    # --- Continuous keys for movement (Q7) ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ball_x -= ball_speed
    if keys[pygame.K_RIGHT]:
        ball_x += ball_speed
    if keys[pygame.K_UP]:
        ball_y -= ball_speed
    if keys[pygame.K_DOWN]:
        ball_y += ball_speed

    # Keep moving ball inside window
    if ball_x - ball_radius < 0:
        ball_x = ball_radius
    if ball_x + ball_radius > WIDTH:
        ball_x = WIDTH - ball_radius
    if ball_y - ball_radius < 0:
        ball_y = ball_radius
    if ball_y + ball_radius > HEIGHT:
        ball_y = HEIGHT - ball_radius

    # Q8. Auto-bouncing ball update
    auto_ball_x += auto_ball_speed_x
    if auto_ball_x - auto_ball_radius <= 0 or auto_ball_x + auto_ball_radius >= WIDTH:
        auto_ball_speed_x *= -1
        auto_ball_x += auto_ball_speed_x  # tiny nudge so it doesn't stick

    # --- Drawing ---
    screen.fill(bg_color)  # Q2

    # Q3. Shapes
    pygame.draw.rect(screen, rect_color, rect_pos)                               # red rectangle 100x50
    pygame.draw.circle(screen, green, circle_center, circle_radius)              # green circle r=40
    pygame.draw.line(screen, black, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)   # black line across

    # Q5. Draw clicked circles
    for pos in clicked_circles:
        pygame.draw.circle(screen, mouse_circle_color, pos, mouse_circle_radius)

    # Q7. Moving ball
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    # Q8. Auto-bouncing ball
    pygame.draw.circle(screen, auto_ball_color, (int(auto_ball_x), auto_ball_y), auto_ball_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
