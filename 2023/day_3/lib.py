import sys

from pathlib import Path
from typing import Iterator, Optional


Position = tuple[int, int]


def error(msg: str) -> None:
    print(msg, file=sys.stderr)
    exit(1)


class EngineSchematic:
    @classmethod
    def from_file(cls, path: Path):
        if not path.exists():
            error(f'file not found: {path}')

        with open(path) as f:
            return cls(schematic=[line.strip() for line in f.readlines()])

    def extract_num(self, row: int, col: int) -> Optional[int]:
        """
        Extract a number in its entirety from the schematic, starting at (x, y).

        First check if the current position is a number. If it isn't, return None.

        Then check the left side if we have a number, keep going until we hit a symbol.
        Keep track of the number of digits we've seen so far and prepend them to a string.

        Then check the right side if we have a number, keep going until we hit a symbol.
        Keep track of the number of digits we've seen so far and append them to the string.

        Finally, return the string as an int.
        """
        if not self._is_num(row, col):
            return None

        return int(self._extract_num_left(row, col) + self[row][col] + self._extract_num_right(row, col))

    def iter_all_symbol_positions(self) -> Iterator[Position]:
        """
        Iterate over the schematic and yield the position of each symbol.
        """
        for row in range(len(self.schematic)):
            for col in range(len(self.schematic[row])):
                if not self._is_num(row, col) and self[row][col] != '.':
                    yield row, col

    def iter_symbol_positions(self, symbol: str) -> Iterator[Position]:
        """
        Iterate over the schematic and yield the position of the given symbol.
        """
        for row in range(len(self.schematic)):
            for col in range(len(self.schematic[row])):
                if self[row][col] == symbol:
                    yield row, col

    def extract_nums_around(self, row: int, col: int) -> set[int]:
        """
        Extract all the numbers around a symbol.
        """

        nums = set()

        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                num = self.extract_num(r, c)

                if num is not None:
                    nums.add(num)

        return nums

    def _extract_num_left(self, row: int, col: int) -> str:
        num: list[str] = []
        col -= 1

        while col >= 0 and self._is_num(row, col):
            num.append(self[row][col])
            col -= 1

        return ''.join(reversed(num))

    def _extract_num_right(self, row: int, col: int) -> str:
        num: list[str] = []
        col += 1

        while col < len(self[row]) and self._is_num(row, col):
            num.append(self[row][col])
            col += 1

        return ''.join(num)

    def _is_num(self, row: int, col: int) -> bool:
        """
        Check if the current position is a number.
        """
        return self[row][col].isdigit()

    def __getitem__(self, key: int) -> str:
        """
        Allow indexing into the schematic.
        """
        return self.schematic[key]

    def __init__(self, schematic: list[str]):
        self.schematic = schematic

    def __str__(self) -> str:
        return '\n'.join(self.schematic)

    def __repr__(self) -> str:
        assert len(self.schematic) > 0, 'schematic is empty'
        return f'<EngineSchematic rows={len(self.schematic)} cols={len(self.schematic[0])}>'
