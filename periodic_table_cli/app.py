import sys
import curses
import traceback
from state_controller import StateController
from dashboard import Dashboard
from colors import Colors
import os

DEGUG_MODE = True  # TODO: Set to False, remove unknown color logs from colors.py

class KeyMap:
    ESC       = 27
    SLASH     = 47
    BACKSLASH = 92
    ENTER_LF  = 10
    ENTER_CR  = 13
    BACKSPACE = 8
    DELETE    = 127

    LETTERS = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    ]
    NUMBERS = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]
    SPECIAL_CHARACTERS = [ '-', ' ' ]

class App:

    def __init__(self, config, data):
        self.data = data
        self.state_controller = StateController(data, config)
        self.dashboard = Dashboard(data)

        # Key setup before curses is initialized
        os.environ.setdefault('ESCDELAY', '1')

    def _draw(self, window, full):
        render_config = self.state_controller.get_render_config()
        self._clear_screen(window, full)
        self.dashboard.render(render_config)
        window.refresh()

    def _clear_screen(self, window, full):
        if full:
            window.clear()
        window.move(0, 0)

    def start(self, window):
        curses.curs_set(0)
        Colors.init_colors()
        self.dashboard.set_window(window)
        self._draw(window, True)
        self._handle_keys(window)

    def _handle_keys(self, window):
        while True:
            handled = False
            full = False
            try:
                key = window.getch()
                key_char = self._get_key_char(key)

                if key == curses.KEY_RESIZE:
                    curses.resize_term(0, 0)
                    curses.curs_set(0)
                    handled = True
                    full = True
                elif key == KeyMap.ESC:
                    self.exit()
                elif key == curses.KEY_UP:
                    handled = self.state_controller.process_up()
                elif key == curses.KEY_DOWN:
                    handled = self.state_controller.process_down()
                elif key == curses.KEY_LEFT:
                    handled = self.state_controller.process_left()
                elif key == curses.KEY_RIGHT:
                    handled = self.state_controller.process_right()
                elif key == KeyMap.SLASH:
                    handled = self.state_controller.process_slash()
                elif key == KeyMap.BACKSLASH:
                    handled = self.state_controller.process_backslash()
                elif key == curses.KEY_ENTER or key == KeyMap.ENTER_LF or key == KeyMap.ENTER_CR:
                    handled = self.state_controller.process_enter()
                elif key == curses.KEY_BACKSPACE or key == KeyMap.BACKSPACE or key == KeyMap.DELETE:
                    handled = self.state_controller.process_backspace()
                elif key_char in KeyMap.LETTERS or key_char in KeyMap.NUMBERS or key_char in KeyMap.SPECIAL_CHARACTERS:
                    handled = self.state_controller.process_search_input(key_char)

                if handled:
                    self._draw(window, full)
            except KeyboardInterrupt:
                self.exit()  # CTRL-C
            except Exception as e:
                if DEGUG_MODE:
                    self.exit(traceback.format_exc())
                else:
                    self.exit('An error occurred, exiting.')

    def _get_key_char(self, key):
        try:
            return chr(key)
        except:
            return None

    def exit(self, message=None):
        if message:
            print(message)
        sys.exit()
