import curses
from colors import Colors
from renderer import Renderer
from tables import DASHBOARD
import os

class BoardItem:

    def __init__(self, character):
        self.character = character
        self.init_character = None
        self.config = BoardItemConfig()

class BoardItemConfig:

    def __init__(self):
        self.foreground_color = None
        self.background_color = None
        self.bold = False

    def clear(self):
        self.foreground_color = None
        self.background_color = None
        self.bold = False

class Dashboard:

    HORIZONTAL_RATIO = 0.5
    VERTICAL_RATIO = 0.333

    BG_COLOR = Colors.BLACK
    FG_COLOR = Colors.WHITE

    def __init__(self, data):
        self.data = data
        self.board = self._parse_board()
        self._save_board()

    def set_window(self, window):
        self.window = window
        self.window.bkgd(' ', curses.color_pair(Colors.get_color_pair_id(Dashboard.FG_COLOR.FG, Dashboard.BG_COLOR.BG)))

    def get_number_of_lines(self):
        return len(self.board)

    def _parse_board(self):
        parts = DASHBOARD.split('\n')
        board = []

        for part in parts:
            row = []
            for char in part:
                row.append(BoardItem(char))
            board.append(row)

        return board

    def _save_board(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                self.board[r][c].init_character = self.board[r][c].character

    def _reset_board(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                self.board[r][c].character = self.board[r][c].init_character
                self.board[r][c].config.clear()

    def _set_background(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                self.board[r][c].config.background_color = self.BG_COLOR.BG
                self.board[r][c].config.foreground_color = self.FG_COLOR.FG

    def _get_full_screen_board(self):
        full_rows, full_columns = self.window.getmaxyx()
        full_columns = full_columns - 1

        full_board = []

        for r in range(full_rows):
            row = []
            for c in range(full_columns):
                item = BoardItem(' ')
                item.config.background_color = self.BG_COLOR.BG
                item.config.foreground_color = self.FG_COLOR.FG
                row.append(item)
            full_board.append(row)

        rows_to_draw = min(full_rows, len(self.board))
        columns_to_draw = min(full_columns, len(self.board[0]))

        for r in range(rows_to_draw):
            for c in range(columns_to_draw):
                c_offset = 0
                if full_columns > len(self.board[r]):
                    c_offset = int((full_columns - len(self.board[r])) * self.HORIZONTAL_RATIO)

                r_offset = 0
                if full_rows > len(self.board):
                    r_offset = int((full_rows - len(self.board)) * self.VERTICAL_RATIO)

                full_board[r_offset + r][c_offset + c] = self.board[r][c]

        return full_board

    def _draw(self):
        full_board = self._get_full_screen_board()
        Renderer.generate_standard(full_board, self.window)

    def render(self, render_config):
        self._reset_board()
        self._set_background()
        # TODO: Update board
        self._draw()