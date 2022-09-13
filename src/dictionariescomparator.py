from typing import Dict, List


class DictionariesComparator:
    """
    Given two dictionaries, reports:
    - which keys have the same value in both dictonaries,
    - which are present in both dictionaries, but with different values,
    - which are unique.
    """
    def __init__(self, a: Dict, b: Dict, a_id: int, b_id: int, all_groups: bool = False) -> None:
        self.a = a
        self.b = b
        self.a_id = a_id if self.a else ''
        self.b_id = b_id if self.b else ''
        self.all_groups = all_groups
        self.__distribute_keys()
        self.__print('Same key and value', self.same_value)
        self.__print('Same key', self.same_key)
        self.__print('Unique keys', self.unique_keys)

    def __distribute_keys(self) -> None:
        """
        Merges the keys of both dicitionaries and group them in three
        groups: same_value, same_key and unique_keys.
        """
        self.same_value = []
        self.same_key = []
        self.unique_keys = []
        merged = {**self.a, **self.b}
        all_keys = sorted(merged.keys())
        for k in all_keys:
            if k in self.a and k in self.b:
                if self.a[k] == self.b[k]:
                    self.same_value.append(k)
                else:
                    self.same_key.append(k)
            else:
                self.unique_keys.append(k)
    
    def __print(self, title: str, group: List) -> None:
        """
        Prints the keys and its values in each dicionary that belong to 
        the passed group.
        """
        KEYSIZE = 30
        VALUESIZE = 50

        def make_line(key: str, a: str, b: str) -> str:
            """
            Returns a line composed by a key and its value in each dictionary.
            """
            line = f'{key:<{KEYSIZE}} {a:<{VALUESIZE}} {b:<{VALUESIZE}}'
            return line

        def get_value_into_pieces(dic: Dict, key: str) -> List:
            """
            Splits the string representation of the key's value, whenever its
            length is bigger than VALUESIZE.
            """
            value = str(dic.get(key, ''))
            pieces = [value]
            if len(value) > VALUESIZE:
                pieces = []
                while value:
                    pieces.append(value[:VALUESIZE])
                    value = value[VALUESIZE:]
            return pieces

        if group or self.all_groups:
            header = make_line(title, self.a_id, self.b_id)
            dashed_line = len(header) * '-'
            print()
            print(header)
            print(dashed_line)
            for k in group:
                pieces_a = get_value_into_pieces(self.a, k)
                pieces_b = get_value_into_pieces(self.b, k)
                key_line = make_line(k, pieces_a.pop(0), pieces_b.pop(0))
                print(key_line)
                while pieces_a or pieces_b:
                    piece_a = pieces_a.pop(0) if pieces_a else ''
                    piece_b = pieces_b.pop(0) if pieces_b else ''
                    continuation_line = make_line('', piece_a, piece_b)
                    print(continuation_line)
            print()
