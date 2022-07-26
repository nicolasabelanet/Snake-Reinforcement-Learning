SHOW_DISPLAY = True

if SHOW_DISPLAY:
    import pygame
import random
from collections import namedtuple
from enum import Enum
import numpy as np


if SHOW_DISPLAY:
    pygame.init()
    font = pygame.font.Font('arial.ttf', 50)

# reset function
# reward
# play(action) -> direction
# game_iteration
# is_collision

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (255, 0 ,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 60
SPEED = 0

class SnakeGameAI:

    def __init__(self, width = 1920, height = 1440):
        self.width = width
        self.height = height 
        
        # init display
        if SHOW_DISPLAY:
            self.display = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption('Snake')
            self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.width / 2, self.height / 2)
        self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - BLOCK_SIZE * 2, self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0



    def _place_food(self):
        
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):

        self.frame_iteration += 1

        # 1. collect user input
        if SHOW_DISPLAY:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
          
        # 2. move our snake
        self._move(action) # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        if SHOW_DISPLAY:
            self._update_ui()
            self.clock.tick(SPEED)

        # 6. reutrn game over and score
        return reward, game_over, self.score

    def is_collision(self, point = None):
        
        if point is None:
            point = self.head

        if point.x > self.width - BLOCK_SIZE \
            or point.x < 0 \
            or point.y > self.height - BLOCK_SIZE \
            or point.y < 0:

            return True

        if point in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)
        
        for point in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, 
                pygame.Rect(point.x + (0.2 * BLOCK_SIZE), point.y + (0.2 * BLOCK_SIZE), BLOCK_SIZE * 0.6, BLOCK_SIZE * 0.6))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE ))

        text = font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_direction = clock_wise[index]
            
        elif np.array_equal(action, [0, 1, 0]):
            next_index = (index + 1) % len(clock_wise)
            new_direction = clock_wise[next_index]
        
        else:
            next_index = (index - 1) % len(clock_wise)
            new_direction = clock_wise[next_index]

        self.direction = new_direction
        
        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self. direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
        