from __future__ import annotations

import subprocess


def line_count(filename: str) -> int:
    """*nix only"""
    return int(subprocess.check_output(['wc', '-l', filename]).split()[0])


class Round:
    def __init__(self, cubes: dict[str, int]):
        self.cubes = cubes

    @classmethod
    def from_str(cls, line: str) -> Round:
        cubes: dict[str, int] = {}

        for cube_set in line.split('; '):
            revealed_cubes = cube_set.split(', ')
            for cube in revealed_cubes:
                count, colour = cube.split()
                cubes[colour] = int(count)

        return cls(cubes)

    def __repr__(self) -> str:
        return f'<Round cubes={self.cubes}>'


class Game:
    """
    A game is a collection of rounds. It keeps track
    of the max number of cubes of each colour across
    all rounds.
    """

    def __init__(self, game_id: int, rounds: list[Round]):
        self.id = game_id

        # keep the count of max cubes of each colour across all rounds
        self.cubes: dict[str, int] = {}

        for round in rounds:
            for colour, count in round.cubes.items():
                self.cubes[colour] = max(count, self.cubes.get(colour, 0))

    @classmethod
    def from_str(cls, line: str) -> Game:
        game_str, cube_str = line.split(': ')
        game_id = int(game_str.split()[-1])

        rounds: list[Round] = [Round.from_str(round_str) for round_str in cube_str.split('; ')]

        return cls(game_id, rounds)

    def __repr__(self) -> str:
        return f'<Game id={self.id} cubes={self.cubes}>'
