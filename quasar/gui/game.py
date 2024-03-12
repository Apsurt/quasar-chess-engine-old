import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from quasar.chess import Board
from quasar.chess import Point

class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.display = pygame.display.set_mode((800, 800))

        self.view_center = Point(4, 4)
        self.square_size = 100

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True
    
    def move_board(self, x, y):
        self.view_center += Point(x, y)
    
    def draw_board(self):
        pass

    def update(self):
        self.draw_board()
        pygame.display.flip()
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.update()

            self.clock.tick(self.fps)
        pygame.quit()
        quit()

if __name__ == "__main__":
    game = Game()
    game.run()