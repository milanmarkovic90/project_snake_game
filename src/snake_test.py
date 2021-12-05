# Snake test methods

import unittest
import pygame

from snake_project import Snake

class TestSnake(unittest.TestCase):

    def test_initial_direction_is_down(self):
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 1)
        self.assertEqual(self.snake.direction, 'down')

    def test_moving_up_changes_direction_to_up(self):
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 1)
        self.snake.move_right()
        self.snake.move_up()
        self.assertEqual(self.snake.direction, 'up')

    def test_moving_up_when_direction_is_down_then_keep_moving_down(self):
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 1)
        self.snake.move_down()
        self.snake.move_up()
        self.assertEqual(self.snake.direction, 'down')

    def test_moving_left_changes_direction_to_left(self):
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 1)
        self.snake.move_left()
        self.assertEqual(self.snake.direction, 'left')

    def test_moving_right_changes_direction_to_right(self):
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 1)
        self.snake.move_right()
        self.assertEqual(self.snake.direction, 'right')

if __name__ == '__main__':
    unittest.main()