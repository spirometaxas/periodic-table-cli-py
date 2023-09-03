class Utils:

    def get_elements(elements):
        return { element['atomicNumber']: element for element in elements }

    def get_families(elements):
        families = {}
        for element in elements:
            if element.get('family') is not None and element.get('family') != '':
                if element.get('family') not in families:
                    families[element.get('family')] = []
                families[element.get('family')].append(element)
        return families

    def get_shells(elements):
        shells = {}
        for element in elements:
            if element.get('shell') is not None and element.get('shell') != '':
                if element.get('shell') not in shells:
                    shells[element.get('shell')] = []
                shells[element.get('shell')].append(element)
        return shells

    def is_valid_atomic_number(atomic_number):
        return atomic_number and atomic_number >= 1 and atomic_number <= 118

    def get_element_by_atomic_number(atomic_number, elements):
        if atomic_number is None:
            return None
        for element in elements:
            if element.get('atomicNumber') == atomic_number:
                return element
        return None

    def is_valid_element_name(name, elements):
        if name is None:
            return False
        for element in elements:
            if element.get('name').lower() == name.lower():
                return True
        return False

    def get_element_by_name(name, elements):
        if name is None:
            return None
        for element in elements:
            if element.get('name').lower() == name.lower():
                return element
        return None

    def is_valid_element_symbol(symbol, elements):
        if symbol is None:
            return False
        for element in elements:
            if element.get('symbol').lower() == symbol.lower():
                return True
        return False

    def get_element_by_symbol(symbol, elements):
        if symbol is None:
            return None
        for element in elements:
            if element.get('symbol').lower() == symbol.lower():
                return element
        return None

    def is_bottom_section(atomic_number):
        # Lanthanide or Actinide
        return (atomic_number >= 57 and atomic_number <= 71) or (atomic_number >= 89 and atomic_number <= 103)