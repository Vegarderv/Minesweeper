"""GameBoard for MineSweeper"""
import numpy as np
import random
import time


class Board:
    """ Parent Class for game boards"""

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.game_board = np.zeros([self.width, self.height])
        self.init = False

    def _get_surrounding_tiles(self, x, y):
        """Returns an array of the surrounding tiles"""
        surrounding_tiles = []
        if x != 0:
            surrounding_tiles.append(self.game_board[x - 1][y])
            if y != 0:
                surrounding_tiles.append(self.game_board[x - 1][y - 1])
            if y != self.height - 1:
                surrounding_tiles.append(self.game_board[x - 1][y + 1])
        if x != self.width - 1:
            surrounding_tiles.append(self.game_board[x + 1][y])
            if y != 0:
                surrounding_tiles.append(self.game_board[x + 1][y - 1])
            if y != self.height - 1:
                surrounding_tiles.append(self.game_board[x + 1][y + 1])
        if y != 0:
            surrounding_tiles.append(self.game_board[x][y - 1])
        if y != self.height - 1:
            surrounding_tiles.append(self.game_board[x][y + 1])
        return surrounding_tiles


class GameBoard(Board):
    """Game board containing the game information"""

    def __init__(self, no_bombs, width, heigth):
        Board.__init__(self, width, heigth)
        self.no_bombs = no_bombs

    def initiate_board(self, start_x, start_y):
        """Initiates board with bombs and numbers"""
        list_of_coords = []
        for x in range(self.width):
            for y in range(self.height):
                if not ((x == start_x or x == start_x + 1 or x == start_x - 1 or x == start_x + 2 or x == start_x - 2)
                        and (y == start_y or y == start_y + 1 or y == start_y - 1 or y == start_y + 2 or y == start_y - 2)):
                    list_of_coords.append((x, y))
        bomb_coords = random.sample(list_of_coords, self.no_bombs)
        for cords in bomb_coords:
            self.game_board[cords[0]][cords[1]] = -1
        self._finish_board()
        self.init = True

    def get_board(self):
        return self.game_board

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def is_init(self):
        return self.init

    def _finish_board(self):
        """Gives each tile its respective number"""
        for x in range(self.width):
            for y in range(self.height):
                if self.game_board[x][y] != -1:
                    self._find_surrounding_bombs(x, y)

    def _find_surrounding_bombs(self, x, y):
        """Finds number of surrounding bombs"""
        self.game_board[x][y] = self._get_surrounding_tiles(x, y).count(-1)

    def get_field(self, x, y):
        return self.game_board[x][y]


class ClickBoard(Board):
    """Board that contains the information if a tile is clicked or not"""

    def __init__(self, width, height, game_board: GameBoard):
        Board.__init__(self, width, height)
        self.gamer_board = game_board

    def initiate_board(self):
        """Creates an un-clicked board"""

        for x in range(self.width):
            for y in range(self.height):
                self.game_board[x][y] = 0

    def click_board(self, x, y):
        """Removed the tile of a clicked tile"""
        if not self.gamer_board.init:
            self.gamer_board.initiate_board(x, y)
        if self.game_board[x][y] == 0:
            self.game_board[x][y] = 1
            if self.gamer_board.get_field(x, y) == 0:
                self._clear_fields(x, y)

    def right_click_board(self, x, y):
        """Marks a tile with a bomb"""
        if self.game_board[x][y] == 0:
            self.game_board[x][y] = 2
        elif self.game_board[x][y] == 2:
            self.game_board[x][y] = 0

    def is_clicked(self, x, y):
        return self.game_board[x][y]

    def _clear_fields(self, check_x, check_y):
        """Algorithm that finds all empty spaces next to an empty space, and removes all tiles around it"""
        # Clears all empty spaces
        for i in range(10):
            # check one way
            for x in range(self.width):
                for y in range(check_y, self.height):
                    fields = self._get_surrounding_tiles(x, y)
                    gb_fields = self.gamer_board._get_surrounding_tiles(x, y)
                    for num in range(len(fields)):
                        if fields[num] == 1 and gb_fields[num] == 0:
                            self.game_board[x][y] = 1
            # check other way
            for x in range(self.width - 1, -1, -1):
                for y in range(check_y - 1, -1, -1):
                    fields = self._get_surrounding_tiles(x, y)
                    gb_fields = self.gamer_board._get_surrounding_tiles(x, y)
                    for num in range(len(fields)):
                        if fields[num] == 1 and gb_fields[num] == 0:
                            self.game_board[x][y] = 1

    def is_finished(self):
        """Checks if number of un-clicked/right clicked tiles is the same
        as number of bombs. In other words, the game is finished and the player
        has completed the puzzle"""
        no_tiles = 0
        for row in self.game_board:
            no_tiles += list(row).count(0) + list(row).count(2)
        return no_tiles == self.gamer_board.no_bombs





