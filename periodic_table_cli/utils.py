class Utils:

    @staticmethod
    def get_elements(elements):
        return { element['atomicNumber']: element for element in elements }

    @staticmethod
    def get_families(elements):
        families = {}
        for element in elements:
            if element.get('family') is not None and element.get('family') != '':
                if element.get('family') not in families:
                    families[element.get('family')] = []
                families[element.get('family')].append(element)
        return families

    @staticmethod
    def get_shells(elements):
        shells = {}
        for element in elements:
            if element.get('shell') is not None and element.get('shell') != '':
                if element.get('shell') not in shells:
                    shells[element.get('shell')] = []
                shells[element.get('shell')].append(element)
        return shells

    @staticmethod
    def is_valid_atomic_number(atomic_number):
        return atomic_number and atomic_number >= 1 and atomic_number <= 118

    @staticmethod
    def get_element_by_atomic_number(atomic_number, elements):
        if atomic_number is None:
            return None
        for element in elements:
            if element.get('atomicNumber') == atomic_number:
                return element
        return None

    @staticmethod
    def is_valid_element_name(name, elements):
        if name is None:
            return False
        for element in elements:
            if element.get('name').lower() == name.lower():
                return True
        return False

    @staticmethod
    def get_element_by_name(name, elements):
        if name is None:
            return None
        for element in elements:
            if element.get('name').lower() == name.lower():
                return element
        return None

    @staticmethod
    def is_valid_element_symbol(symbol, elements):
        if symbol is None:
            return False
        for element in elements:
            if element.get('symbol').lower() == symbol.lower():
                return True
        return False

    @staticmethod
    def get_element_by_symbol(symbol, elements):
        if symbol is None:
            return None
        for element in elements:
            if element.get('symbol').lower() == symbol.lower():
                return element
        return None

    @staticmethod
    def is_bottom_section(atomic_number):
        # Lanthanide or Actinide
        return (atomic_number >= 57 and atomic_number <= 71) or (atomic_number >= 89 and atomic_number <= 103)

    @staticmethod
    def get_values_for_element_field(elements, field_name, formatter=None):
        return [formatter(e.get(field_name)) if formatter is not None else e.get(field_name) for e in elements]

    @staticmethod
    def get_max_value(values):
        max_val = float('-inf')
        for v in values:
            if v is not None and v > max_val:
                max_val = v
        return max_val

    @staticmethod
    def get_min_value(values):
        min_val = float('inf')
        for v in values:
            if v is not None and v < min_val:
                min_val = v
        return min_val

    @staticmethod
    def get_meter_value(value, config):
        if config and config.max_value is not None and config.min_value is not None and value is not None:
            meter_value = (value - config.min_value) / (config.max_value - config.min_value)
            return max(min(meter_value, 1.0), 0.0)
        return None

    @staticmethod
    def is_number(value):
        return isinstance(value, int) or isinstance(value, float)

    @staticmethod
    def parse_number(value, units_length=None):
        parsed_number = None
        if value is not None and units_length is not None and len(value) > units_length:
            parsed_number = float(value[:-units_length])
        elif value is not None:
            try:
                parsed_number = float(value)
            except:
                pass
        if parsed_number is not None and Utils.is_number(parsed_number):
            return parsed_number
        return None

    @staticmethod
    def get_bucket_value(meter_value, buckets):
        bucket = int(meter_value * buckets)
        if bucket == buckets:
            return bucket - 1
        return bucket

    @staticmethod
    def chain_sort(o1, o2, sorts):
        for sort in sorts:
            res = sort(o1, o2)
            if res is not None and res != 0 and Utils.is_number(res):
                return res
        return 0