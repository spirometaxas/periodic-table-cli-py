from utils import Utils
from functools import cmp_to_key

class SearchResultType:
    ELEMENT = 'element'
    FAMILY  = 'family'
    SHELL   = 'shell'

class SearchResult:

    class Section:

        def __init__(self, text, index=None):
            self.text = text
            self.index = index

    def __init__(self, type, id):
        self.type = type
        self.id = id
        self.name = None
        self.atomic_number = None
        self.atomic_symbol = None

class SearchProcessor:

    def _is_atomic_number_search(self, text):
        return text is not None and len(text) > 0 and text[0].isdigit()

    def _get_atomic_number_matches(self, text, data):
        results = []
        for element in data.get('elements'):
            atomic_number_string = str(element.get('atomicNumber'))
            index_value = atomic_number_string.find(text)
            if index_value >= 0:
                result = SearchResult(SearchResultType.ELEMENT, element.get('atomicNumber'))
                result.atomic_number = SearchResult.Section(atomic_number_string, index_value)
                result.name = SearchResult.Section(element.get('name'))
                results.append(result)
        return sorted(results, key=cmp_to_key(lambda o1, o2: Utils.chain_sort(o1, o2, [
                lambda o1, o2: o1.atomic_number.index - o2.atomic_number.index,
                lambda o1, o2: o1.id - o2.id,
            ])))

    def _get_atomic_symbol_and_name_matches(self, text, data):
        results = []
        for element in data.get('elements'):
            atomic_symbol = element.get('symbol')
            symbol_index_value = atomic_symbol.lower().find(text.lower())
            atomic_name = element.get('name')
            name_index_value = atomic_name.lower().find(text.lower())
            
            if symbol_index_value >= 0 or name_index_value >= 0:
                result = SearchResult(SearchResultType.ELEMENT, element.get('atomicNumber'))
                result.atomic_symbol = SearchResult.Section(atomic_symbol, symbol_index_value if symbol_index_value >= 0 else None)
                result.name = SearchResult.Section(atomic_name, name_index_value if name_index_value >= 0 else None)
                results.append(result)

        return sorted(results, key=cmp_to_key(lambda o1, o2: Utils.chain_sort(o1, o2, [
                lambda o1, o2: SearchProcessor._sort_by_index(o1, o2),
                lambda o1, o2: SearchProcessor._sort_by_matched_symbol_or_name(o1, o2),
                lambda o1, o2: len(o1.atomic_symbol.text) - len(o2.atomic_symbol.text) if o1.atomic_symbol.index is not None and o2.atomic_symbol.index is not None else 0,
                lambda o1, o2: SearchProcessor._sort_by_index(o1, o2),
                lambda o1, o2: o1.id - o2.id,
            ])))

    @staticmethod
    def _sort_by_index(o1, o2):
        o1IndexMin = SearchProcessor._get_index_min(o1.atomic_symbol.index, o1.name.index)
        o2IndexMin = SearchProcessor._get_index_min(o2.atomic_symbol.index, o2.name.index)
        return o1IndexMin - o2IndexMin

    @staticmethod
    def _sort_by_matched_symbol_or_name(o1, o2):
        if o1.atomic_symbol.index is not None and o1.name.index is not None and (o2.atomic_symbol.index is None or o2.name.index is None):
            return -1
        elif o2.atomic_symbol.index is not None and o2.name.index is not None and (o1.atomic_symbol.index is None or o1.name.index is None):
            return 1
        elif o1.atomic_symbol.index is not None and o2.atomic_symbol.index is None:
            return -1
        elif o2.atomic_symbol.index is not None and o1.atomic_symbol.index is None:
            return 1
        elif o1.name.index is not None and o2.name.index is None:
            return -1
        elif o2.name.index is not None and o1.name.index is None:
            return 1
        else:
            return 0

    def _get_element_family_name_matches(self, text, data):
        results = []
        for key_name, family_info in data.get('families').items():
            family_name = family_info.get('name')
            name_index_value = family_name.lower().find(text.lower())
            if name_index_value >= 0:
                result = SearchResult(SearchResultType.FAMILY, key_name)
                result.name = SearchResult.Section(family_name, name_index_value if name_index_value >= 0 else None)
                results.append(result)
        return sorted(results, key=cmp_to_key(lambda o1, o2: Utils.chain_sort(o1, o2, [
                lambda o1, o2: o1.name.index - o2.name.index
            ])))

    def _get_shell_name_matches(self, text, data):
        results = []
        for key_name, shell_info in data.get('shells').items():
            shell_name = shell_info.get('name')
            name_index_value = shell_name.lower().find(text.lower())
            if name_index_value >= 0:
                result = SearchResult(SearchResultType.SHELL, key_name)
                result.name = SearchResult.Section(shell_name, name_index_value if name_index_value >= 0 else None)
                results.append(result)
        return sorted(results, key=cmp_to_key(lambda o1, o2: Utils.chain_sort(o1, o2, [
                lambda o1, o2: o1.name.index - o2.name.index
            ])))

    @staticmethod
    def _get_index_min(index1, index2):
        if index1 is not None and index2 is not None:
            return min(index1, index2)
        elif index1 is not None:
            return index1
        else:
            return index2

    @staticmethod
    def _get_index_max(index1, index2):
        if index1 is not None and index2 is not None:
            return max(index1, index2)
        elif index1 is not None:
            return index1
        else:
            return index2

    def query(self, text, max_results, data):
        results = []
        if self._is_atomic_number_search(text):
            results.extend(self._get_atomic_number_matches(text, data))
        else:
            atomic_symbol_name_matches = self._get_atomic_symbol_and_name_matches(text, data)
            element_family_name_matches = self._get_element_family_name_matches(text, data)
            shell_name_matches = self._get_shell_name_matches(text, data)
            results.extend(atomic_symbol_name_matches)
            results.extend(element_family_name_matches)
            results.extend(shell_name_matches)

        return results[:max_results]