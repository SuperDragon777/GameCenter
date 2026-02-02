import pygame
import random
from enum import Enum
from collections import deque
import os, sys

def resource_path(path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, path)
    return path


score_per_food = 1
tick = 10

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Snake:
    def __init__(self, width=800, height=600, grid_size=20):
        pygame.init()
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.grid_width = width // grid_size
        self.grid_height = height // grid_size
        
        self.screen = pygame.display.set_mode((width, height))
        icon = pygame.image.load(resource_path("snake_icon.png"))
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Змейка")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.reset_game()
        
    def reset_game(self):
        start_x = self.grid_width // 2
        start_y = self.grid_height // 2
        self.snake = deque([(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)])
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        
    def spawn_food(self):
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_w and self.direction != Direction.DOWN:
                    self.next_direction = Direction.UP
                elif event.key == pygame.K_s and self.direction != Direction.UP:
                    self.next_direction = Direction.DOWN
                elif event.key == pygame.K_a and self.direction != Direction.RIGHT:
                    self.next_direction = Direction.LEFT
                elif event.key == pygame.K_d and self.direction != Direction.LEFT:
                    self.next_direction = Direction.RIGHT
        return True
    
    def update(self):
        if self.game_over:
            return
        
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or
            new_head[1] < 0 or new_head[1] >= self.grid_height):
            print(f"[DEATH] Snake hit the wall at position ({new_head[0]}, {new_head[1]}). Final score: {self.score}")
            self.game_over = True
            return
        
        if new_head in self.snake:
            print(f"[DEATH] Snake hit itself at position {new_head}. Final score: {self.score}")
            self.game_over = True
            return
        
        self.snake.appendleft(new_head)
        
        if new_head == self.food:
            self.score += score_per_food
            print(f"[FOOD] Ate food at {new_head}. Score: {self.score}, Snake length: {len(self.snake)}")
            self.food = self.spawn_food()
        else:
            self.snake.pop()
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        
        for i, (x, y) in enumerate(self.snake):
            color = (0, 255, 0) if i == 0 else (0, 200, 0)
            pygame.draw.rect(self.screen, color, 
                           (x * self.grid_size, y * self.grid_size, 
                            self.grid_size - 2, self.grid_size - 2))
        
        x, y = self.food
        pygame.draw.rect(self.screen, (255, 0, 0),
                        (x * self.grid_size, y * self.grid_size,
                        self.grid_size - 2, self.grid_size - 2))
        
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over_text = self.font.render("Game Over", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(tick)
        
        pygame.quit()

def main():
    game = Snake()
    game.run()
    
if __name__ == "__main__":
    game = Snake()
    game.run()