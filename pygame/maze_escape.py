import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 30
PLAYER_SPEED = 5
OBSTACLE_WIDTH = 60
OBSTACLE_HEIGHT = 100
NUM_OBSTACLES = 6

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

class MazeEscape:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Maze Escape")
        self.clock = pygame.time.Clock()
        
        # Player position
        self.player_x = 20
        self.player_y = SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2
        
        # Game state
        self.game_over = False
        self.game_won = False
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        
        # Create obstacles
        self.obstacles = self.create_obstacles()
        
    def create_obstacles(self):
        """Create obstacles at random positions"""
        obstacles = []
        
        # Create obstacles in the middle area of the screen
        for i in range(NUM_OBSTACLES):
            # Ensure obstacles are not too close to start or end
            x = random.randint(150, SCREEN_WIDTH - 150 - OBSTACLE_WIDTH)
            y = random.randint(50, SCREEN_HEIGHT - 50 - OBSTACLE_HEIGHT)
            
            # Make sure obstacles don't overlap too much
            valid_position = False
            attempts = 0
            while not valid_position and attempts < 20:
                valid_position = True
                for existing_obstacle in obstacles:
                    if (abs(x - existing_obstacle['x']) < OBSTACLE_WIDTH + 20 and
                        abs(y - existing_obstacle['y']) < OBSTACLE_HEIGHT + 20):
                        valid_position = False
                        x = random.randint(150, SCREEN_WIDTH - 150 - OBSTACLE_WIDTH)
                        y = random.randint(50, SCREEN_HEIGHT - 50 - OBSTACLE_HEIGHT)
                        break
                attempts += 1
            
            obstacle = {'x': x, 'y': y}
            obstacles.append(obstacle)
            
        return obstacles
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (self.game_over or self.game_won):
                    self.__init__()  # Reset game
        return True
    
    def update(self):
        """Update game logic"""
        if self.game_over or self.game_won:
            return
        
        # Handle player movement
        keys = pygame.key.get_pressed()
        new_x = self.player_x
        new_y = self.player_y
        
        if keys[pygame.K_LEFT] and self.player_x > 0:
            new_x = self.player_x - PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.player_x < SCREEN_WIDTH - PLAYER_SIZE:
            new_x = self.player_x + PLAYER_SPEED
        if keys[pygame.K_UP] and self.player_y > 0:
            new_y = self.player_y - PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.player_y < SCREEN_HEIGHT - PLAYER_SIZE:
            new_y = self.player_y + PLAYER_SPEED
        
        # Check collision with obstacles before moving
        player_rect = pygame.Rect(new_x, new_y, PLAYER_SIZE, PLAYER_SIZE)
        
        collision = False
        for obstacle in self.obstacles:
            obstacle_rect = pygame.Rect(obstacle['x'], obstacle['y'], 
                                      OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
            if player_rect.colliderect(obstacle_rect):
                collision = True
                break
        
        # Only move if no collision
        if not collision:
            self.player_x = new_x
            self.player_y = new_y
        else:
            # If collision detected, game over
            self.game_over = True
        
        # Check if player reached the right side (win condition)
        if self.player_x >= SCREEN_WIDTH - PLAYER_SIZE - 10:
            self.game_won = True
    
    def draw(self):
        """Draw everything on screen"""
        self.screen.fill(WHITE)
        
        # Draw goal area (right side)
        goal_area = pygame.Rect(SCREEN_WIDTH - 50, 0, 50, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, GREEN, goal_area)
        
        # Draw start area (left side)
        start_area = pygame.Rect(0, 0, 50, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, YELLOW, start_area)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, RED, 
                           (obstacle['x'], obstacle['y'], OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
            # Draw border
            pygame.draw.rect(self.screen, BLACK, 
                           (obstacle['x'], obstacle['y'], OBSTACLE_WIDTH, OBSTACLE_HEIGHT), 2)
        
        # Draw player
        if not self.game_over:
            pygame.draw.rect(self.screen, BLUE, 
                           (self.player_x, self.player_y, PLAYER_SIZE, PLAYER_SIZE))
            # Draw player border
            pygame.draw.rect(self.screen, BLACK, 
                           (self.player_x, self.player_y, PLAYER_SIZE, PLAYER_SIZE), 2)
        
        # Draw instructions at the top
        if not self.game_over and not self.game_won:
            instruction_text = self.small_font.render(
                "Use arrow keys to move. Avoid red obstacles. Reach the green area!", 
                True, BLACK)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, 20))
            self.screen.blit(instruction_text, instruction_rect)
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            collision_text = self.small_font.render("You hit an obstacle!", True, BLACK)
            restart_text = self.small_font.render("Press R to restart", True, BLACK)
            
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            collision_rect = collision_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(collision_text, collision_rect)
            self.screen.blit(restart_text, restart_rect)
        
        # Draw win message
        if self.game_won:
            win_text = self.font.render("YOU WIN!", True, GREEN)
            success_text = self.small_font.render("You successfully escaped the maze!", True, BLACK)
            restart_text = self.small_font.render("Press R to play again", True, BLACK)
            
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            success_rect = success_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            
            self.screen.blit(win_text, win_rect)
            self.screen.blit(success_text, success_rect)
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
    game = MazeEscape()
    game.run()