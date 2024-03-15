import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from chess import Board
from chess import Point
from chess import PieceName
from chess.utils import starting_fen
from .colors import *
import numpy as np

pygame.init()

class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.board.load_fen(starting_fen)
        self.display = pygame.display.set_mode((600, 600))

        self.square_size = self.display.get_width()//8
        self.offset = Point(-self.square_size, -self.square_size)
        self.scale = 1

        self.last_mouse = Point(0, 0)

        self.selected_tile = None

        self.clock = pygame.time.Clock()
        self.fps = 6000
        self.running = True

        self.images = self.load_images()
    
    def load_images(self):
        images = []
        colors = ['b','w']
        pieces = ['b', 'k', 'n', 'p', 'q', 'r']
        for color in colors:
            for piece in pieces:
                path = f"quasar/gui/assets/{color}{piece}.png"
                img = pygame.image.load(path)
                images.append(img)
        return images

    def get_image(self, piece):
        pieces = ['b', 'k', 'n', 'p', 'q', 'r']
        if piece.color.name[0].lower() == 'b':
            i = 0
        else:
            i = 6
        if piece.name == PieceName.KNIGHT:
            piece_nickname = 'n'
        else:
            piece_nickname = piece.name.name[0].lower()
        i += pieces.index(piece_nickname)
        return self.images[i]
    
    def get_visible_tiles(self):
        scaled_tile = self.scale * self.square_size
        visible_tiles = []

        n = (self.display.get_width() // scaled_tile)
        m = (self.display.get_height() // scaled_tile)

        n_min = int(np.floor(0 - (self.offset.x//scaled_tile)))
        n_max = int(np.ceil(n - (self.offset.x//scaled_tile)))
        m_min = int(np.floor(0 - (self.offset.y//scaled_tile)))
        m_max = int(np.ceil(m - (self.offset.y//scaled_tile)))

        tiles = []
        for y in range(m_min-1, m_max+1):
            for x in range(n_min-1, n_max+1):
                tiles.append(Point(x,y))
        for tile in tiles:
            x = tile.x * scaled_tile + self.offset.x
            y = tile.y * scaled_tile + self.offset.y
            if x + scaled_tile > 0 and x < self.display.get_width() and y + scaled_tile > 0 and y < self.display.get_height():
                visible_tiles.append(tile)
        
        return visible_tiles

    def draw_board(self):
        self.display.fill((255, 255, 255))
        selected_piece = self.board.get_piece_at(self.selected_tile)
        possible_move_generator = self.board.get_possible_moves_generator(selected_piece)
        scaled_tile = self.scale * self.square_size
        visible_tiles = self.get_visible_tiles()
        for tile in visible_tiles:
            color = white_tile if (tile.y%2) == (tile.x%2) else black_tile
            if tile == self.selected_tile:
                color = selected_tile
            x = tile.x * scaled_tile + self.offset.x
            y = tile.y * scaled_tile + self.offset.y
            x = np.ceil(x)
            y = np.ceil(y)
            scaled_tile = np.ceil(scaled_tile)
            pygame.draw.rect(self.display, color, (x, y, scaled_tile, scaled_tile))
            
            piece = self.board.get_piece_at(tile)
            if piece.name != PieceName.NONE:
                img = self.get_image(piece)
                img = pygame.transform.smoothscale(img, (scaled_tile, scaled_tile))
                self.display.blit(img, (x,y))

    def update(self):
        self.draw_board()
        pygame.display.flip()
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.last_mouse = Point(*pygame.mouse.get_pos())
                if event.type == pygame.MOUSEMOTION:
                    if event.buttons[0]:
                        mouse = Point(*pygame.mouse.get_pos())
                        self.offset += mouse - self.last_mouse
                        self.last_mouse = mouse
                if event.type == pygame.MOUSEWHEEL:
                    self.scale *= 1 + event.y * 0.1
                    self.scale = max(0.1, self.scale)
                    self.scale = min(10, self.scale)
                    if self.scale == 0.1:
                        self.square_size *= 0.1
                        self.scale = 1
                    if self.scale == 10:
                        self.square_size *= 10
                        self.scale = 1
            
            self.update()
            pygame.display.set_caption(str(round(self.clock.get_fps(), 2)))
            self.clock.tick(self.fps)
        pygame.quit()
        quit()

if __name__ == "__main__":
    game = Game()
    game.run()