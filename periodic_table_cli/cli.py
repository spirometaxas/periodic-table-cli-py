import sys
import os
import json
import curses
from .data_processor import DataProcessor
from .chart_processor import ChartProcessor
from .app import App
import locale

class AppConfig:

    def __init__(self, atomic_number, symbol, name):
        self.atomic_number = atomic_number
        self.symbol = symbol
        self.name = name

class DataConfig(AppConfig):

    def __init__(self, atomic_number, symbol, name, verbose):
        super().__init__(atomic_number, symbol, name)
        self.verbose = verbose

class ChartConfig(AppConfig):

    def __init__(self, atomic_number, symbol, name, small):
        super().__init__(atomic_number, symbol, name)
        self.small = small

class MODES:
    APP   = 'APP'
    DATA  = 'DATA'
    CHART = 'CHART'

DATA_FILE = 'data.json'

def print_usage():
    print('\n'\
        '           ╔═╗                               ╔═╗ \n'\
        '           ╠═╬═╗                   ╔═╦═╦═╦═╦═╬═╣ \n'\
        '           ╠═╬═╣                   ╠═╬═╬═╬═╬═╬═╣ \n'\
        '           ╠═╬═╬═╦═╦═╦═╦═╦═╦═╦═╦═╦═╬═╬═╬═╬═╬═╬═╣ \n'\
        '           ╠═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╣ \n'\
        '           ╠═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╣ \n'\
        '           ╠═╬═╣:╠═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╣ \n'\
        '           ╚═╩═╝ ╚═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╝ \n'\
        '               ╔═╦═╦═╦═╦═╦═╦═╦═╦═╦═╦═╦═╦═╦═╦═╗   \n'\
        '              :╠═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╬═╣   \n'\
        '               ╚═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╩═╝   \n'\
        '\n'\
        ' An interactive Periodic Table of Elements app for the console!\n'\
        '\n'\
        ' Interactive Controls:\n'\
        '   - Navigation: Use <UP>|<DOWN>|<LEFT>|<RIGHT> arrows\n'\
        '\n'\
        '   - Display Mode: Use SLASH </> to toggle the display mode forwards\n'\
        '                   Use BACKSLASH <\\> to toggle the display mode in reverse\n'\
        '\n'\
        '   - Search: Query with letters or numbers\n'\
        '             Use <UP>|<DOWN> arrows to navigate results\n'\
        '             Press <ENTER> to select\n'\
        '             Press <LEFT> to exit search\n'\
        '\n'\
        '   - Quit: Press <ESC> or <CTRL+C>\n'\
        '\n'\
        ' Usage:\n'\
        '   $ periodic-table-cli\n'\
        '   $ periodic-table-cli [options]\n'\
        '\n'\
        ' Options:\n'\
        '   --mode=<mode>          Set the mode for the application.  Supports three values:\n'\
        '                            - app:    Run in interactive mode (default)\n'\
        '                            - data:   Display data for a specified element\n'\
        '                            - chart:  Prints a non-interactive table only\n'\
        '   --atomic-number=<int>  Initialize the Periodic Table at the specified atomic number (1-118)\n'\
        '   --symbol=<symbol>      Initialize the Periodic Table at the specified element symbol\n'\
        '   --name=<name>          Initialize the Periodic Table at the specified element name\n'\
        '   --small, -s            Print a smaller Periodic Table of Elements (include --mode=chart)\n'\
        '   --verbose, -v          Print a complete data chart with all elements (include --mode=data)\n'\
        '\n'\
        ' Full Docs: https://spirometaxas.com/projects/periodic-table-cli\n\n'\
        ' Last updated January 2024\n'\
        ' ' + get_version() + '\n')

def get_version():
    return 'v2.0.6 (Python)'

def get_flags(params):
    return [param for param in params if param.startswith('-')]

def is_small(flags):
    return any(flag.lower() in ('-s', '--small') for flag in flags)

def is_help(flags):
    return any(flag.lower() in ('--help', '-h') for flag in flags)

def is_verbose(flags, mode):
    return mode == MODES.DATA and any(flag.lower() in ('--verbose', '-v') for flag in flags)

def is_version(flags, mode):
    return mode == MODES.APP and any(flag.lower() in ('--version', '-v') for flag in flags)

def get_mode(flags):
    prefix = '--mode='
    for flag in flags:
        if flag and flag.lower().startswith(prefix):
            mode_string = flag[len(prefix):]
            if mode_string is not None:
                if mode_string.upper() == MODES.DATA:
                    return MODES.DATA
                elif mode_string.upper() == MODES.CHART:
                    return MODES.CHART
                elif mode_string.upper() == MODES.APP:
                    return MODES.APP
    return MODES.APP  # Default to APP

def get_atomic_number(flags):
    prefix = '--atomic-number='
    for flag in flags:
        if flag and flag.lower().startswith(prefix):
            atomic_number_string = flag[len(prefix):]
            if atomic_number_string is not None and atomic_number_string.isdigit():
                return int(atomic_number_string)
    return None

def get_name(flags):
    prefix = '--name='
    for flag in flags:
        if flag and flag.lower().startswith(prefix):
            name_string = flag[len(prefix):]
            if name_string is not None:
                return name_string
    return None

def get_symbol(flags):
    prefix = '--symbol='
    for flag in flags:
        if flag and flag.lower().startswith(prefix):
            symbol_string = flag[len(prefix):]
            if symbol_string is not None:
                return symbol_string
    return None

def load_data():
    current_dir = os.path.join(os.path.dirname(__file__), '')
    data_file_path = os.path.join(current_dir, DATA_FILE)
    try:
        f = open(data_file_path)
        data = json.load(f)
        f.close()
        return data
    except:
        print('\n Error loading data file.\n')
        sys.exit()

def _wrapper(func):
    # Using workaround to address windows-curses bug on Python 3.12
    # More info: https://github.com/zephyrproject-rtos/windows-curses/issues/50
    if os.name == 'nt' and sys.version_info[0] == 3 and sys.version_info[1] >= 12:
        stdscr = None
        try:
            import _curses
            # This crashes on Python 3.12.
            # setupterm(term=_os.environ.get("TERM", "unknown"),
            # fd=_sys.__stdout__.fileno())
            stdscr = _curses.initscr()
            for key, value in _curses.__dict__.items():
                if key[0:4] == 'ACS_' or key in ('LINES', 'COLS'):
                    setattr(curses, key, value)

            curses.noecho()
            curses.cbreak()
            
            if stdscr is not None:
                stdscr.keypad(True)
                func(stdscr)
        finally:
            if stdscr is not None:
                stdscr.keypad(False)
            curses.nocbreak()
            curses.echo()
            curses.endwin()
    else:
        curses.wrapper(func)

def main():
    os.system('')  # Enable ANSI escape sequences on Windows
    locale.setlocale(locale.LC_ALL, '')

    mode = MODES.APP
    atomic_number = None
    name = None
    symbol = None
    small = False
    verbose = False

    if len(sys.argv) > 1:
        params = sys.argv[1:]
        mode = get_mode(params)
        atomic_number = get_atomic_number(params)
        name = get_name(params)
        symbol = get_symbol(params)
        small = is_small(params)
        verbose = is_verbose(params, mode)

        if is_help(params):
            print_usage()
            sys.exit()
        elif is_version(params, mode):
            print('\n ' + get_version() + '\n')
            sys.exit()
        elif mode == MODES.DATA:
            data = load_data()
            print(DataProcessor.format_data(DataConfig(atomic_number, symbol, name, verbose), data))
            sys.exit()
        elif mode == MODES.CHART:
            data = load_data()
            print(ChartProcessor.format_chart(ChartConfig(atomic_number, symbol, name, small), data))
            sys.exit()

    if not sys.stdout.isatty():
        print('\n Error: Interactive mode is only supported within a terminal screen.\n')
        sys.exit()

    data = load_data()
    app = App(AppConfig(atomic_number, symbol, name), data)
    _wrapper(app.start)

if __name__ == '__main__':
    main()