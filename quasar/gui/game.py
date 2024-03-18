"""
This module contains the Game class, 
which is responsible for the game loop and 
the game's main logic.
"""

import sys
import pygame
import numpy as np
from quasar.chess import Board, Point, PieceName, Piece
from quasar.chess.utils import STARTING_FEN
from quasar.chess.moves import Move
from quasar.chess.errors import InvalidMoveError
from .colors import BLACK_TILE, WHITE_TILE, SELECTED_TILE, ACCENT_COLOR

class Game:
    """
    The Game class is responsible for the game loop and the game's main logic.
    """
    def __init__(self) -> None:
        """
        The constructor for the Game class.
        """
        self.board = Board()
        self.board.load_fen(STARTING_FEN)
        self.display = pygame.display.set_mode((600, 600))

        self.square_size = self.display.get_width()//8
        self.offset = Point(-1,8) * self.square_size
        self.scale = 1

        self.selected_tile = None

        self.last_mouse = Point(0,0)

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.load_images()
    
    def board_to_pygame(self, point: Point) -> Point:
        """
        Convert a point from the board to the pygame coordinate system.

        :param point: The point to convert.
        :type point: Point
        :return: The point in the pygame coordinate system.
        :rtype: Point
        """
        return Point(point.x, -point.y)

    def load_images(self) -> list:
        """
        Load the images for the pieces.

        :return: self.images
        :rtype: list
        """
        self.images = []
        colors = ['b','w']
        pieces = ['b', 'k', 'n', 'p', 'q', 'r']
        for color in colors:
            for piece in pieces:
                path = f"quasar/gui/assets/{color}{piece}.png"
                img = pygame.image.load(path)
                self.images.append(img)
        return self.images

    def get_image(self, piece: Piece) -> pygame.Surface:
        """
        Get the image for the piece.

        :param piece: The piece to get the image for.
        :type piece: Piece
        :return: The image for the piece.
        :rtype: pygame.Surface
        """
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

    def get_visible_tiles(self) -> list:
        """
        Get the visible tiles on the board.

        :return: The visible tiles on the board.
        :rtype: list
        """
        scaled_tile = self.scale * self.square_size
        visible_tiles = []

        n = self.display.get_width() // scaled_tile
        m = self.display.get_height() // scaled_tile

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
            if x + scaled_tile > 0 and x < self.display.get_width():
                if y + scaled_tile > 0 and y < self.display.get_height():
                    visible_tiles.append(tile)
        return visible_tiles

    def get_tile_at_mouse(self) -> Point:
        """
        Get the tile at the mouse position.

        :return: The tile at the mouse position.
        :rtype: Point
        """
        mouse_pos = Point(*pygame.mouse.get_pos())
        tile = Point(
            int((mouse_pos.x - self.offset.x) // (self.scale * self.square_size)),
            int((mouse_pos.y - self.offset.y) // (self.scale * self.square_size)))
        return self.board_to_pygame(tile)

    def draw_board(self) -> None:
        """
        Draw the board on the display.
        """
        self.display.fill((255, 255, 255))
        selected_piece = self.board.get_piece_at(self.selected_tile)
        scaled_tile = self.scale * self.square_size
        visible_tiles = self.get_visible_tiles()
        min_x_visible = min([self.board_to_pygame(tile).x for tile in visible_tiles])
        max_x_visible = max([self.board_to_pygame(tile).x for tile in visible_tiles])
        min_y_visible = min([self.board_to_pygame(tile).y for tile in visible_tiles])
        max_y_visible = max([self.board_to_pygame(tile).y for tile in visible_tiles])
        possible_move_generator = self.board.get_possible_moves_generator(
            selected_piece,
            Point(min_x_visible, min_y_visible),
            Point(max_x_visible, max_y_visible))
        for tile in visible_tiles:
            tile = self.board_to_pygame(tile)
            color = WHITE_TILE if (tile.y%2) == (tile.x%2) else BLACK_TILE
            if tile == self.selected_tile:
                color = SELECTED_TILE
            tile = self.board_to_pygame(tile)
            x = tile.x * scaled_tile + self.offset.x
            y = tile.y * scaled_tile + self.offset.y
            x = np.ceil(x)
            y = np.ceil(y)
            scaled_tile = np.ceil(scaled_tile)
            pygame.draw.rect(self.display, color, (x, y, scaled_tile, scaled_tile))
            tile = self.board_to_pygame(tile)

            piece = self.board.get_piece_at(tile)
            if piece.name != PieceName.NONE:
                img = self.get_image(piece)
                img = pygame.transform.smoothscale(img, (scaled_tile, scaled_tile))
                self.display.blit(img, (x,y))
        if not selected_piece.is_none() and selected_piece.color == self.board.current_player:
            while True:
                try:
                    move = next(possible_move_generator)
                    target = move.target
                    target = self.board_to_pygame(move.target)
                    x = target.x * scaled_tile + self.offset.x
                    y = target.y * scaled_tile + self.offset.y
                    x = np.ceil(x)
                    y = np.ceil(y)
                    scaled_tile = np.ceil(scaled_tile)
                    pygame.draw.circle(
                        self.display, ACCENT_COLOR,
                        (x + scaled_tile//2, y + scaled_tile//2),
                        scaled_tile//4)
                except StopIteration:
                    break

    def update(self) -> None:
        """
        Update the display.
        """
        self.draw_board()
        pygame.display.flip()

    def handle_rmb(self, event: pygame.event.Event) -> None:
        """
        Handle the right mouse button event.

        :param event: The event to handle.
        :type event: pygame.event.Event
        """
        if event.button == 3:
            self.last_mouse = Point(*pygame.mouse.get_pos())

    def handle_lmb(self, event: pygame.event.Event) -> None:
        """
        Handle the left mouse button event.

        :param event: The event to handle.
        :type event: pygame.event.Event
        """
        if event.button == 1:
            mouse_pos = Point(*pygame.mouse.get_pos())
            tile = Point(
                int((mouse_pos.x - self.offset.x) // (self.scale * self.square_size)),
                int((mouse_pos.y - self.offset.y) // (self.scale * self.square_size)))
            tile = self.board_to_pygame(tile)

            piece = self.board.get_piece_at(self.selected_tile)
            if piece.name != PieceName.NONE and \
                piece.color == self.board.current_player:
                move = Move(piece.color, self.selected_tile, tile)
                if self.board.is_possible_move(move):
                    try:
                        self.board.make_move(move)
                    except InvalidMoveError:
                        pass
            if tile == self.selected_tile:
                self.selected_tile = None
            else:
                self.selected_tile = tile

    def handle_mousemotion(self, event: pygame.event.Event) -> None:
        """
        Handle the mouse motion event.

        :param event: The event to handle.
        :type event: pygame.event.Event
        """
        if event.buttons[2]:
            mouse = Point(*pygame.mouse.get_pos())
            self.offset += mouse - self.last_mouse
            self.last_mouse = mouse

    def handle_mousewheel(self, event: pygame.event.Event) -> None:
        """
        Handle the mouse wheel event.

        :param event: The event to handle.
        :type event: pygame.event.Event
        """
        self.scale *= 1 + event.y * 0.1
        self.scale = max(0.1, self.scale)
        self.scale = min(10, self.scale)
        if self.scale == 0.1:
            self.square_size *= 0.1
            self.scale = 1
        if self.scale == 10:
            self.square_size *= 10
            self.scale = 1

    def handle_input(self) -> None:
        """
        Handle the input events.
        """
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_rmb(event)
                self.handle_lmb(event)
            if event.type == pygame.MOUSEMOTION:
                self.handle_mousemotion(event)
            if event.type == pygame.MOUSEWHEEL:
                self.handle_mousewheel(event)

    def run(self) -> None:
        """
        Run the game loop.
        """
        running = True
        while running:
            if pygame.event.get(pygame.QUIT):
                running = False
            self.handle_input()
            self.update()
            caption = str(round(self.clock.get_fps(), 2)) + str(self.get_tile_at_mouse())
            pygame.display.set_caption(caption)
            self.clock.tick(self.fps)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
