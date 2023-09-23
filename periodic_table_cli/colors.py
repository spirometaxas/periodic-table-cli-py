import curses

class Color:

    def __init__(self, config):
        self.FG = config['FG']
        self.BG = config['BG']
        self.ANSI = config['ANSI']
        self.R = Color._base_255_to_1000(config['R'])
        self.G = Color._base_255_to_1000(config['G'])
        self.B = Color._base_255_to_1000(config['B'])

    @staticmethod
    def _base_255_to_1000(val):
        return int((val / 255.0) * 1000)

class Colors:
    BLACK       = Color({ 'FG':  0, 'BG':  0, 'ANSI':   0, 'R':   0, 'G':   0, 'B':   0 })  # Use default black
    WHITE       = Color({ 'FG': 11, 'BG': 11, 'ANSI': 255, 'R': 238, 'G': 238, 'B': 238 })
    GRAY        = Color({ 'FG': 12, 'BG': 12, 'ANSI': 244, 'R': 128, 'G': 128, 'B': 128 })
    LIGHT_GRAY  = Color({ 'FG': 13, 'BG': 13, 'ANSI': 250, 'R': 188, 'G': 188, 'B': 188 })
    FOCUS_GOLD  = Color({ 'FG': 14, 'BG': 14, 'ANSI': 214, 'R': 255, 'G': 175, 'B':   0 })
    FOCUS_BLUE  = Color({ 'FG': 15, 'BG': 15, 'ANSI':  33, 'R': 0,   'G': 135, 'B': 255 })

    RED         = Color({ 'FG': 16, 'BG': 16, 'ANSI': 196, 'R': 255, 'G':   0, 'B':   0 })
    DARK_RED    = Color({ 'FG': 17, 'BG': 17, 'ANSI':  88, 'R': 135, 'G':   0, 'B':   0 })
    ORANGE      = Color({ 'FG': 18, 'BG': 18, 'ANSI': 208, 'R': 255, 'G': 135, 'B':   0 })
    YELLOW      = Color({ 'FG': 19, 'BG': 19, 'ANSI': 226, 'R': 255, 'G': 255, 'B':   0 })
    DARK_YELLOW = Color({ 'FG': 20, 'BG': 20, 'ANSI': 136, 'R': 175, 'G': 135, 'B':   0 })
    GREEN       = Color({ 'FG': 21, 'BG': 21, 'ANSI':  40, 'R':   0, 'G': 215, 'B':   0 })
    MID_GREEN   = Color({ 'FG': 22, 'BG': 22, 'ANSI':  34, 'R':   0, 'G': 175, 'B':   0 })
    DARK_GREEN  = Color({ 'FG': 23, 'BG': 23, 'ANSI':  28, 'R':   0, 'G': 135, 'B':   0 })
    SKY_BLUE    = Color({ 'FG': 24, 'BG': 24, 'ANSI':  51, 'R':   0, 'G': 255, 'B': 255 })
    BLUE        = Color({ 'FG': 25, 'BG': 25, 'ANSI':  27, 'R':   0, 'G':  95, 'B': 255 })
    MAGENTA     = Color({ 'FG': 26, 'BG': 26, 'ANSI': 207, 'R': 255, 'G':  95, 'B': 255 })
    PURPLE      = Color({ 'FG': 27, 'BG': 27, 'ANSI':  93, 'R': 135, 'G':   0, 'B': 255 })

    COLORS = [ 
        BLACK, WHITE, GRAY, LIGHT_GRAY, FOCUS_GOLD, FOCUS_BLUE,
        RED, DARK_RED, ORANGE, YELLOW, DARK_YELLOW, GREEN,
        MID_GREEN, DARK_GREEN, SKY_BLUE, BLUE, MAGENTA, PURPLE,
    ]

    METER_COLORS = [
        Color({ 'FG': 28, 'BG': 28, 'ANSI': 51,  'R':   0, 'G': 255, 'B': 255 }),
        Color({ 'FG': 29, 'BG': 29, 'ANSI': 50,  'R':   0, 'G': 255, 'B': 215 }),
        Color({ 'FG': 30, 'BG': 30, 'ANSI': 49,  'R':   0, 'G': 255, 'B': 175 }),
        Color({ 'FG': 31, 'BG': 31, 'ANSI': 48,  'R':   0, 'G': 255, 'B': 135 }),
        Color({ 'FG': 32, 'BG': 32, 'ANSI': 47,  'R':   0, 'G': 255, 'B':  95 }),
        Color({ 'FG': 33, 'BG': 33, 'ANSI': 46,  'R':   0, 'G': 255, 'B':   0 }),
        Color({ 'FG': 34, 'BG': 34, 'ANSI': 82,  'R':  95, 'G': 255, 'B':   0 }),
        Color({ 'FG': 35, 'BG': 35, 'ANSI': 118, 'R': 135, 'G': 255, 'B':   0 }),
        Color({ 'FG': 36, 'BG': 36, 'ANSI': 154, 'R': 175, 'G': 255, 'B':   0 }),
        Color({ 'FG': 37, 'BG': 37, 'ANSI': 190, 'R': 215, 'G': 255, 'B':   0 }),
        Color({ 'FG': 38, 'BG': 38, 'ANSI': 226, 'R': 255, 'G': 255, 'B':   0 }),
        Color({ 'FG': 39, 'BG': 39, 'ANSI': 220, 'R': 255, 'G': 215, 'B':   0 }),
        Color({ 'FG': 40, 'BG': 40, 'ANSI': 214, 'R': 255, 'G': 175, 'B':   0 }),
        Color({ 'FG': 41, 'BG': 41, 'ANSI': 208, 'R': 255, 'G': 135, 'B':   0 }),
        Color({ 'FG': 42, 'BG': 42, 'ANSI': 202, 'R': 255, 'G':  95, 'B':   0 }),
        Color({ 'FG': 43, 'BG': 43, 'ANSI': 196, 'R': 255, 'G':   0, 'B':   0 }),
    ]

    COLOR_TO_PAIR_ID = {}

    @staticmethod
    def init_colors():
        for color in Colors.COLORS:
            if color.FG > 10:
                curses.init_color(color.FG, color.R, color.G, color.B)

        for color in Colors.METER_COLORS:
            curses.init_color(color.FG, color.R, color.G, color.B)

        color_pair_id = 10  # Start after the default colors 0-7

        # Foreground colors
        for fg_color in Colors.COLORS:
            curses.init_pair(color_pair_id, fg_color.FG, Colors.BLACK.BG)
            Colors.COLOR_TO_PAIR_ID[Colors._create_color_pair_key(fg_color.FG, Colors.BLACK.BG)] = color_pair_id
            color_pair_id = color_pair_id + 1

        # Background colors
        for bg_color in Colors.COLORS:
            curses.init_pair(color_pair_id, Colors.BLACK.FG, bg_color.BG)
            Colors.COLOR_TO_PAIR_ID[Colors._create_color_pair_key(Colors.BLACK.FG, bg_color.BG)] = color_pair_id
            color_pair_id = color_pair_id + 1

        # Background meter colors
        for meter_color in Colors.METER_COLORS:
            curses.init_pair(color_pair_id, Colors.BLACK.FG, meter_color.BG)
            Colors.COLOR_TO_PAIR_ID[Colors._create_color_pair_key(Colors.BLACK.FG, meter_color.BG)] = color_pair_id
            color_pair_id = color_pair_id + 1

        # Search colors
        curses.init_pair(color_pair_id, Colors.MID_GREEN.FG, Colors.WHITE.BG)
        Colors.COLOR_TO_PAIR_ID[Colors._create_color_pair_key(Colors.MID_GREEN.FG, Colors.WHITE.BG)] = color_pair_id

    @staticmethod
    def _create_color_pair_key(fg_color_id, bg_color_id):
        return str(fg_color_id) + '_' + str(bg_color_id)

    @staticmethod
    def get_color_pair_id(fg_color_id, bg_color_id):
        color_pair_key = Colors._create_color_pair_key(fg_color_id, bg_color_id)
        if color_pair_key in Colors.COLOR_TO_PAIR_ID:
            return Colors.COLOR_TO_PAIR_ID[color_pair_key]
        return Colors.COLOR_TO_PAIR_ID[Colors._create_color_pair_key(Colors.WHITE.FG, Colors.BLACK.BG)]