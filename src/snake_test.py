# Snake test methods

import unittest
import pygame

from snake_project import Snake

class TestSnake(unittest.TestCase):

    def test_initial_direction_is_down(self):
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 1)
        self.assertEqual(self.snake.direction, 'down')

if __name__ == '__main__':
    unittest.main()