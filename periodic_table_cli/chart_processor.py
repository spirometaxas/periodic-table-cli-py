import os
import sys
from .utils import Utils
from .state_controller import Layout
from .tables import PERIODIC_TABLE_SMALL, PERIODIC_TABLE

class Dimensions:

    def __init__(self, start, vertical_offset, horizontal_offset, width):
        self.start = start
        self.vertical_offset = vertical_offset
        self.horizontal_offset = horizontal_offset
        self.width = width

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class ChartProcessor:

    class DIMENSIONS:

        SMALL    = Dimensions(Point(4, 3), 3, 4, 3)
        STANDARD = Dimensions(Point(4, 3), 3, 6, 5)


    HIGHLIGHT = '\u001b[7m'
    OFF = '\u001b[0m'

    @staticmethod
    def _format_specific_element(element, small):
        chart = PERIODIC_TABLE_SMALL if small else PERIODIC_TABLE
        dim = ChartProcessor.DIMENSIONS.SMALL if small else ChartProcessor.DIMENSIONS.STANDARD
        lines = chart.split('\n')
        pos = ChartProcessor._find_element(element.get('atomicNumber'))

        y = dim.start.y + (pos['row'] * dim.vertical_offset)
        x = dim.start.x + (pos['column'] * dim.horizontal_offset)

        if Utils.is_bottom_section(element.get('atomicNumber')):
            y += 2

        lines[y] = lines[y][:x] + ChartProcessor.HIGHLIGHT + lines[y][x:x + dim.width] + ChartProcessor.OFF + lines[y][x + dim.width:]
        lines[y + 1] = lines[y + 1][:x] + ChartProcessor.HIGHLIGHT + lines[y + 1][x:x + dim.width] + ChartProcessor.OFF + lines[y + 1][x + dim.width:]
        
        return '\n'.join(lines)

    @staticmethod
    def _find_element(atomic_number):
        for row, row_data in enumerate(Layout.PeriodicTable):
            for column, element_number in enumerate(row_data):
                if element_number == atomic_number:
                    return { 'row': row, 'column': column }
        return None

    @staticmethod
    def format_chart(config, data):
        small = config.small or False
        element = None

        if config.atomic_number is not None or config.symbol is not None or config.name is not None:
            if config.atomic_number is not None and Utils.is_valid_atomic_number(config.atomic_number):
                element = Utils.get_element_by_atomic_number(config.atomic_number, data.get('elements'))
            elif config.symbol is not None and Utils.is_valid_element_symbol(config.symbol, data.get('elements')):
                element = Utils.get_element_by_symbol(config.symbol, data.get('elements'))
            elif config.name is not None and Utils.is_valid_element_name(config.name, data.get('elements')):
                element = Utils.get_element_by_name(config.name, data.get('elements'))

            if element is not None:
                return ChartProcessor._format_specific_element(element, small)
            else:
                return '\n Specified element not found.\n'

        # If no element was specified, display the regular chart
        return PERIODIC_TABLE_SMALL if small else PERIODIC_TABLE