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
                if Renderer._is_bold(full_board[r][c].config):
                    window.addstr(full_board[r][c].character.encode('utf-8'), color | curses.A_BOLD)
                else:
                    window.addstr(full_board[r][c].character.encode('utf-8'), color)

    @staticmethod
    def generate_optimized(full_board, window):
        row = 0
        for r in range(len(full_board)):
            window.move(r, 0)
            current_color = curses.color_pair(Colors.get_color_pair_id(full_board[r][0].config.foreground_color, full_board[r][0].config.background_color))
            current_bold = Renderer._is_bold(full_board[r][0].config)
            block = ''
            for c in range(len(full_board[r])):
                color = curses.color_pair(Colors.get_color_pair_id(full_board[r][c].config.foreground_color, full_board[r][c].config.background_color))
                is_bold = Renderer._is_bold(full_board[r][c].config)
                if color == current_color and is_bold == current_bold:
                    block += full_board[r][c].character
                else:
                    if current_bold:
                        window.addstr(block.encode('utf-8'), current_color | curses.A_BOLD)
                    else:
                        window.addstr(block.encode('utf-8'), current_color)
                    current_color = color
                    current_bold = is_bold
                    block = '' + full_board[r][c].character

            # Write last part of row and reset for next row
            if current_bold:
                window.addstr(block.encode('utf-8'), current_color | curses.A_BOLD)
            else:
                window.addstr(block.encode('utf-8'), current_color)

    @staticmethod
    def _is_bold(config):
        # Bold results in the wrong color on Windows
        return config.bold == True and os.name != 'nt'