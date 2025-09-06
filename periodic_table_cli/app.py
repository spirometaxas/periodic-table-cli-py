import sys
import curses
import traceback
from .state_controller import StateController
from .dashboard import Dashboard
from .colors import Colors
import os

class MinimumSupportedDimensions:
    ROWS    = 46
    COLUMNS = 156

DEGUG_MODE = False

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

    COMMA        = 44
    PERIOD       = 46
    LEFT_CARROT  = 60
    RIGHT_CARROT = 62

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
            window.bkgd(' ', curses.color_pair(Colors.get_color_pair_id(Colors.WHITE.FG, Colors.DEEP_BLACK.BG)))
        window.move(0, 0)

    def start(self, window):
        try:
            Colors.init_colors()
        except:
            self.exit(window, '\n Error: Interactive mode is only supported on terminals that support 256 colors.\n')

        curses.curs_set(0)
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
                curses.flushinp()

                if key == curses.KEY_RESIZE:
                    curses.curs_set(0)
                    self.dashboard.update_scrolling_on_resize()
                    handled = True
                    full = True
                elif key == KeyMap.ESC:
                    self.exit(window)
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
                elif key == KeyMap.COMMA:
                    handled = self.dashboard.scroll_up()
                elif key == KeyMap.PERIOD:
                    handled = self.dashboard.scroll_down()
                elif key == KeyMap.LEFT_CARROT:
                    handled = self.dashboard.scroll_left()
                elif key == KeyMap.RIGHT_CARROT:
                    handled = self.dashboard.scroll_right()

                if handled:
                    self._draw(window, full)
            except KeyboardInterrupt:
                self.exit(window)  # CTRL-C
            except Exception as e:
                if DEGUG_MODE:
                    self.exit(window, traceback.format_exc())
                else:
                    self.exit(window, 'An error occurred, exiting.')

    def _get_key_char(self, key):
        try:
            return chr(key)
        except:
            return None

    def exit(self, window, message=None):
        full_rows, full_columns = window.getmaxyx()
        if message:
            sys.exit(message)
        elif full_rows < MinimumSupportedDimensions.ROWS or full_columns < MinimumSupportedDimensions.COLUMNS:
            sys.exit('\n' +
                ' Tip: Current screen dimensions are smaller than minimum supported dimensions, and some screen components may have been cut off.\n' +
                ' To fix this, either make the screen bigger or use scrolling to pan across the screen:\n' +
                '   - Use COMMA (,) to scroll up\n' +
                '   - Use PERIOD (.) to scroll down\n' +
                '   - Use LEFT CARROT (<) to scroll left\n' +
                '   - Use RIGHT CARROT (>) to scroll right\n')
        sys.exit()
