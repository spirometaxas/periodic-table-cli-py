import os
import sys
from .utils import Utils

class BoxCharacters:
    VERTICAL   = '│'
    HORIZONTAL = '─'
    CROSS      = '┼'

class ColumnItem:

    def __init__(self, key, title, title_parts):
        self.key = key
        self.title = title
        self.title_parts = title_parts

class DataProcessor:

    COLUMN_CONFIG = [
        ColumnItem('atomicNumber',          'Atomic Number',          [ '', 'Atomic', 'Number' ]           ),
        ColumnItem('symbol',                'Symbol',                 [ '', '', 'Symbol' ]                 ),
        ColumnItem('name',                  'Name',                   [ '', '', 'Name' ]                   ),
        ColumnItem('family',                'Family',                 [ '', '', 'Family' ]                 ),
        ColumnItem('standardState',         'State',                  [ '', '', 'State' ]                  ),
        ColumnItem('atomicMass',            'Atomic Mass',            [ '', 'Atomic Mass', '(u)' ]         ),
        ColumnItem('numberOfProtons',       'Protons',                [ '', 'Pro-', 'tons' ]               ),
        ColumnItem('numberOfNeutrons',      'Neutrons',               [ '', 'Neut-', 'rons' ]              ),
        ColumnItem('numberOfElectrons',     'Electrons',              [ '', 'Elect-', 'rons' ]             ),
        ColumnItem('numberOfValence',       'Valence Electrons',      [ 'Valence', 'Elect-', 'rons' ]      ),
        ColumnItem('valency',               'Valency',                [ '', '', 'Valency' ]                ),
        ColumnItem('atomicRadius',          'Atomic Radius',          [ 'Atomic', 'Radius', '(pm)' ]       ),
        ColumnItem('density',               'Density',                [ '', 'Density', '(g/cm^3)' ]        ),
        ColumnItem('electronegativity',     'Electronegativity',      [ '', 'Electro-', 'negativity' ]     ),
        ColumnItem('ionizationEnergy',      'Ioization Energy',       [ 'Ionization', 'Energy', '(eV)' ]   ),
        ColumnItem('electronAffinity',      'Electron Affinity',      [ 'Electron', 'Affinity', '(eV)' ]   ),
        ColumnItem('meltingPoint',          'Melting Point',          [ 'Melting', 'Point', '(K)' ]        ),
        ColumnItem('boilingPoint',          'Boiling Point',          [ 'Boiling', 'Point', '(K)' ]        ),
        ColumnItem('specificHeat',          'Specific Heat',          [ 'Specific', 'Heat', '(J/g K)' ]    ),
        ColumnItem('radioactive',           'Radioactive',            [ '', 'Radio-', 'active' ]           ),
        ColumnItem('occurrence',            'Occurrence',             [ '', '', 'Occurrence' ]             ),
        ColumnItem('yearDiscovered',        'Year',                   [ '', '', 'Year' ]                   ),
        ColumnItem('period',                'Period',                 [ '', '', 'Period' ]                 ),
        ColumnItem('group',                 'Group',                  [ '', '', 'Group' ]                  ),
        ColumnItem('shell',                 'Shell',                  [ '', '', 'Shell' ]                  ),
        ColumnItem('electronConfiguration', 'Electron Configuration', [ '', '', 'Electron Configuration' ] ),
        ColumnItem('oxidationStates',       'Oxidation States',       [ '', '', 'Oxidation States' ]       ),
    ]

    @staticmethod
    def _create_grid(x, y):
        grid = []
        for i in range(y):
            row = []
            for j in range(x):
                row.append(' ')
            grid.append(row)
        return grid

    @staticmethod
    def _get_title_length(title):
        size = 0
        for t in title:
            if size < len(t):
                size = len(t)
        return size

    @staticmethod
    def _get_column_data_length(grid, c):
        size = 0
        for i in range(len(grid)):
            if size < len(grid[i][c]):
                size = len(grid[i][c])
        return size

    @staticmethod
    def _get_string_with_padding(text, length, alignment='left'):
        if alignment == 'left':
            if len(text) < length:
                padding_length = length - len(text)
                return text + ' ' * padding_length
            else:
                return text
        elif alignment == 'center':
            if len(text) < length:
                padding_length = length - len(text)
                buffer = padding_length // 2
                return ' ' * buffer + text + ' ' * (padding_length - buffer)
            else:
                return text
        elif alignment == 'right':
            if len(text) < length:
                padding_length = length - len(text)
                return ' ' * padding_length + text
            else:
                return text

    @staticmethod
    def _render_grid(grid, full_column_config, verbose, width=None):
        sizes = []
        for i in range(len(full_column_config)):
            title_length = DataProcessor._get_title_length(full_column_config[i].title_parts)
            data_length = DataProcessor._get_column_data_length(grid, i)
            sizes.append(max(title_length, data_length))

        # Omit columns that do not fit on the screen
        column_config = full_column_config
        if width is not None and width > 0:
            current_column = 0
            current_width = 1 + sizes[0]
            while current_column + 1 < len(sizes) and current_width < width:
                if current_width + 3 < width:
                    current_width += 3
                else:
                    break
                if current_width + sizes[current_column + 1] < width:
                    current_width += sizes[current_column + 1]
                    current_column += 1
                else:
                    break

            column_config = full_column_config[:current_column + 1]

        response = '\n'

        # Titles
        for j in range(len(column_config[0].title_parts)):
            response += ' '  # Left buffer
            for i in range(len(column_config)):
                entry = DataProcessor._get_string_with_padding(column_config[i].title_parts[j], sizes[i], 'center')
                response += entry
                if i < len(column_config) - 1:
                    response += ' ' + BoxCharacters.VERTICAL + ' '  # Column buffer
            response += '\n'

        # Border
        for i in range(len(column_config)):
            response += BoxCharacters.HORIZONTAL * (sizes[i] + 2)
            if i < len(column_config) - 1:
                response += BoxCharacters.CROSS
        response += '\n'

        # Data
        for i in range(len(grid)):
            response += ' '
            for j in range(len(column_config)):
                response += str(DataProcessor._get_string_with_padding(grid[i][j], sizes[j]))
                if j < len(column_config) - 1:
                    response += ' ' + BoxCharacters.VERTICAL + ' '  # Column buffer
            response += '\n'

        if verbose:
            response += '\n ** Expected'
        else:
            response += '\n Run with --verbose (-v) for more data.'

        if len(column_config) < len(full_column_config):
            response += '\n\n ' + str(len(full_column_config) - len(column_config)) + ' columns omitted due to screen size constraints.  Specify an element to see the full data.'

        response += '\n'

        return response

    @staticmethod
    def _get_column_display_values(key, element, families, shells):
        if key == 'family':
            return families.get(element.get(key)).get('name')
        elif key == 'shell':
            return shells.get(element.get(key)).get('name')
        else:
            value = element.get(key)
            if value is None:
                return '-'
            elif key == 'atomicMass':
                return value.replace(' u', '')
            elif key == 'atomicRadius':
                return value.replace(' pm', '')
            elif key == 'density':
                return value.replace(' g/cm^3', '')
            elif key in ('ionizationEnergy', 'electronAffinity'):
                return value.replace(' eV', '')
            elif key in ('meltingPoint', 'boilingPoint'):
                return value.replace(' K', '')
            elif key == 'radioactive':
                return 'Yes' if value else 'No'
            return str(value)

    @staticmethod
    def _get_list_display_values(key, element, families, shells):
        if key == 'family':
            return families.get(element.get(key)).get('name')
        elif key == 'shell':
            return shells.get(element.get(key)).get('name')
        else:
            value = element.get(key)
            if value is None:
                return '-'
            elif key == 'radioactive':
                return 'Yes' if value else 'No'
            return str(value)

    @staticmethod
    def _format_all_elements(data, verbose, width):
        elements = sorted(data.get('elements'), key=lambda x: x.get('atomicNumber'))

        column_config = DataProcessor.COLUMN_CONFIG if verbose else DataProcessor.COLUMN_CONFIG[:3]
        grid = DataProcessor._create_grid(len(column_config), len(elements))

        for i, element in enumerate(elements):
            for j, config in enumerate(column_config):
                grid[i][j] = DataProcessor._get_column_display_values(config.key, element, data.get('families'), data.get('shells'))

        return DataProcessor._render_grid(grid, column_config, verbose, width)

    @staticmethod
    def _format_specific_element(element, data):
        response = '\n'
        for item in DataProcessor.COLUMN_CONFIG:
            response += ' ' + item.title + ': ' + DataProcessor._get_list_display_values(item.key, element, data['families'], data['shells']) + '\n'
        response += '\n'
        return response

    @staticmethod
    def format_data(config, data):
        element = None
        if config.atomic_number is not None or config.symbol is not None or config.name is not None:
            if config and Utils.is_valid_atomic_number(config.atomic_number):
                element = Utils.get_element_by_atomic_number(config.atomic_number, data.get('elements'))
            elif config and Utils.is_valid_element_symbol(config.symbol, data.get('elements')):
                element = Utils.get_element_by_symbol(config.symbol, data.get('elements'))
            elif config and Utils.is_valid_element_name(config.name, data.get('elements')):
                element = Utils.get_element_by_name(config.name, data.get('elements'))

            if element is not None:
                return DataProcessor._format_specific_element(element, data)
            else:
                return '\n Specified element not found.\n'

        # Element was not specified, so display the full chart
        width = None
        if sys.stdout.isatty():
            width = os.get_terminal_size().columns

        verbose = config.verbose or False
        return DataProcessor._format_all_elements(data, verbose, width)