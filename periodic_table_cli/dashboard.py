import curses
from colors import Colors
from renderer import Renderer
from tables import DASHBOARD
from utils import Utils
from state_controller import Layout, DisplayModes, SelectModes
from search_processor import SearchResultType
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

class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

class PointLength(Point):

    def __init__(self, x, y, length):
        super(PointLength, self).__init__(x, y)
        self.length = length

class PointLengthColor(PointLength):

    def __init__(self, x, y, length, color):
        super(PointLengthColor, self).__init__(x, y, length)
        self.color = color

class ColorConfig:

    def __init__(self, color):
        self.color = color

class Dashboard:

    HORIZONTAL_RATIO = 0.5
    VERTICAL_RATIO = 0.333

    ELEMENTS_POS = Point(3, 2)
    ELEMENT_WIDTH = 6
    ELEMENT_HEIGHT = 3

    BG_COLOR = Colors.BLACK
    FG_COLOR = Colors.WHITE

    DISPLAY_CONFIG = PointLength(117, 36, 36)

    CONNECTORS_POS = [
        Point(16, 18), Point(17, 18), Point(18, 18), Point(19, 18), Point(20, 18),
        Point(18, 19), Point(18, 20), Point(16, 21), Point(17, 21), Point(18, 21),
        Point(19, 21), Point(20, 21), Point(18, 22), Point(18, 23), Point(18, 24),
        Point(17, 24), Point(16, 24), Point(15, 24), Point(14, 24), Point(13, 24),
        Point(13, 25), Point(13, 26), Point(13, 27), Point(13, 28), Point(13, 29),
        Point(14, 26), Point(14, 29),
    ]

    FAMILIES_CONFIG = {
        # Row 1
        'Alkali metal':          PointLengthColor(  7, 36, 19, Colors.RED         ),
        'Alkaline earth metal':  PointLengthColor( 27, 36, 27, Colors.ORANGE      ),
        'Transition metal':      PointLengthColor( 55, 36, 23, Colors.YELLOW      ),
        'Post-transition metal': PointLengthColor( 79, 36, 28, Colors.DARK_YELLOW ),

        # Row 2
        'Metalloid': PointLengthColor(  7, 37, 19, Colors.GREEN      ),
        'Nonmetal':  PointLengthColor( 27, 37, 27, Colors.DARK_GREEN ),
        'Halogen':   PointLengthColor( 55, 37, 23, Colors.SKY_BLUE   ),
        'Noble gas': PointLengthColor( 79, 37, 28, Colors.BLUE       ),
        
        # Row 3
        'Lanthanide': PointLengthColor(  7, 38, 19, Colors.MAGENTA ),
        'Actinide':   PointLengthColor( 27, 38, 27, Colors.PURPLE  ),
    }

    SHELLS_CONFIG = {
        's-shell': PointLengthColor( 16, 43, 13, Colors.RED    ),
        'p-shell': PointLengthColor( 39, 43, 13, Colors.YELLOW ),
        'd-shell': PointLengthColor( 62, 43, 13, Colors.GREEN  ),
        'f-shell': PointLengthColor( 85, 43, 13, Colors.BLUE   ),
    }

    STATES_CONFIG = {
        'Solid':     ColorConfig(Colors.WHITE),
        'Solid **':  ColorConfig(Colors.GRAY),
        'Liquid':    ColorConfig(Colors.RED),
        'Liquid **': ColorConfig(Colors.DARK_RED),
        'Gas':       ColorConfig(Colors.SKY_BLUE),
        'Gas **':    ColorConfig(Colors.BLUE),
    }

    VALENCE_ELECTRON_CONFIG = {
        'colors': {
            1: ColorConfig(Colors.PURPLE),
            2: ColorConfig(Colors.MAGENTA),
            3: ColorConfig(Colors.BLUE),
            4: ColorConfig(Colors.SKY_BLUE),
            5: ColorConfig(Colors.GREEN),
            6: ColorConfig(Colors.YELLOW),
            7: ColorConfig(Colors.ORANGE),
            8: ColorConfig(Colors.RED),
        },
        'min_value': 1,
        'max_value': 8,
    }

    VALENCY_CONFIG = {
        'colors': {
            0: ColorConfig(Colors.SKY_BLUE),
            1: ColorConfig(Colors.GREEN),
            2: ColorConfig(Colors.YELLOW),
            3: ColorConfig(Colors.ORANGE),
            4: ColorConfig(Colors.RED),
        },
        'min_value': 0,
        'max_value': 4,
    }

    RADIOACTIVE_CONFIG = {
        True:  ColorConfig(Colors.RED),
        False: ColorConfig(Colors.GREEN),
    }

    OCCURRENCE_CONFIG = {
        'Natural':   ColorConfig(Colors.SKY_BLUE),
        'Rare':      ColorConfig(Colors.YELLOW),
        'Synthetic': ColorConfig(Colors.ORANGE),
    }

    YEAR_CONFIG = {
        'min_value': 1669,
        'max_value': 2010,
        'colors': {
            'ANCIENT': Colors.WHITE,
        },
    }

    PERIOD_POS = {
        1: PointLength( 1,  3, 1 ),
        2: PointLength( 1,  6, 1 ),
        3: PointLength( 1,  9, 1 ),
        4: PointLength( 1, 12, 1 ),
        5: PointLength( 1, 15, 1 ),
        6: PointLength( 1, 18, 1 ),
        7: PointLength( 1, 21, 1 ),
    }

    GROUP_POS = {
        1:  PointLength(   6,  1, 1 ),
        2:  PointLength(  12,  4, 1 ),
        3:  PointLength(  18, 10, 1 ),
        4:  PointLength(  24, 10, 1 ),
        5:  PointLength(  30, 10, 1 ),
        6:  PointLength(  36, 10, 1 ),
        7:  PointLength(  42, 10, 1 ),
        8:  PointLength(  48, 10, 1 ),
        9:  PointLength(  54, 10, 1 ),
        10: PointLength(  59, 10, 2 ),
        11: PointLength(  65, 10, 2 ),
        12: PointLength(  71, 10, 2 ),
        13: PointLength(  77,  4, 2 ),
        14: PointLength(  83,  4, 2 ),
        15: PointLength(  89,  4, 2 ),
        16: PointLength(  95,  4, 2 ),
        17: PointLength( 101,  4, 2 ),
        18: PointLength( 107,  1, 2 ),
    }

    PANEL_CONFIG = {
        'TOP_POS':  Point(117, 3),
        'LIST_POS': Point(117, 5),
        'WIDTH': 36,
        'HEIGHT': 26,
    }

    TITLES = {
        'THE_PERIODIC_TABLE_OF_ELEMENTS': PointLength(  30,  2, 30 ),  # The Periodic Table of Elements
        'ELEMENT_FAMILIES':               PointLength(  49, 34, 16 ),  # Element Families
        'ELEMENT_CONFIGURATIONS':         PointLength(  46, 41, 23 ),  # Element Configurations
        'DISPLAY_MODES':                  PointLength( 129, 34, 12 ),  # Display Mode
        'CONTROLS':                       PointLength( 131, 39,  8 ),  # Controls
    }

    SEARCH_CONFIG = {
        'colors': {
            'RESULTS':         Colors.GREEN,
            'RESULTS_FOCUSED': Colors.MID_GREEN,
            'NO_RESULTS':      Colors.RED,
        },
    }


    def __init__(self, data):
        self.data = data
        self.board = self._parse_board()
        self._initDataOnBoard()
        self._save_board()

    def _initDataOnBoard(self):
        elements = Utils.get_elements(self.data.get('elements'))
        for r in range(len(Layout.PeriodicTable)):
            for c in range(len(Layout.PeriodicTable[r])):
                if Layout.PeriodicTable[r][c] is not None and Layout.PeriodicTable[r][c] > 0:
                    x_offset = self.ELEMENTS_POS.x
                    y_offset = self.ELEMENTS_POS.y
                    if Utils.is_bottom_section(Layout.PeriodicTable[r][c]):
                        y_offset += 2

                    # Atomic number
                    if Layout.PeriodicTable[r][c] < 10:
                        self._set_text(x_offset + (c * self.ELEMENT_WIDTH) + 3, y_offset + (r * self.ELEMENT_HEIGHT) + 1,
                                       str(elements[Layout.PeriodicTable[r][c]].get('atomicNumber')))
                    else:
                        self._set_text(x_offset + (c * self.ELEMENT_WIDTH) + 2, y_offset + (r * self.ELEMENT_HEIGHT) + 1,
                                       str(elements[Layout.PeriodicTable[r][c]].get('atomicNumber')))

                    # Symbol
                    self._set_text(x_offset + (c * self.ELEMENT_WIDTH) + 3, y_offset + (r * self.ELEMENT_HEIGHT) + 2,
                                   elements[Layout.PeriodicTable[r][c]].get('symbol'))

        for family, family_config in self.FAMILIES_CONFIG.items():
            self._set_text(family_config.x + 3, family_config.y, self.data.get('families').get(family).get('name'),
                           family_config.length - 3, 'left')

        for shell, shell_config in self.SHELLS_CONFIG.items():
            self._set_text(shell_config.x + 3, shell_config.y, self.data.get('shells').get(shell).get('name'),
                           shell_config.length - 3, 'left')

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

    def _make_bold(self, x, y, length):
        for c in range(length):
            self.board[y][x + c].config.bold = True

    def _set_text_color(self, x, y, length, color, bold):
        for c in range(length):
            self.board[y][x + c].config.foreground_color = color.FG
            self.board[y][x + c].config.bold = bold

    def _set_highlight_color(self, x, y, length, color):
        for c in range(length):
            self.board[y][x + c].config.background_color = color.BG
            self.board[y][x + c].config.foreground_color = Colors.BLACK.FG

    def _set_text(self, x, y, text, max_length=None, _type=None):
        offset = 0
        if max_length is not None and _type is not None:
            if _type == 'center':
                offset = max(int((max_length - len(text)) / 2), 0)
            elif _type == 'right':
                offset = max(max_length - len(text), 0)
        for i in range(len(text)):
            self.board[y][x + offset + i].character = str(text[i])

    def _decorate_titles(self):
        for title in self.TITLES:
            self._make_bold(self.TITLES[title].x, self.TITLES[title].y, self.TITLES[title].length)

    def _get_element_fill_color(self, element, display_mode):
        if display_mode == DisplayModes.STANDARD:
            return None
        elif display_mode == DisplayModes.FAMILIES:
            return self.FAMILIES_CONFIG[element.display.family].color
        elif display_mode == DisplayModes.SHELLS:
            return self.SHELLS_CONFIG[element.display.shell].color
        elif display_mode == DisplayModes.STATES:
            return self.STATES_CONFIG[element.display.state].color
        elif display_mode == DisplayModes.VALENCE_ELECTRONS:
            config = self.VALENCE_ELECTRON_CONFIG['colors'].get(element.display.valence_electrons)
            return config.color if config is not None else None
        elif display_mode == DisplayModes.VALENCY:
            config = self.VALENCY_CONFIG['colors'].get(element.display.valency)
            return config.color if config is not None else None
        elif display_mode == DisplayModes.RADIOACTIVE:
            config = self.RADIOACTIVE_CONFIG.get(element.display.radioactive)
            return config.color if config is not None else None
        elif display_mode == DisplayModes.OCCURRENCE:
            config = self.OCCURRENCE_CONFIG.get(element.display.occurrence)
            return config.color if config is not None else None
        elif element.display.meter is not None:
            color_index = Utils.get_bucket_value(element.display.meter, len(Colors.METER_COLORS))
            return Colors.METER_COLORS[color_index]
        elif element.display.is_ancient:
            return self.YEAR_CONFIG['colors']['ANCIENT']

    def _decorate_element(self, x, y, color, fill_color, focused, display_mode):
        # Lines
        self.board[y][x].config.foreground_color = color.FG
        self.board[y + 1][x].config.foreground_color = color.FG
        self.board[y + 2][x].config.foreground_color = color.FG
        self.board[y + 3][x].config.foreground_color = color.FG

        self.board[y][x + 1].config.foreground_color = color.FG
        self.board[y][x + 2].config.foreground_color = color.FG
        self.board[y][x + 3].config.foreground_color = color.FG
        self.board[y][x + 4].config.foreground_color = color.FG
        self.board[y][x + 5].config.foreground_color = color.FG
        self.board[y][x + 6].config.foreground_color = color.FG

        self.board[y + 1][x + 6].config.foreground_color = color.FG
        self.board[y + 2][x + 6].config.foreground_color = color.FG
        self.board[y + 3][x + 6].config.foreground_color = color.FG

        self.board[y + 3][x + 1].config.foreground_color = color.FG
        self.board[y + 3][x + 2].config.foreground_color = color.FG
        self.board[y + 3][x + 3].config.foreground_color = color.FG
        self.board[y + 3][x + 4].config.foreground_color = color.FG
        self.board[y + 3][x + 5].config.foreground_color = color.FG

        # Text
        if focused:
            # Atomic number
            self.board[y + 1][x + 2].config.foreground_color = color.FG
            self.board[y + 1][x + 3].config.foreground_color = color.FG
            self.board[y + 1][x + 4].config.foreground_color = color.FG

            self.board[y + 1][x + 2].config.bold = True
            self.board[y + 1][x + 3].config.bold = True
            self.board[y + 1][x + 4].config.bold = True

            # Element
            element_color = Colors.WHITE
            if display_mode != DisplayModes.STANDARD and fill_color is not None:
                element_color = Colors.BLACK
            self.board[y + 2][x + 2].config.foreground_color = element_color.FG
            self.board[y + 2][x + 3].config.foreground_color = element_color.FG
            self.board[y + 2][x + 4].config.foreground_color = element_color.FG

            self.board[y + 2][x + 2].config.bold = True
            self.board[y + 2][x + 3].config.bold = True
            self.board[y + 2][x + 4].config.bold = True
        else:
            if display_mode != DisplayModes.STANDARD and fill_color is not None:
                # Atomic number
                self.board[y + 1][x + 2].config.foreground_color = Colors.BLACK.FG
                self.board[y + 1][x + 3].config.foreground_color = Colors.BLACK.FG
                self.board[y + 1][x + 4].config.foreground_color = Colors.BLACK.FG

                # Element
                self.board[y + 2][x + 2].config.foreground_color = Colors.BLACK.FG
                self.board[y + 2][x + 3].config.foreground_color = Colors.BLACK.FG
                self.board[y + 2][x + 4].config.foreground_color = Colors.BLACK.FG
            else:
                # Atomic number
                self.board[y + 1][x + 2].config.foreground_color = Colors.GRAY.FG
                self.board[y + 1][x + 3].config.foreground_color = Colors.GRAY.FG
                self.board[y + 1][x + 4].config.foreground_color = Colors.GRAY.FG

                # Element
                self.board[y + 2][x + 2].config.foreground_color = Colors.WHITE.FG
                self.board[y + 2][x + 3].config.foreground_color = Colors.WHITE.FG
                self.board[y + 2][x + 4].config.foreground_color = Colors.WHITE.FG

        # Fill color
        top_color = self.BG_COLOR
        if fill_color is not None and not focused:
            top_color = fill_color

        self.board[y + 1][x + 1].config.background_color = top_color.BG
        self.board[y + 1][x + 2].config.background_color = top_color.BG
        self.board[y + 1][x + 3].config.background_color = top_color.BG
        self.board[y + 1][x + 4].config.background_color = top_color.BG
        self.board[y + 1][x + 5].config.background_color = top_color.BG

        if fill_color is not None:
            self.board[y + 2][x + 1].config.background_color = fill_color.BG
            self.board[y + 2][x + 2].config.background_color = fill_color.BG
            self.board[y + 2][x + 3].config.background_color = fill_color.BG
            self.board[y + 2][x + 4].config.background_color = fill_color.BG
            self.board[y + 2][x + 5].config.background_color = fill_color.BG

    def _apply_config_to_elements(self, config):
        # Lines
        for point in self.CONNECTORS_POS:
            self.board[point.y][point.x].config.foreground_color = Colors.GRAY.FG

        # Draw unselected
        for r in range(len(Layout.PeriodicTable)):
            for c in range(len(Layout.PeriodicTable[r])):
                if Layout.PeriodicTable[r][c] is not None and Layout.PeriodicTable[r][c] > 0:
                    element_config = config.elements[Layout.PeriodicTable[r][c]]
                    x_offset = self.ELEMENTS_POS.x
                    y_offset = self.ELEMENTS_POS.y
                    if Utils.is_bottom_section(element_config.atomic_number):
                        y_offset += 2

                    fill_color = self._get_element_fill_color(element_config, config.display_mode)
                    focus_color = Colors.WHITE

                    if (
                        config.shells.selected is None
                        and config.families.selected is None
                        and config.display_mode == DisplayModes.STANDARD
                    ):
                        focus_color = Colors.FOCUS_BLUE

                    self._decorate_element(
                        x_offset + (c * self.ELEMENT_WIDTH),
                        y_offset + (r * self.ELEMENT_HEIGHT),
                        focus_color,
                        fill_color,
                        False,
                        config.display_mode,
                    )

        for family in self.FAMILIES_CONFIG:
            family_config = self.FAMILIES_CONFIG[family]
            self._set_text_color(family_config.x, family_config.y, family_config.length, Colors.GRAY, False)

        for shell in self.SHELLS_CONFIG:
            shell_config = self.SHELLS_CONFIG[shell]
            self._set_text_color(shell_config.x, shell_config.y, shell_config.length, Colors.GRAY, False)

        # Draw selected
        for r in range(len(Layout.PeriodicTable)):
            for c in range(len(Layout.PeriodicTable[r])):
                if Layout.PeriodicTable[r][c] > 0 and config.elements[Layout.PeriodicTable[r][c]] is not None and config.elements[Layout.PeriodicTable[r][c]].selected is not None:
                    element_config = config.elements[Layout.PeriodicTable[r][c]]
                    x_offset = self.ELEMENTS_POS.x
                    y_offset = self.ELEMENTS_POS.y
                    if Utils.is_bottom_section(element_config.atomic_number):
                        y_offset += 2
                    fill_color = self._get_element_fill_color(element_config, config.display_mode)
                    if element_config.selected.type == SelectModes.ELEMENT:
                        self._decorate_element(
                            x_offset + (c * self.ELEMENT_WIDTH),
                            y_offset + (r * self.ELEMENT_HEIGHT),
                            Colors.FOCUS_GOLD,
                            fill_color,
                            True,
                            config.display_mode,
                        )
                    elif element_config.selected.type == SelectModes.FAMILY:
                        family_config = self.FAMILIES_CONFIG[config.families.selected]
                        self._decorate_element(
                            x_offset + (c * self.ELEMENT_WIDTH),
                            y_offset + (r * self.ELEMENT_HEIGHT),
                            family_config.color,
                            fill_color,
                            True,
                            config.display_mode,
                        )
                    elif element_config.selected.type == SelectModes.SHELL:
                        shell_config = self.SHELLS_CONFIG[config.shells.selected]
                        self._decorate_element(
                            x_offset + (c * self.ELEMENT_WIDTH),
                            y_offset + (r * self.ELEMENT_HEIGHT),
                            shell_config.color,
                            fill_color,
                            True,
                            config.display_mode,
                        )

        if config and config.families:
            if config.families.indicated and self.FAMILIES_CONFIG[config.families.indicated]:
                family_config = self.FAMILIES_CONFIG[config.families.indicated]
                self._set_text_color(family_config.x, family_config.y, family_config.length, Colors.FOCUS_GOLD, True)
            elif config.families.selected and self.FAMILIES_CONFIG[config.families.selected]:
                family_config = self.FAMILIES_CONFIG[config.families.selected]
                self._set_highlight_color(family_config.x, family_config.y, family_config.length, family_config.color)

        if config.display_mode == DisplayModes.FAMILIES:
            for family_name in self.FAMILIES_CONFIG:
                family_config = self.FAMILIES_CONFIG[family_name]
                self._set_highlight_color(family_config.x, family_config.y, 2, family_config.color)

        if config and config.shells:
            if config.shells.indicated and self.SHELLS_CONFIG[config.shells.indicated]:
                shell_config = self.SHELLS_CONFIG[config.shells.indicated]
                self._set_text_color(shell_config.x, shell_config.y, shell_config.length, Colors.FOCUS_GOLD, True)
            elif config.shells.selected and self.SHELLS_CONFIG[config.shells.selected]:
                shell_config = self.SHELLS_CONFIG[config.shells.selected]
                self._set_highlight_color(shell_config.x, shell_config.y, shell_config.length, shell_config.color)

        if config.display_mode == DisplayModes.SHELLS:
            for shell_name in self.SHELLS_CONFIG:
                shells_config = self.SHELLS_CONFIG[shell_name]
                self._set_highlight_color(shells_config.x, shells_config.y, 2, shells_config.color)

        if config and config.period and self.PERIOD_POS[config.period]:
            period_config = self.PERIOD_POS[config.period]
            self._set_text_color(period_config.x, period_config.y, period_config.length, Colors.FOCUS_GOLD, False)

        if config and config.group and self.GROUP_POS[config.group]:
            group_config = self.GROUP_POS[config.group]
            self._set_text_color(group_config.x, group_config.y, group_config.length, Colors.FOCUS_GOLD, False)

    def _set_display_mode(self, config):
        if config.display_mode == DisplayModes.STANDARD:
            self._set_text(self.DISPLAY_CONFIG.x, self.DISPLAY_CONFIG.y, 'STANDARD', self.DISPLAY_CONFIG.length, 'center')
        elif config.display_mode == DisplayModes.FAMILIES:
            self._set_text(self.DISPLAY_CONFIG.x, self.DISPLAY_CONFIG.y, 'ELEMENT FAMILIES', self.DISPLAY_CONFIG.length, 'center')
            self._set_highlight_color(
                self.TITLES['ELEMENT_FAMILIES'].x - 2,
                self.TITLES['ELEMENT_FAMILIES'].y,
                self.TITLES['ELEMENT_FAMILIES'].length + 4,
                Colors.WHITE,
            )
        elif config.display_mode == DisplayModes.SHELLS:
            self._set_text(self.DISPLAY_CONFIG.x, self.DISPLAY_CONFIG.y, 'ELECTRON CONFIGURATIONS', self.DISPLAY_CONFIG.length, 'center')
            self._set_highlight_color(
                self.TITLES['ELEMENT_CONFIGURATIONS'].x - 2,
                self.TITLES['ELEMENT_CONFIGURATIONS'].y,
                self.TITLES['ELEMENT_CONFIGURATIONS'].length + 4,
                Colors.WHITE,
            )
        elif config.display_mode == DisplayModes.STATES:
            section_length = int(self.DISPLAY_CONFIG.length / 3)
            self._set_highlight_color(self.DISPLAY_CONFIG.x, self.DISPLAY_CONFIG.y, section_length - 1, self.STATES_CONFIG['Solid'].color)
            self._set_text(self.DISPLAY_CONFIG.x, self.DISPLAY_CONFIG.y, 'SOLID', section_length - 1, 'center')

            self._set_highlight_color(self.DISPLAY_CONFIG.x + section_length, self.DISPLAY_CONFIG.y, section_length, self.STATES_CONFIG['Liquid'].color)
            self._set_text(self.DISPLAY_CONFIG.x + section_length, self.DISPLAY_CONFIG.y, 'LIQUID', section_length, 'center')

            self._set_highlight_color(self.DISPLAY_CONFIG.x + (2 * section_length) + 1, self.DISPLAY_CONFIG.y, section_length - 1, self.STATES_CONFIG['Gas'].color)
            self._set_text(self.DISPLAY_CONFIG.x + (2 * section_length) + 1, self.DISPLAY_CONFIG.y, 'GAS', section_length - 1, 'center')
        elif config.display_mode == DisplayModes.VALENCE_ELECTRONS:
            section_length = int(self.DISPLAY_CONFIG.length / 2)
            part_length = 2
            self._set_text(self.DISPLAY_CONFIG.x, self.DISPLAY_CONFIG.y, 'VALENCE ELECTRONS', section_length, 'center')
            count = 0
            for i in range(self.VALENCE_ELECTRON_CONFIG['min_value'], self.VALENCE_ELECTRON_CONFIG['max_value'] + 1):
                self._set_highlight_color(
                    self.DISPLAY_CONFIG.x + section_length + (count * part_length) + 2,
                    self.DISPLAY_CONFIG.y,
                    part_length,
                    self.VALENCE_ELECTRON_CONFIG['colors'][i].color,
                )
                self._set_text(
                    self.DISPLAY_CONFIG.x + section_length + (count * part_length) + 2,
                    self.DISPLAY_CONFIG.y,
                    ' ' + str(i),
                    part_length,
                    'left',
                )
                count += 1
        elif config.display_mode == DisplayModes.VALENCY:
            section_length = int(self.DISPLAY_CONFIG.length / 2)
            part_length = 3
            self._set_text(self.DISPLAY_CONFIG.x, self.DISPLAY_CONFIG.y, 'VALENCY', section_length, 'center')
            count = 0
            for i in range(self.VALENCY_CONFIG['min_value'], self.VALENCY_CONFIG['max_value'] + 1):
                self._set_highlight_color(
                    self.DISPLAY_CONFIG.x + section_length + (count * part_length) + 3,
                    self.DISPLAY_CONFIG.y,
                    part_length,
                    self.VALENCY_CONFIG['colors'][i].color,
                )
                self._set_text(
                    self.DISPLAY_CONFIG.x + section_length + (count * part_length) + 3,
                    self.DISPLAY_CONFIG.y,
                    str(i),
                    part_length,
                    'center',
                )
                count += 1
        elif config.display_mode == DisplayModes.RADIOACTIVE:
            section_length = int(self.DISPLAY_CONFIG.length / 2)
            self._set_highlight_color(self.DISPLAY_CONFIG.x, self.DISPLAY_CONFIG.y, section_length - 1, self.RADIOACTIVE_CONFIG[True].color)
            self._set_text(self.DISPLAY_CONFIG.x, self.DISPLAY_CONFIG.y, 'RADIOACTIVE', section_length - 1, 'center')

            self._set_highlight_color(self.DISPLAY_CONFIG.x + section_length, self.DISPLAY_CONFIG.y, section_length, self.RADIOACTIVE_CONFIG[False].color)
            self._set_text(self.DISPLAY_CONFIG.x + section_length, self.DISPLAY_CONFIG.y, 'STABLE', section_length, 'center')
        elif config.display_mode == DisplayModes.OCCURRENCE:
            section_length = int(self.DISPLAY_CONFIG.length / 3)
            self._set_highlight_color(self.DISPLAY_CONFIG.x, self.DISPLAY_CONFIG.y, section_length - 1, self.OCCURRENCE_CONFIG['Natural'].color)
            self._set_text(self.DISPLAY_CONFIG.x, self.DISPLAY_CONFIG.y, 'NATURAL', section_length - 1, 'center')

            self._set_highlight_color(self.DISPLAY_CONFIG.x + section_length, self.DISPLAY_CONFIG.y, section_length, self.OCCURRENCE_CONFIG['Rare'].color)
            self._set_text(self.DISPLAY_CONFIG.x + section_length, self.DISPLAY_CONFIG.y, 'RARE', section_length, 'center')

            self._set_highlight_color(
                self.DISPLAY_CONFIG.x + (2 * section_length) + 1,
                self.DISPLAY_CONFIG.y,
                section_length - 1,
                self.OCCURRENCE_CONFIG['Synthetic'].color,
            )
            self._set_text(
                self.DISPLAY_CONFIG.x + (2 * section_length) + 1,
                self.DISPLAY_CONFIG.y,
                'SYNTHETIC',
                section_length - 1,
                'center',
            )
        elif config.display_mode == DisplayModes.YEAR:
            section_length = int(self.DISPLAY_CONFIG.length / 2)
            self._set_text(self.DISPLAY_CONFIG.x, self.DISPLAY_CONFIG.y, 'YEAR', section_length - 9, 'center')

            self._set_highlight_color(self.DISPLAY_CONFIG.x + section_length - 8, self.DISPLAY_CONFIG.y, 9, self.YEAR_CONFIG['colors']['ANCIENT'])
            self._set_text(self.DISPLAY_CONFIG.x + section_length - 8, self.DISPLAY_CONFIG.y, 'ANCIENT', 9, 'center')

            for i in range(len(Colors.METER_COLORS)):
                self._set_highlight_color(self.DISPLAY_CONFIG.x + section_length + i + 2, self.DISPLAY_CONFIG.y, 1, Colors.METER_COLORS[i])

            self._set_text_color(self.DISPLAY_CONFIG.x + section_length + 3, self.DISPLAY_CONFIG.y, 4, Colors.BLACK, False)
            self._set_text(self.DISPLAY_CONFIG.x + section_length + 3, self.DISPLAY_CONFIG.y, str(self.YEAR_CONFIG['min_value']), 4, 'left')

            self._set_text_color(self.DISPLAY_CONFIG.x + (2 * section_length) - 5, self.DISPLAY_CONFIG.y, 4, Colors.BLACK, False)
            self._set_text(self.DISPLAY_CONFIG.x + (2 * section_length) - 5, self.DISPLAY_CONFIG.y, str(self.YEAR_CONFIG['max_value']), 4, 'left')
        elif config.display_mode and config.display_mode.is_meter:
            section_length = int(self.DISPLAY_CONFIG.length / 2)
            self._set_text(
                self.DISPLAY_CONFIG.x,
                self.DISPLAY_CONFIG.y,
                self._get_field_name(config.display_mode.key).upper(),
                section_length,
                'center',
            )
            for i in range(len(Colors.METER_COLORS)):
                self._set_highlight_color(self.DISPLAY_CONFIG.x + section_length + i + 2, self.DISPLAY_CONFIG.y, 1, Colors.METER_COLORS[i])

            self._set_text_color(self.DISPLAY_CONFIG.x + section_length + 3, self.DISPLAY_CONFIG.y, 3, Colors.BLACK, False)
            self._set_text(self.DISPLAY_CONFIG.x + section_length + 3, self.DISPLAY_CONFIG.y, 'MIN', 3, 'left')

            self._set_text_color(self.DISPLAY_CONFIG.x + (2 * section_length) - 4, self.DISPLAY_CONFIG.y, 3, Colors.BLACK, False)
            self._set_text(self.DISPLAY_CONFIG.x + (2 * section_length) - 4, self.DISPLAY_CONFIG.y, 'MAX', 3, 'left')

    def _get_field_name(self, key):
        for data in Layout.PanelData:
            if data.key == key:
                return data.name
        return None

    def _get_field_index(self, key):
        for i, data in enumerate(Layout.PanelData):
            if data.key == key:
                return i
        return None

    def _get_lines_from_description(self, text):
        parts = text.split(' ')
        lines = []
        line = ''
        for part in parts:
            if len(line) + len(part) <= self.PANEL_CONFIG['WIDTH']:
                line += part
            else:
                lines.append(line)
                line = part
            if len(line) < self.PANEL_CONFIG['WIDTH']:
                line += ' '
        lines.append(line)
        return lines

    def _populate_panel(self, config):
        if config.mode == SelectModes.SEARCH:
            self._populate_search_panel(config)
        else:
            self._populate_data_panel(config)

    def _populate_data_panel(self, config):
        # Top
        if config.panel and config.panel.top:
            if config.panel.top.element:
                self._set_text_color(self.PANEL_CONFIG['TOP_POS'].x, self.PANEL_CONFIG['TOP_POS'].y, self.PANEL_CONFIG['WIDTH'], Colors.FOCUS_GOLD, True)
                self._set_text(self.PANEL_CONFIG['TOP_POS'].x, self.PANEL_CONFIG['TOP_POS'].y, config.panel.top.element, self.PANEL_CONFIG['WIDTH'], 'center')
            elif config.panel.top.family:
                color = self.FAMILIES_CONFIG[config.panel.top.id].color
                self._set_text_color(self.PANEL_CONFIG['TOP_POS'].x, self.PANEL_CONFIG['TOP_POS'].y, self.PANEL_CONFIG['WIDTH'], color, True)
                self._set_text(self.PANEL_CONFIG['TOP_POS'].x, self.PANEL_CONFIG['TOP_POS'].y, config.panel.top.family, self.PANEL_CONFIG['WIDTH'], 'center')
            elif config.panel.top.shell:
                color = self.SHELLS_CONFIG[config.panel.top.id].color
                self._set_text_color(self.PANEL_CONFIG['TOP_POS'].x, self.PANEL_CONFIG['TOP_POS'].y, self.PANEL_CONFIG['WIDTH'], color, True)
                self._set_text(self.PANEL_CONFIG['TOP_POS'].x, self.PANEL_CONFIG['TOP_POS'].y, config.panel.top.shell, self.PANEL_CONFIG['WIDTH'], 'center')

        # List
        if config.panel.bottom and config.panel.bottom.list:
            current_y = self.PANEL_CONFIG['LIST_POS'].y
            has_expected = False
            for pair in config.panel.bottom.list:
                self._set_text_color(self.PANEL_CONFIG['LIST_POS'].x, current_y, int(self.PANEL_CONFIG['WIDTH'] / 2), Colors.GRAY, False)
                self._set_text(self.PANEL_CONFIG['TOP_POS'].x, current_y, pair.key + ':', int(self.PANEL_CONFIG['WIDTH'] / 2), 'right')

                value = self._get_panel_value(pair.value)
                if len(value) + 1 > self.PANEL_CONFIG['WIDTH'] / 2:
                    current_y += 1
                    self._set_text_color(self.PANEL_CONFIG['LIST_POS'].x, current_y, self.PANEL_CONFIG['WIDTH'], Colors.WHITE, False)
                    self._set_text(self.PANEL_CONFIG['TOP_POS'].x, current_y, ' ' + value, self.PANEL_CONFIG['WIDTH'], 'right')
                else:
                    color = Colors.WHITE
                    if pair.value is None:
                        color = Colors.GRAY

                    self._set_text_color(self.PANEL_CONFIG['LIST_POS'].x + int(self.PANEL_CONFIG['WIDTH'] / 2), current_y, int(self.PANEL_CONFIG['WIDTH'] / 2), color, False)
                    self._set_text(self.PANEL_CONFIG['TOP_POS'].x + int(self.PANEL_CONFIG['WIDTH'] / 2), current_y, ' ' + self._get_panel_value(pair.value), self.PANEL_CONFIG['WIDTH'] / 2, 'left')

                    if value is not None and value.endswith(' **'):
                        has_expected = True

                current_y += 1

            if config.display_mode and config.display_mode.key:
                field_index = self._get_field_index(config.display_mode.key)
                self._set_highlight_color(self.PANEL_CONFIG['LIST_POS'].x - 1, self.PANEL_CONFIG['LIST_POS'].y + field_index, self.PANEL_CONFIG['WIDTH'] + 2, Colors.WHITE)

            if has_expected:
                self._set_text_color(self.PANEL_CONFIG['LIST_POS'].x, self.PANEL_CONFIG['LIST_POS'].y + self.PANEL_CONFIG['HEIGHT'] - 1, self.PANEL_CONFIG['WIDTH'], Colors.GRAY, False)
                self._set_text(self.PANEL_CONFIG['TOP_POS'].x, self.PANEL_CONFIG['LIST_POS'].y + self.PANEL_CONFIG['HEIGHT'] - 1, '** Expected', self.PANEL_CONFIG['WIDTH'], 'right')
        elif config.panel.bottom and config.panel.bottom.description:
            lines = self._get_lines_from_description(config.panel.bottom.description)
            current_y = self.PANEL_CONFIG['LIST_POS'].y
            for line in lines:
                self._set_text_color(self.PANEL_CONFIG['LIST_POS'].x, current_y, self.PANEL_CONFIG['WIDTH'], Colors.LIGHT_GRAY, False)
                self._set_text(self.PANEL_CONFIG['TOP_POS'].x, current_y, line, self.PANEL_CONFIG['WIDTH'], 'left')
                current_y += 1

    def _populate_search_panel(self, config):
        has_results = config.panel.bottom and config.panel.bottom.results and len(config.panel.bottom.results) > 0

        # Top
        if config.panel and config.panel.top:
            if config.panel.top.query:
                color = self.SEARCH_CONFIG['colors']['RESULTS'] if has_results else self.SEARCH_CONFIG['colors']['NO_RESULTS']
                self._set_text_color(self.PANEL_CONFIG['TOP_POS'].x, self.PANEL_CONFIG['TOP_POS'].y, self.PANEL_CONFIG['WIDTH'], color, True)
                self._set_text(self.PANEL_CONFIG['TOP_POS'].x, self.PANEL_CONFIG['TOP_POS'].y, config.panel.top.query, self.PANEL_CONFIG['WIDTH'], 'center')

        # Bottom
        if has_results:
            highlight_length = len(config.panel.top.query) if config.panel.top.query else 0
            name_offset = 5

            if config.panel.bottom.index is not None:
                self._set_highlight_color(self.PANEL_CONFIG['LIST_POS'].x - 1, self.PANEL_CONFIG['LIST_POS'].y + config.panel.bottom.index, self.PANEL_CONFIG['WIDTH'] + 2, Colors.WHITE)

            for i, item in enumerate(config.panel.bottom.results):
                is_selected = config.panel.bottom.index == i
                selected_color = self.SEARCH_CONFIG['colors']['RESULTS_FOCUSED'] if is_selected else self.SEARCH_CONFIG['colors']['RESULTS']

                if item.type == SearchResultType.ELEMENT:
                    if item.atomic_number is not None:
                        self._set_text(self.PANEL_CONFIG['LIST_POS'].x, self.PANEL_CONFIG['LIST_POS'].y + i, item.atomic_number.text, 3, 'left')
                        if item.atomic_number.index is not None:
                            self._set_text_color(self.PANEL_CONFIG['LIST_POS'].x + item.atomic_number.index, self.PANEL_CONFIG['LIST_POS'].y + i, highlight_length, selected_color, False)
                    elif item.atomic_symbol is not None:
                        self._set_text(self.PANEL_CONFIG['LIST_POS'].x, self.PANEL_CONFIG['LIST_POS'].y + i, item.atomic_symbol.text, 2, 'left')
                        if item.atomic_symbol.index is not None:
                            self._set_text_color(self.PANEL_CONFIG['LIST_POS'].x + item.atomic_symbol.index, self.PANEL_CONFIG['LIST_POS'].y + i, highlight_length, selected_color, False)
                    if item.name:
                        self._set_text(self.PANEL_CONFIG['LIST_POS'].x + name_offset, self.PANEL_CONFIG['LIST_POS'].y + i, item.name.text, self.PANEL_CONFIG['WIDTH'] - name_offset, 'left')
                        if item.name.index is not None:
                            self._set_text_color(self.PANEL_CONFIG['LIST_POS'].x + item.name.index + name_offset, self.PANEL_CONFIG['LIST_POS'].y + i, highlight_length, selected_color, False)
                else:
                    if item.name:
                        self._set_text(self.PANEL_CONFIG['LIST_POS'].x, self.PANEL_CONFIG['LIST_POS'].y + i, item.name.text, self.PANEL_CONFIG['WIDTH'], 'left')
                        if item.name.index is not None:
                            self._set_text_color(self.PANEL_CONFIG['LIST_POS'].x + item.name.index, self.PANEL_CONFIG['LIST_POS'].y + i, highlight_length, selected_color, False)

            self._set_text_color(self.PANEL_CONFIG['LIST_POS'].x, self.PANEL_CONFIG['LIST_POS'].y + self.PANEL_CONFIG['HEIGHT'] - 2, self.PANEL_CONFIG['WIDTH'], Colors.GRAY, False)
            self._set_text(self.PANEL_CONFIG['TOP_POS'].x, self.PANEL_CONFIG['LIST_POS'].y + self.PANEL_CONFIG['HEIGHT'] - 2, 'Navigation:<UP|DOWN>  Select:<ENTER>', self.PANEL_CONFIG['WIDTH'], 'center')
        else:
            self._set_text_color(self.PANEL_CONFIG['LIST_POS'].x, self.PANEL_CONFIG['LIST_POS'].y, self.PANEL_CONFIG['WIDTH'], Colors.GRAY, False)
            self._set_text(self.PANEL_CONFIG['TOP_POS'].x, self.PANEL_CONFIG['LIST_POS'].y, 'NO RESULTS', self.PANEL_CONFIG['WIDTH'], 'center')

        self._set_text_color(self.PANEL_CONFIG['LIST_POS'].x, self.PANEL_CONFIG['LIST_POS'].y + self.PANEL_CONFIG['HEIGHT'] - 1, self.PANEL_CONFIG['WIDTH'], Colors.GRAY, False)
        self._set_text(self.PANEL_CONFIG['TOP_POS'].x, self.PANEL_CONFIG['LIST_POS'].y + self.PANEL_CONFIG['HEIGHT'] - 1, 'Exit Search:<LEFT>', self.PANEL_CONFIG['WIDTH'], 'center')

    def _get_panel_value(self, value):
        if value is not None:
            if value is True:
                return 'Yes'
            elif value is False:
                return 'No'
            return str(value)
        else:
            return '-'

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
        Renderer.generate_optimized(full_board, self.window)

    def render(self, render_config):
        self._reset_board()
        self._set_background()
        self._decorate_titles()
        self._set_display_mode(render_config)
        self._apply_config_to_elements(render_config)
        self._populate_panel(render_config)
        self._draw()