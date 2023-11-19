from utils import Utils
from search_processor import SearchProcessor, SearchResultType

class SelectModes:
    ELEMENT = 'element'
    FAMILY  = 'family'
    SHELL   = 'shell'
    SEARCH  = 'search'

class DisplayMode:

    def __init__(self, name, key=None, is_meter=False):
        self.name = name
        self.key = key
        self.is_meter = is_meter

class DisplayModes:
    STANDARD          = DisplayMode('standard'                                     )
    FAMILIES          = DisplayMode('families'                                     )
    SHELLS            = DisplayMode('shells'                                       )
    STATES            = DisplayMode('states',            'standardState'           )
    ATOMIC_MASS       = DisplayMode('atomicMass',        'atomicMass',        True )
    PROTONS           = DisplayMode('protons',           'numberOfProtons',   True )
    NEUTRONS          = DisplayMode('neutrons',          'numberOfNeutrons',  True )
    ELECTRONS         = DisplayMode('electrons',         'numberOfElectrons', True )
    VALENCE_ELECTRONS = DisplayMode('numberOfValence',   'numberOfValence'         )
    VALENCY           = DisplayMode('valency',           'valency'                 )
    ATOMIC_RADIUS     = DisplayMode('atomicRadius',      'atomicRadius',      True )
    DENSITY           = DisplayMode('density',           'density',           True )
    ELECTRONEGATIVITY = DisplayMode('electronegativity', 'electronegativity', True )
    IONIZATION_ENERGY = DisplayMode('ionizationEnergy',  'ionizationEnergy',  True )
    ELECTRON_AFFINITY = DisplayMode('electronAffinity',  'electronAffinity',  True )
    MELTING_POINT     = DisplayMode('meltingPoint',      'meltingPoint',      True )
    BOILING_POINT     = DisplayMode('boilingPoint',      'boilingPoint',      True )
    SPECIFIC_HEAT     = DisplayMode('specificHeat',      'specificHeat',      True )
    RADIOACTIVE       = DisplayMode('radioactive',       'radioactive'             )
    OCCURRENCE        = DisplayMode('occurrence',        'occurrence'              )
    YEAR              = DisplayMode('yearDiscovered',    'yearDiscovered',    True )

class ElementItem:

    def __init__(self, key, index):
        self.key = key
        self.index = index

class PanelItem:

    def __init__(self, key, name):
        self.key = key
        self.name = name

class Layout:

    PeriodicTable = [
        [   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   2 ],
        [   3,   4,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   5,   6,   7,   8,   9,  10 ],
        [  11,  12,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  13,  14,  15,  16,  17,  18 ],
        [  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29,  30,  31,  32,  33,  34,  35,  36 ],
        [  37,  38,  39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54 ],
        [  55,  56,   0,  72,  73,  74,  75,  76,  77,  78,  79,  80,  81,  82,  83,  84,  85,  86 ],
        [  87,  88,   0, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118 ],
        [   0,   0,  57,  58,  59,  60,  61,  62,  63,  64,  65,  66,  67,  68,  69,  70,  71,   0 ],
        [   0,   0,  89,  90,  91,  92,  93,  94,  95,  96,  97,  98,  99, 100, 101, 102, 103,   0 ],
    ]

    FamiliesTable = [ 
        ElementItem('Alkali metal', 0), ElementItem('Alkaline earth metal', 1), ElementItem('Transition metal', 2), ElementItem('Post-transition metal', 3),
        ElementItem('Metalloid',    4), ElementItem('Nonmetal',             5), ElementItem('Halogen',          6), ElementItem('Noble gas',             7),
        ElementItem('Lanthanide',   8), ElementItem('Actinide',             9),
    ]

    ShellsTable = [
        ElementItem('s-shell', 0), ElementItem('p-shell', 1), ElementItem('d-shell', 2), ElementItem('f-shell', 3),
    ]

    PanelData = [
        PanelItem('atomicNumber',          'Atomic Number'     ),
        PanelItem('symbol',                'Symbol'            ),
        PanelItem('standardState',         'State'             ),
        PanelItem('atomicMass',            'Atomic Mass'       ),
        PanelItem('numberOfProtons',       'Protons'           ),
        PanelItem('numberOfNeutrons',      'Neutrons'          ),
        PanelItem('numberOfElectrons',     'Electrons'         ),
        PanelItem('numberOfValence',       'Valence Electrons' ),
        PanelItem('valency',               'Valency'           ),
        PanelItem('atomicRadius',          'Atomic Radius'     ),
        PanelItem('density',               'Density'           ),
        PanelItem('electronegativity',     'Electronegativity' ),
        PanelItem('ionizationEnergy',      'Ionization Energy' ),
        PanelItem('electronAffinity',      'Electron Affinity' ),
        PanelItem('meltingPoint',          'Melting Point'     ),
        PanelItem('boilingPoint',          'Boiling Point'     ),
        PanelItem('specificHeat',          'Specific Heat'     ),
        PanelItem('radioactive',           'Radioactive'       ),
        PanelItem('occurrence',            'Occurrence'        ),
        PanelItem('yearDiscovered',        'Year'              ),
        PanelItem('electronConfiguration', 'Electron Config'   ),
        PanelItem('oxidationStates',       'Oxidation States'  ),
    ]

    SearchConfig = {
        'MAX_SEARCH_LENGTH':  36,
        'MAX_SEARCH_RESULTS': 23,
    }

class FocusConfig:

    def __init__(self, type, id=None):
        self.type = type
        self.id = id

class SearchConfig:

    def __init__(self, query, results, index):
        self.query = query
        self.results = results
        self.index = index

class MeterItem:

    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

class ElementItem:
    def __init__(self, row, column):
        self.row = row
        self.column = column

class BoardItemConfig:

    class Selected:

        def __init__(self):
            self.type = None

    class Display:

        def __init__(self):
            self.family = None
            self.shell = None
            self.state = None
            self.valenceElectrons = None
            self.valency = None
            self.radioactive = None
            self.occurrence = None
            self.meter = None
            self.isAncient = None

    def __init__(self, atomic_number):
        self.atomic_number = atomic_number
        self.selected = BoardItemConfig.Selected()
        self.display = BoardItemConfig.Display()

class ListConfig:

    def __init__(self):
        self.indicated = None
        self.selected = None

class PanelConfig:

    class Top:

        def __init__(self):
            self.id = None
            self.element = None
            self.family = None
            self.shell = None
            self.query = None

    class Bottom:

        class ListItem:

            def __init__(self, key, value):
                self.key = key
                self.value = value

        def __init__(self):
            self.list = []
            self.description = None
            self.results = None
            self.index = None

    def __init__(self):
        self.top = PanelConfig.Top()
        self.bottom = PanelConfig.Bottom()

class RenderConfig:

    def __init__(self):
        self.elements = None
        self.families = None
        self.shells = None
        self.group = None
        self.period = None
        self.display_mode = None
        self.panel = None
        self.mode = None

class StateController:

    display_mode_order = [
        DisplayModes.STANDARD,
        DisplayModes.FAMILIES,
        DisplayModes.SHELLS,
        DisplayModes.STATES,
        DisplayModes.ATOMIC_MASS,
        DisplayModes.PROTONS,
        DisplayModes.NEUTRONS,
        DisplayModes.ELECTRONS,
        DisplayModes.VALENCE_ELECTRONS,
        DisplayModes.VALENCY,
        DisplayModes.ATOMIC_RADIUS,
        DisplayModes.DENSITY,
        DisplayModes.ELECTRONEGATIVITY,
        DisplayModes.IONIZATION_ENERGY,
        DisplayModes.ELECTRON_AFFINITY,
        DisplayModes.MELTING_POINT,
        DisplayModes.BOILING_POINT,
        DisplayModes.SPECIFIC_HEAT,
        DisplayModes.RADIOACTIVE,
        DisplayModes.OCCURRENCE,
        DisplayModes.YEAR,
    ]

    def __init__(self, data, config):
        self.data = data
        if config and Utils.is_valid_atomic_number(config.atomic_number):
            self.current_focus = FocusConfig(SelectModes.ELEMENT, config.atomic_number)
        elif config and Utils.is_valid_element_symbol(config.symbol, data.get('elements')):
            element = Utils.get_element_by_symbol(config.symbol, data.get('elements'))
            self.current_focus = FocusConfig(SelectModes.ELEMENT, element.atomic_number)
        elif config and Utils.is_valid_element_name(config.name, data.get('elements')):
            element = Utils.get_element_by_name(config.name, data.get('elements'))
            self.current_focus = FocusConfig(SelectModes.ELEMENT, element.atomic_number)
        else:
            self.current_focus = FocusConfig(SelectModes.ELEMENT, 1)

        self.elements = Utils.get_elements(data.get('elements'))
        self.current_display_mode = DisplayModes.STANDARD

        self.previous_focus = None
        self.search_processor = SearchProcessor()
        self.search_state = None

        self.init_meter_config()

    def init_meter_config(self):
        field_formatters = {
            'atomicMass': (lambda v: Utils.parse_number(v, len(' u'))),
            'numberOfProtons': (lambda v: Utils.parse_number(v)),
            'numberOfNeutrons': (lambda v: Utils.parse_number(v)),
            'numberOfElectrons': (lambda v: Utils.parse_number(v)),
            'numberOfValence': (lambda v: Utils.parse_number(v)),
            'valency': (lambda v: Utils.parse_number(v)),
            'atomicRadius': (lambda v: Utils.parse_number(v, len(' pm'))),
            'density': (lambda v: Utils.parse_number(v, len(' g/cm^3'))),
            'electronegativity': (lambda v: Utils.parse_number(v)),
            'ionizationEnergy': (lambda v: Utils.parse_number(v, len(' eV'))),
            'electronAffinity': (lambda v: Utils.parse_number(v, len(' eV'))),
            'meltingPoint': (lambda v: Utils.parse_number(v, len(' K'))),
            'boilingPoint': (lambda v: Utils.parse_number(v, len(' K'))),
            'specificHeat': (lambda v: Utils.parse_number(v, len(' J/g K'))),
            'yearDiscovered': (lambda v: Utils.parse_number(v)),
        }

        field_configs = {}

        for mode in self.display_mode_order:
            if mode.is_meter:
                field_list = Utils.get_values_for_element_field(list(self.elements.values()), mode.key, field_formatters.get(mode.key))
                field_configs[mode.key] = MeterItem(Utils.get_min_value(field_list), Utils.get_max_value(field_list))

        for atomic_number, element in self.elements.items():
            element['meter_config'] = {}

            for mode in self.display_mode_order:
                if mode.is_meter:
                    field_value = element.get(mode.key)
                    element['meter_config'][mode.key] = Utils.get_meter_value(field_formatters.get(mode.key)(field_value), field_configs.get(mode.key))

    def process_left(self):
        if self.current_focus.type == SelectModes.ELEMENT:
            if self.current_focus.id > 1:
                self.current_focus.id -= 1
                return True
        elif self.current_focus.type in [SelectModes.FAMILY, SelectModes.SHELL]:
            if self.current_focus.id > 0:
                self.current_focus.id -= 1
                return True
        elif self.current_focus.type == SelectModes.SEARCH:
            self.current_focus = self.previous_focus
            self.previous_focus = None
            self.search_state = {}
            return True
        return False

    def process_right(self):
        if self.current_focus.type == SelectModes.ELEMENT:
            if self.current_focus.id < 118:
                self.current_focus.id += 1
                return True
        elif self.current_focus.type == SelectModes.FAMILY:
            if self.current_focus.id < 9:
                self.current_focus.id += 1
                return True
        elif self.current_focus.type == SelectModes.SHELL:
            if self.current_focus.id < 3:
                self.current_focus.id += 1
                return True
        return False

    def process_up(self):
        if self.current_focus.type == SelectModes.ELEMENT:
            current_pos = self._find_element(self.current_focus.id)
            if self.current_focus.id == 57:
                self.current_focus.id = 39
                return True
            elif current_pos.row > 0:
                next_atomic_number = Layout.PeriodicTable[current_pos.row - 1][current_pos.column]
                if next_atomic_number != 0:
                    self.current_focus.id = next_atomic_number
                    return True
        elif self.current_focus.type == SelectModes.FAMILY:
            if 4 <= self.current_focus.id <= 9:
                self.current_focus.id -= 4
            elif self.current_focus.id == 0:
                self.current_focus = FocusConfig(SelectModes.ELEMENT, 89)
            elif self.current_focus.id == 1:
                self.current_focus = FocusConfig(SelectModes.ELEMENT, 91)
            elif self.current_focus.id == 2:
                self.current_focus = FocusConfig(SelectModes.ELEMENT, 95)
            else:
                self.current_focus = FocusConfig(SelectModes.ELEMENT, 99)
            return True
        elif self.current_focus.type == SelectModes.SHELL:
            if self.current_focus.id == 0:
                self.current_focus = FocusConfig(SelectModes.FAMILY, 8)
            elif self.current_focus.id == 1:
                self.current_focus = FocusConfig(SelectModes.FAMILY, 9)
            elif self.current_focus.id == 2:
                self.current_focus = FocusConfig(SelectModes.FAMILY, 6)
            else:
                self.current_focus = FocusConfig(SelectModes.FAMILY, 7)
            return True
        elif self.current_focus.type == SelectModes.SEARCH:
            if self.search_state and self.search_state.results and len(self.search_state.results) > 0 and \
                    self.search_state.index is not None and self.search_state.index > 0:
                self.search_state.index -= 1
                return True
        return False

    def process_down(self):
        if self.current_focus.type == SelectModes.ELEMENT:
            current_pos = self._find_element(self.current_focus.id)
            if self.current_focus.id in [39, 87, 88]:
                self.current_focus.id = 57
                return True
            elif self.current_focus.id == 118:
                self.current_focus.id = 71
                return True
            else:
                if current_pos.row < 8:
                    self.current_focus.id = Layout.PeriodicTable[current_pos.row + 1][current_pos.column]
                else:
                    if self.current_focus.id in [89, 90]:
                        self.current_focus = FocusConfig(SelectModes.FAMILY, 0)
                    elif self.current_focus.id in [91, 92, 93, 94]:
                        self.current_focus = FocusConfig(SelectModes.FAMILY, 1)
                    elif self.current_focus.id in [95, 96, 97, 98]:
                        self.current_focus = FocusConfig(SelectModes.FAMILY, 2)
                    else:
                        self.current_focus = FocusConfig(SelectModes.FAMILY, 3)
                return True
        elif self.current_focus.type == SelectModes.FAMILY:
            if 0 <= self.current_focus.id <= 5:
                self.current_focus.id += 4
            elif self.current_focus.id == 6:
                self.current_focus = FocusConfig(SelectModes.SHELL, 2)
            elif self.current_focus.id == 7:
                self.current_focus = FocusConfig(SelectModes.SHELL, 3)
            elif self.current_focus.id == 8:
                self.current_focus = FocusConfig(SelectModes.SHELL, 0)
            else:
                self.current_focus = FocusConfig(SelectModes.SHELL, 1)
            return True
        elif self.current_focus.type == SelectModes.SEARCH:
            if self.search_state and self.search_state.results and len(self.search_state.results) > 0 and \
                    self.search_state.index is not None and self.search_state.index + 1 < len(self.search_state.results):
                self.search_state.index += 1
                return True
        return False

    def process_slash(self):
        current_index = self.display_mode_order.index(self.current_display_mode)
        if current_index == len(self.display_mode_order) - 1:
            self.current_display_mode = self.display_mode_order[0]
        else:
            self.current_display_mode = self.display_mode_order[current_index + 1]
        return True

    def process_backslash(self):
        current_index = self.display_mode_order.index(self.current_display_mode)
        if current_index == 0:
            self.current_display_mode = self.display_mode_order[-1]
        else:
            self.current_display_mode = self.display_mode_order[current_index - 1]
        return True

    def process_backspace(self):
        if self.current_focus.type == SelectModes.SEARCH:
            if self.search_state and self.search_state.query and len(self.search_state.query) > 0:
                self.search_state.query = self.search_state.query[:-1]
                if len(self.search_state.query) == 0:
                    self.current_focus = self.previous_focus
                    self.previous_focus = None
                    self.search_state = None
                    return True
                self.search_state.results = self.search_processor.query(
                    self.search_state.query, Layout.SearchConfig['MAX_SEARCH_RESULTS'], self.data
                )
                self.search_state.index = 0
            return True
        return False

    def process_enter(self):
        if self.current_focus.type == SelectModes.SEARCH:
            if (
                self.search_state is not None
                and self.search_state.results is not None
                and len(self.search_state.results) > 0
                and self.search_state.index < len(self.search_state.results)
            ):
                selected_item = self.search_state.results[self.search_state.index]
                if selected_item.type == SearchResultType.ELEMENT:
                    self.current_focus = FocusConfig(SelectModes.ELEMENT, selected_item.id)
                elif selected_item.type == SearchResultType.FAMILY:
                    family_index = self._find_family(selected_item.id)
                    self.current_focus = FocusConfig(SelectModes.FAMILY, family_index)
                elif selected_item.type == SearchResultType.SHELL:
                    shell_index = self._find_shell(selected_item.id)
                    self.current_focus = FocusConfig(SelectModes.SHELL, shell_index)
                else:
                    self.current_focus = self.previous_focus
            else:
                self.current_focus = self.previous_focus
            self.previous_focus = None
            self.search_state = None
            return True
        return False

    def process_search_input(self, key):
        if self.current_focus.type != SelectModes.SEARCH:
            # Don't start query with space or dash
            if key == ' ' or key == '-':
                return False
            self.previous_focus = self.current_focus
            self.current_focus = FocusConfig(SelectModes.SEARCH)
            self.search_state = SearchConfig('', [], 0)

        if self.search_state.query and len(self.search_state.query) >= Layout.SearchConfig['MAX_SEARCH_LENGTH']:
            return False

        # Don't allow appending multiple spaces or dashes
        if (
            self.search_state.query is not None
            and len(self.search_state.query) > 0
            and (
                (self.search_state.query[-1] == ' ' and key == ' ')
                or (self.search_state.query[-1] == '-' and key == '-')
            )
        ):
            return False

        self.search_state.query += key.upper()
        self.search_state.results = self.search_processor.query(
            self.search_state.query, Layout.SearchConfig['MAX_SEARCH_RESULTS'], self.data
        )
        self.search_state.index = 0
        return True

    def get_render_config(self):
        board = {}
        families = ListConfig()
        shells = ListConfig()
        group = None
        period = None
        panel = PanelConfig()
        
        for r in range(len(Layout.PeriodicTable)):
            for c in range(len(Layout.PeriodicTable[r])):
                if Layout.PeriodicTable[r][c] > 0:
                    config = BoardItemConfig(Layout.PeriodicTable[r][c])
                    if (
                        self.current_focus.type == SelectModes.ELEMENT
                        and self.current_focus.id == Layout.PeriodicTable[r][c]
                    ):
                        config.selected.type = SelectModes.ELEMENT
                    elif (
                        self.current_focus.type == SelectModes.FAMILY
                        and self.elements[Layout.PeriodicTable[r][c]].get('family') == Layout.FamiliesTable[self.current_focus.id].key
                    ):
                        config.selected.type = SelectModes.FAMILY
                    elif (
                        self.current_focus.type == SelectModes.SHELL
                        and self.elements[Layout.PeriodicTable[r][c]].get('shell') == Layout.ShellsTable[self.current_focus.id].key
                    ):
                        config.selected.type = SelectModes.SHELL

                    if self.current_display_mode == DisplayModes.FAMILIES:
                        config.display.family = self.elements[Layout.PeriodicTable[r][c]].get('family')
                    elif self.current_display_mode == DisplayModes.SHELLS:
                        config.display.shell = self.elements[Layout.PeriodicTable[r][c]].get('shell')
                    elif self.current_display_mode == DisplayModes.STATES:
                        config.display.state = self.elements[Layout.PeriodicTable[r][c]].get('standardState')
                    elif self.current_display_mode == DisplayModes.VALENCE_ELECTRONS:
                        config.display.valenceElectrons = self.elements[Layout.PeriodicTable[r][c]].get('numberOfValence')
                    elif self.current_display_mode == DisplayModes.VALENCY:
                        config.display.valency = self.elements[Layout.PeriodicTable[r][c]].get('valency')
                    elif self.current_display_mode == DisplayModes.RADIOACTIVE:
                        config.display.radioactive = self.elements[Layout.PeriodicTable[r][c]].get('radioactive')
                    elif self.current_display_mode == DisplayModes.OCCURRENCE:
                        config.display.occurrence = self.elements[Layout.PeriodicTable[r][c]].get('occurrence')
                    elif self.current_display_mode and self.current_display_mode.is_meter:
                        config.display.meter = self.elements[Layout.PeriodicTable[r][c]]['meter_config'].get(self.current_display_mode.key)
                        if self.current_display_mode == DisplayModes.YEAR:
                            config.display.isAncient = True if self.elements[Layout.PeriodicTable[r][c]].get(self.current_display_mode.key) == 'Ancient' else None
                    board[Layout.PeriodicTable[r][c]] = config

        if self.current_focus.type == SelectModes.ELEMENT:
            families.indicated = self.elements[self.current_focus.id].get('family')
            shells.indicated = self.elements[self.current_focus.id].get('shell')
            group = self.elements[self.current_focus.id].get('group')
            period = self.elements[self.current_focus.id].get('period')
            panel.top.element = self.elements[self.current_focus.id].get('name')
            panel.top.id = self.current_focus.id
            for key_config in Layout.PanelData:
                value = self.elements[self.current_focus.id].get(key_config.key)
                panel.bottom.list.append(PanelConfig.Bottom.ListItem(key_config.name, value))
        elif self.current_focus.type == SelectModes.FAMILY:
            families.selected = Layout.FamiliesTable[self.current_focus.id].key
            panel.top.family = self.data.get('families').get(Layout.FamiliesTable[self.current_focus.id].key).get('name')
            panel.top.id = Layout.FamiliesTable[self.current_focus.id].key
            panel.bottom.description = self.data.get('families').get(Layout.FamiliesTable[self.current_focus.id].key).get('description')
        elif self.current_focus.type == SelectModes.SHELL:
            shells.selected = Layout.ShellsTable[self.current_focus.id].key
            panel.top.shell = self.data.get('shells').get(Layout.ShellsTable[self.current_focus.id].key).get('name')
            panel.top.id = Layout.ShellsTable[self.current_focus.id].key
            panel.bottom.description = self.data.get('shells').get(Layout.ShellsTable[self.current_focus.id].key).get('description')
        elif self.current_focus.type == SelectModes.SEARCH:
            panel.top.query = self.search_state.query
            panel.bottom.results = self.search_state.results
            panel.bottom.index = self.search_state.index

        render_config = RenderConfig()
        render_config.elements = board
        render_config.families = families
        render_config.shells = shells
        render_config.group = group
        render_config.period = period
        render_config.displayMode = self.current_display_mode
        render_config.panel = panel
        render_config.mode = self.current_focus.type
        return render_config

    def _find_element(self, atomic_number):
        for row in range(len(Layout.PeriodicTable)):
            for column in range(len(Layout.PeriodicTable[row])):
                if Layout.PeriodicTable[row][column] == atomic_number:
                    return ElementItem(row, column)
        return None

    def _find_family(self, family_key):
        for i in range(len(Layout.FamiliesTable)):
            if Layout.FamiliesTable[i].key == family_key:
                return Layout.FamiliesTable[i].index
        return None

    def _find_shell(self, shell_key):
        for i in range(len(Layout.ShellsTable)):
            if Layout.ShellsTable[i].key == shell_key:
                return Layout.ShellsTable[i].index
        return None
