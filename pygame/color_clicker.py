import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CIRCLE_RADIUS = 40
NUM_CIRCLES = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

class ColorClickerGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Color Clicker Game")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.circles = []
        self.colors = [RED, BLUE, GREEN, YELLOW, PURPLE]
        self.score = 0
        self.game_over = False
        self.start_time = time.time()
        self.end_time = None
        self.font = pygame.font.Font(None, 36)
        
        self.create_circles()
        
    def create_circles(self):
        """Create circles at random positions"""
        self.circles = []
        for i in range(NUM_CIRCLES):
            # Ensure circles don't overlap too much
            while True:
                x = random.randint(CIRCLE_RADIUS, SCREEN_WIDTH - CIRCLE_RADIUS)
                y = random.randint(CIRCLE_RADIUS, SCREEN_HEIGHT - CIRCLE_RADIUS)
                
                # Check if position is too close to existing circles
                valid_position = True
                for existing_circle in self.circles:
                    distance = ((x - existing_circle['x'])**2 + (y - existing_circle['y'])**2)**0.5
                    if distance < CIRCLE_RADIUS * 2.5:  # Minimum distance between circles
                        valid_position = False
                        break
                
                if valid_position:
                    break
            
            circle = {
                'x': x,
                'y': y,
                'color': self.colors[i % len(self.colors)],
                'clicked': False
            }
            self.circles.append(circle)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_circle_click(mouse_x, mouse_y)
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.__init__()  # Reset game
                    
        return True
    
    def check_circle_click(self, mouse_x, mouse_y):
        """Check if mouse click hits any circle"""
        for circle in self.circles:
            if not circle['clicked']:
                # Calculate distance from mouse to circle center
                distance = ((mouse_x - circle['x'])**2 + (mouse_y - circle['y'])**2)**0.5
                
                if distance <= CIRCLE_RADIUS:
                    circle['clicked'] = True
                    self.score += 1
                    
                    # Check if all circles are clicked
                    if self.score >= NUM_CIRCLES:
                        self.game_over = True
                        self.end_time = time.time()
                    break
    
    def get_elapsed_time(self):
        """Get elapsed time since game start"""
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time
    
    def draw(self):
        """Draw everything on screen"""
        self.screen.fill(WHITE)
        
        # Draw circles
        for circle in self.circles:
            if not circle['clicked']:
                pygame.draw.circle(self.screen, circle['color'], 
                                 (circle['x'], circle['y']), CIRCLE_RADIUS)
                # Draw border
                pygame.draw.circle(self.screen, BLACK, 
                                 (circle['x'], circle['y']), CIRCLE_RADIUS, 3)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}/{NUM_CIRCLES}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # Draw timer
        elapsed_time = self.get_elapsed_time()
        time_text = self.font.render(f"Time: {elapsed_time:.1f}s", True, BLACK)
        self.screen.blit(time_text, (10, 50))
        
        # Draw instructions
        if self.score == 0:
            instruction_text = self.font.render("Click all the colored circles!", True, BLACK)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, 100))
            self.screen.blit(instruction_text, instruction_rect)
        
        # Draw game completion message
        if self.game_over:
            win_text = self.font.render("Congratulations! All circles clicked!", True, GREEN)
            total_time_text = self.font.render(f"Total time: {elapsed_time:.2f} seconds", True, BLACK)
            restart_text = self.font.render("Press R to play again", True, BLACK)
            
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            time_rect = total_time_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            
            self.screen.blit(win_text, win_rect)
            self.screen.blit(total_time_text, time_rect)
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ColorClickerGame()
    game.run()