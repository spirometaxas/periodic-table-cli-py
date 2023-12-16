import curses
import os
from colors import Colors

class Renderer:

    @staticmethod
    def generate_standard(full_board, window):
        row = 0
        for r in range(len(full_board)):
            window.move(r, 0)
            for c in range(len(full_board[r])):
                color = curses.color_pair(Colors.get_color_pair_id(full_board[r][c].config.foreground_color, full_board[r][c].config.background_color))
                if full_board[r][c].config.bold and os.name != 'nt':
                    # Bold results in the wrong color on Windows
                    window.addstr(full_board[r][c].character.encode('utf-8'), color | curses.A_BOLD)
                else:
                    window.addstr(full_board[r][c].character.encode('utf-8'), color)