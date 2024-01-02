import curses

class Color:

    def __init__(self, config):
        self.FG = config['ANSI']
        self.BG = config['ANSI']
        self.ANSI = config['ANSI']
        self.R = Color._base_255_to_1000(config['R'])
        self.G = Color._base_255_to_1000(config['G'])
        self.B = Color._base_255_to_1000(config['B'])

    @staticmethod
    def _base_255_to_1000(val):
        return int((val / 255.0) * 1000)

class Colors:
    BLACK       = Color({ 'ANSI':   0, 'R':   0, 'G':   0, 'B':   0 })  # Use default black
    WHITE       = Color({ 'ANSI': 255, 'R': 238, 'G': 238, 'B': 238 })
    GRAY        = Color({ 'ANSI': 244, 'R': 128, 'G': 128, 'B': 128 })
    LIGHT_GRAY  = Color({ 'ANSI': 250, 'R': 188, 'G': 188, 'B': 188 })
    FOCUS_GOLD  = Color({ 'ANSI': 214, 'R': 255, 'G': 175, 'B':   0 })
    FOCUS_BLUE  = Color({ 'ANSI':  33, 'R': 0,   'G': 135, 'B': 255 })

    RED         = Color({ 'ANSI': 196, 'R': 255, 'G':   0, 'B':   0 })
    DARK_RED    = Color({ 'ANSI':  88, 'R': 135, 'G':   0, 'B':   0 })
    ORANGE      = Color({ 'ANSI': 208, 'R': 255, 'G': 135, 'B':   0 })
    YELLOW      = Color({ 'ANSI': 226, 'R': 255, 'G': 255, 'B':   0 })
    DARK_YELLOW = Color({ 'ANSI': 136, 'R': 175, 'G': 135, 'B':   0 })
    GREEN       = Color({ 'ANSI':  40, 'R':   0, 'G': 215, 'B':   0 })
    MID_GREEN   = Color({ 'ANSI':  34, 'R':   0, 'G': 175, 'B':   0 })
    DARK_GREEN  = Color({ 'ANSI':  28, 'R':   0, 'G': 135, 'B':   0 })
    SKY_BLUE    = Color({ 'ANSI':  51, 'R':   0, 'G': 255, 'B': 255 })
    BLUE        = Color({ 'ANSI':  27, 'R':   0, 'G':  95, 'B': 255 })
    MAGENTA     = Color({ 'ANSI': 207, 'R': 255, 'G':  95, 'B': 255 })
    PURPLE      = Color({ 'ANSI':  93, 'R': 135, 'G':   0, 'B': 255 })

    COLORS = [ 
        BLACK, WHITE, GRAY, LIGHT_GRAY, FOCUS_GOLD, FOCUS_BLUE,
        RED, DARK_RED, ORANGE, YELLOW, DARK_YELLOW, GREEN,
        MID_GREEN, DARK_GREEN, SKY_BLUE, BLUE, MAGENTA, PURPLE,
    ]

    METER_COLORS = [
        Color({ 'ANSI': 51,  'R':   0, 'G': 255, 'B': 255 }),
        Color({ 'ANSI': 50,  'R':   0, 'G': 255, 'B': 215 }),
        Color({ 'ANSI': 49,  'R':   0, 'G': 255, 'B': 175 }),
        Color({ 'ANSI': 48,  'R':   0, 'G': 255, 'B': 135 }),
        Color({ 'ANSI': 47,  'R':   0, 'G': 255, 'B':  95 }),
        Color({ 'ANSI': 46,  'R':   0, 'G': 255, 'B':   0 }),
        Color({ 'ANSI': 82,  'R':  95, 'G': 255, 'B':   0 }),
        Color({ 'ANSI': 118, 'R': 135, 'G': 255, 'B':   0 }),
        Color({ 'ANSI': 154, 'R': 175, 'G': 255, 'B':   0 }),
        Color({ 'ANSI': 190, 'R': 215, 'G': 255, 'B':   0 }),
        Color({ 'ANSI': 226, 'R': 255, 'G': 255, 'B':   0 }),
        Color({ 'ANSI': 220, 'R': 255, 'G': 215, 'B':   0 }),
        Color({ 'ANSI': 214, 'R': 255, 'G': 175, 'B':   0 }),
        Color({ 'ANSI': 208, 'R': 255, 'G': 135, 'B':   0 }),
        Color({ 'ANSI': 202, 'R': 255, 'G':  95, 'B':   0 }),
        Color({ 'ANSI': 196, 'R': 255, 'G':   0, 'B':   0 }),
    ]

    COLOR_TO_PAIR_ID = {}

    @staticmethod
    def init_colors():
        curses.start_color()
        curses.use_default_colors()
        
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

            curses.init_pair(color_pair_id, Colors.WHITE.FG, bg_color.BG)
            Colors.COLOR_TO_PAIR_ID[Colors._create_color_pair_key(Colors.WHITE.FG, bg_color.BG)] = color_pair_id
            color_pair_id = color_pair_id + 1

        # Background meter colors
        for meter_color in Colors.METER_COLORS:
            curses.init_pair(color_pair_id, Colors.BLACK.FG, meter_color.BG)
            Colors.COLOR_TO_PAIR_ID[Colors._create_color_pair_key(Colors.BLACK.FG, meter_color.BG)] = color_pair_id
            color_pair_id = color_pair_id + 1

            curses.init_pair(color_pair_id, Colors.WHITE.FG, meter_color.BG)
            Colors.COLOR_TO_PAIR_ID[Colors._create_color_pair_key(Colors.WHITE.FG, meter_color.BG)] = color_pair_id
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