import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 15
PADDLE_SPEED = 8
BALL_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class PaddleBall:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Paddle Ball (Mini Pong)")
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
        self.paddle_y = SCREEN_HEIGHT - 50
        
        self.ball_x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
        self.ball_y = BALL_RADIUS
        self.ball_speed_y = BALL_SPEED
        
        self.score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
        
    def reset_ball(self):
        """Reset ball to top of screen at random position"""
        self.ball_x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
        self.ball_y = BALL_RADIUS
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.__init__()  # Reset game
        return True
        
    def update(self):
        """Update game logic"""
        if self.game_over:
            return
            
        # Handle paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.paddle_x > 0:
            self.paddle_x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and self.paddle_x < SCREEN_WIDTH - PADDLE_WIDTH:
            self.paddle_x += PADDLE_SPEED
            
        # Update ball position
        self.ball_y += self.ball_speed_y
        
        # Check ball collision with paddle
        if (self.ball_y + BALL_RADIUS >= self.paddle_y and
            self.ball_y - BALL_RADIUS <= self.paddle_y + PADDLE_HEIGHT and
            self.ball_x >= self.paddle_x and
            self.ball_x <= self.paddle_x + PADDLE_WIDTH):
            self.score += 1
            self.reset_ball()
            
        # Check if ball hits bottom (game over)
        if self.ball_y > SCREEN_HEIGHT:
            self.game_over = True
            
    def draw(self):
        """Draw everything on screen"""
        self.screen.fill(BLACK)
        
        if not self.game_over:
            # Draw paddle
            pygame.draw.rect(self.screen, BLUE, 
                           (self.paddle_x, self.paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
            
            # Draw ball
            pygame.draw.circle(self.screen, RED, 
                             (int(self.ball_x), int(self.ball_y)), BALL_RADIUS)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            restart_text = self.font.render("Press R to restart", True, WHITE)
            
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PaddleBall()
    game.run()